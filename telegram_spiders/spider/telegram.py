from telethon import TelegramClient
from telethon.sessions import StringSession
from telethon.tl.functions.contacts import GetContactsRequest
from telethon.tl.functions.account import GetAuthorizationsRequest
from telethon.tl.types import Channel, User, Chat

import config
from config import images_dir
from utils import *
from message_util import get_code
import asyncio
import time

api_id = config.api_id
api_hash = config.api_hash


async def login():
    login_flag = False
    phone = input("请输入手机号\n")

    # 自动登录
    if session_file_exists(phone=phone):
        print("自动登录中...")
        session = read_session_file(phone=phone)
        client = TelegramClient(StringSession(session), api_id, api_hash)
    # 手动登录
    else:
        login_flag = True
        client = TelegramClient(StringSession(), api_id, api_hash)

    # 连接telegram服务
    try:
        print("连接telegram服务...")
        await client.connect()
    except OSError:
        print("连接telegram服务失败")

    # 手动输入验证码来登录
    if login_flag:
        print("请手动登录，等待验证码...")
        await client.send_code_request(phone=phone, force_sms=True)

        time.sleep(5)
        code = get_code(phone[2:])
        # code = input("请输入手机收到的验证码...\n")
        await client.sign_in(phone=phone, code=code)

        # 保存session以便下次自动登录
        session = client.session.save()
        save_session_file(phone=phone, session=session)

    # 判断是否登录成功
    if await client.is_user_authorized():
        print(str(phone) + "登录成功！")

    return client


async def get_me_info(client):
    print("获取个人信息...")
    me = await client.get_me()
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
            for participant in participant_list:
                insert_user_info(participant)
                insert_channel_user(channel_info["id"], participant["id"])

            # 获取历史消息
            # message_list = await get_messages(client, entity)

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
            for participant in participant_list:
                insert_user_info(participant)
                insert_group_user(group_info["id"], participant["id"])

            # 获取历史消息
            # message_list = await get_messages(client, entity)


async def main():
    # 登录以获得client
    client = await login()
    await get_me_info(client)
    await get_contacts_info(client)
    await get_dialogs_info(client)


if __name__ == '__main__':
    loop = asyncio.get_event_loop()
    loop.run_until_complete(login())
