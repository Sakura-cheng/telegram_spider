import asyncio
import time
import json

from telethon import TelegramClient, events
from telethon.sessions import StringSession
from telethon.tl.functions.account import GetAuthorizationsRequest
from telethon.tl.functions.contacts import GetContactsRequest
from telethon.tl.types import Channel, User, Chat

import config
from config import images_dir, message_token
from message_util import get_code, cancel_all_recv, add_black
from save_util import *
from sql_util import *
from myLogger import log_main

# telegram的api_id和api_hash
api_id = config.api_id
api_hash = config.api_hash


async def register(phone):
    client = TelegramClient(StringSession(), api_id, api_hash)
    # 连接telegram服务
    try:
        print("连接telegram服务...")
        await client.connect()
    except OSError:
        raise RuntimeError('{"error_code": 500, "msg": "连接telegram服务失败..."}')

    print("请手动登录，等待验证码...")
    cancel_all_recv(message_token)
    try:
        await client.send_code_request(phone=phone)
    except Exception as e:
        raise RuntimeError('{"error_code": 501, "msg": "请求验证码失败..."}')

    time.sleep(5)
    # code = get_code(phone[2:])
    code = input("请输入手机收到的验证码...\n")
    try:
        await client.sign_up(code=code, first_name='Test')
    except Exception as e:
        raise RuntimeError('{"error_code": 502, "msg": "请求登录失败..."}')

    # 保存session以便下次自动登录
    session = client.session.save()
    save_session_file(phone=phone, session=session)


async def login(phone):
    '''
    登录telegram
    :return:
    '''
    login_flag = False

    # 自动登录
    session, not_use = get_session_platform(phone=phone)

    if session:
        print("自动登录中...")
        client = TelegramClient(StringSession(session), api_id, api_hash)
    # if session_file_exists(phone=phone):
    #     print("自动登录中...")
    #     session = read_session_file(phone=phone)
    #     client = TelegramClient(StringSession(session), api_id, api_hash)
    # 手动登录
    else:
        login_flag = True
        client = TelegramClient(StringSession(), api_id, api_hash)

    # 连接telegram服务
    try:
        print("连接telegram服务...")
        await client.connect()
    except OSError:
        raise RuntimeError('{"error_code": 500, "msg": "连接telegram服务失败..."}')

    # 手动输入验证码来登录
    if login_flag:
        print("请手动登录，等待验证码...")
        try:
            sent = await client.send_code_request(phone=phone, force_sms=True)
            print(sent)
        except Exception as e:
            print(e)
            if 'banned' in e.__str__():
                # 加入黑名单
                add_black(message_token, phone[2:])
                log_main.logger.error(str(phone) + "is banned")
                print('加入黑名单...')
            raise RuntimeError('{"error_code": 501, "msg": "请求验证码失败..."}')

        time.sleep(5)
        code = get_code(phone[2:])
        # code = input("请输入手机收到的验证码...\n")
        try:
            await client.sign_in(phone=phone, code=code)
        except Exception as e:
            print(e)
            raise RuntimeError('{"error_code": 502, "msg": "请求登录失败..."}')

        # 保存session以便下次自动登录
        session = client.session.save()
        save_session_file(phone=phone, session=session)
        insert_session_platform(phone=phone, session=session)

    # 判断是否登录成功
    if await client.is_user_authorized():
        print(str(phone) + "登录成功！")
        log_main.logger.info(str(phone) + "登录成功！")
        # me = await client.get_me()
        # me_info = save_user_info(me)
        # insert_check_user_info(me_info, phone)
    else:
        print("登录失败")
        log_main.logger.info(str(phone) + "登录失败")
        # 退出登录
        # await client.log_out()
        # # 删除session文件
        # delete_session_file(phone)

    return client


async def get_me_info(client):
    print("获取个人信息...")
    me = await client.get_me()
    print(me.stringify())
    if me is None:
        raise RuntimeError('{"error_code": 404, "msg": "None..."}')
    me_info = save_user_info(me)
    print(me_info)

    # 保存到数据库
    insert_user_info(me_info)
    # 下载头像
    path = await client.download_profile_photo('me', images_dir + str(me.phone) + "/profile_photo.jpg")
    print(path)

    # 获取授权
    print("获取授权（登录设备）...")
    authorizations = await client(GetAuthorizationsRequest())
    authorizations = authorizations.authorizations
    for authorization in authorizations:
        authorization_info = save_authorization_info(authorization)
        print(authorization_info)

        # 保存到数据库
        insert_authorization(authorization_info, me.id)


async def get_contacts_info(client):
    print("获取contacts列表信息...")
    contacts = await client(GetContactsRequest(0))
    users = contacts.users

    me = await client.get_me()
    for user in users:
        user_info = save_user_info(user)
        print(user_info)

        # 保存到数据库
        insert_user_info(user_info)
        insert_contact(me.id, user_info["id"])


async def get_dialogs_info(client):
    print("获得会话列表信息...")
    dialogs = await client.get_dialogs()
    me = await client.get_me()
    for dialog in dialogs:
        entity = dialog.entity
        # 是User
        if isinstance(entity, User):
            print("私聊会话...")
            user_info = save_user_info(entity)
            print(user_info)

            # 保存到数据库
            insert_user_info(user_info)

            # 获取历史消息
            message_list = await get_messages(client, entity)

            # 保存到数据库
            for m in message_list:
                insert_message(m, me.id)

        # 是Channel
        elif isinstance(entity, Channel):
            print("Channel会话...")
            channel_info = save_channel_info(entity)
            print(channel_info)

            # 获取成员
            participant_list = await get_participants(client, entity)

            # 保存到数据库
            num = len(participant_list)
            insert_channel(channel_info, me.id, num)
            insert_many_user_info(participant_list)
            insert_channel_many_user(channel_info["id"], participant_list)
            # for participant in participant_list:
            #     insert_user_info(participant)
            #     insert_channel_user(channel_info["id"], participant["id"])

            # 获取历史消息
            message_list = await get_messages(client, entity)
            # channel中的历史消息保存为json文件
            channel_message = {
                "channel_id": channel_info["id"],
                "message": message_list
            }
            if not os.path.exists('channel_messages'):
                os.mkdir("channel_messages")
            with open('channel_messages/channel_id_' + str(channel_info["id"]) + '.json', 'w', encoding='utf-8') as f:
                f.write(json.dumps(channel_message, ensure_ascii=False))

        # 是Group
        elif isinstance(entity, Chat):
            print("Group会话...")
            group_info = save_group_info(entity)
            print(group_info)

            # 获取成员
            participant_list = await get_participants(client, entity)

            # 保存到数据库
            num = len(participant_list)
            insert_group(group_info, me.id, num)
            insert_many_user_info(participant_list)
            insert_group_many_user(group_info["id"], participant_list)
            # for participant in participant_list:
            #     insert_user_info(participant)
            #     insert_group_user(group_info["id"], participant["id"])

            # 获取历史消息
            # message_list = await get_messages(client, entity)


async def monitor_message(client):
    print("增量监听...")
    me = await client.get_me()

    @client.on(events.NewMessage(incoming=True))
    async def my_handler(event):
        user = await event.get_sender()
        if isinstance(user, User):
            message = event.raw_text

            if isinstance(event.message, Message):
                message_info = save_message_info(event.message)
                print(str(me.phone) + "收到的消息: " + message_info)

                # 保存
                # 获取发送者
                user_info = save_user_info(user)
                # 保存到数据库
                insert_user_info(user_info)
                insert_message(message_info, me.id)

    await client.run_until_disconnected()


async def main(phone, category):
    # 登录以获得client
    try:
        client = await login(phone)
    except Exception as e:
        raise RuntimeError(e)

    if category == 1:
        await get_me_info(client)
        await get_contacts_info(client)
        await get_dialogs_info(client)
        await client.disconnect()
        # # 退出登录
        # await client.log_out()
        # # 删除session文件
        # delete_session_file(phone)
    elif category == 2:
        await monitor_message(client)


if __name__ == '__main__':
    # print(cancel_all_recv(message_token))
    # result = get_phone_test(message_token)
    # if result[0] == '1':
    #     phone = '86' + result[1]
    #     print(phone)
    #     input()
    # cancel_all_recv(message_token)
    # code = get_code(phone)
    # print(code)
    # print(cancel_all_recv(message_token))
    # result = get_phone_test(message_token)
    # phone = result[1]
    # time.sleep(3)
    # print(phone)
    # input('my_test')
    # loop = asyncio.get_event_loop()
    # try:
    #     loop.run_until_complete(login('86' + phone))
    # except Exception as e:
    #     print(e)
    # phone = input('shoujihao ...')
    #
    # try_num = 50
    # message_status, message = get_message(message_token, '86' + str(phone))
    # while message_status == '0' and try_num > 0:
    #     print(message)
    #     time.sleep(3)
    #     message_status, message = get_message(message_token, '86' + str(phone))
    #     try_num -= 1
    #
    # pass

    phone = '8617000616231'
    loop = asyncio.get_event_loop()
    try:
        loop.run_until_complete(main(phone, 1))
    except Exception as e:
        print(e)
