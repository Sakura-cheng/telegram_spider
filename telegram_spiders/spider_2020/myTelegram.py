import asyncio
import time

from telethon import TelegramClient
from telethon.sessions import StringSession
from telethon.tl.functions.channels import JoinChannelRequest
from telethon.tl.functions.contacts import ImportContactsRequest, GetContactsRequest
from telethon.tl.types import Channel, User, Message, InputPhoneContact

from config import api_id, api_hash
from sql_util import *
from save_util import save_message_info


class MyTG:
    def __init__(self):
        self.loop = asyncio.get_event_loop()
        self.client = None
        self.channels = []
        self.friends = []
        self.contacts = []

    async def sign_in_(self, phone):
        login_flag = False

        # 自动登录
        session, not_use = get_session(phone=phone)
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
                raise RuntimeError('{"error_code": 501, "msg": "请求验证码失败..."}')

            time.sleep(5)
            # code = get_code(phone[2:])
            code = input("请输入手机收到的验证码...\n")
            try:
                await client.sign_in(phone=phone, code=code)
            except Exception as e:
                print(e)
                raise RuntimeError('{"error_code": 502, "msg": "请求登录失败..."}')

            # 保存session以便下次自动登录
            session = client.session.save()
            # save_session_file(phone=phone, session=session)
            insert_session(phone=phone, session=session)

        # 判断是否登录成功
        if await client.is_user_authorized():
            print(str(phone) + "登录成功！")
        else:
            print("登录失败")
            delete_session(phone)
            # 退出登录
            # await client.log_out()
            # 删除session文件
            # delete_session_file(phone)
        self.client = client
        return client

    def sign_in(self, phone):
        try:
            self.loop.run_until_complete(self.sign_in_(phone))
            return True
        except Exception as e:
            print(e)
            return False

    async def add_friend_(self, phone):
        contact = InputPhoneContact(client_id=0, phone=phone, first_name=phone,
                                    last_name="test")
        try:
            result = await self.client(ImportContactsRequest(contacts=[contact]))
        except Exception as e:
            raise e

    def add_friend(self, phone):
        try:
            self.loop.run_until_complete(self.add_friend_(phone))
            print("添加成功！")
        except Exception as e:
            print("添加失败！")

    async def get_me_info_(self):
        me = await self.client.get_me()
        print(me.stringify())

    def get_me_info(self):
        try:
            self.loop.run_until_complete(self.get_me_info_())
        except Exception as e:
            print(e)

    async def add_channel_(self, entity):
        try:
            reault = await self.client(JoinChannelRequest(entity))
        except Exception as e:
            raise e

    def add_channel(self, entity):
        try:
            self.loop.run_until_complete(self.add_channel_(entity))
            print("添加成功！")
        except Exception as e:
            print("添加失败！")
            print(type(e), e)

    async def send_message_(self, entity, message):
        try:
            reasult = await self.client.send_message(entity, message)
        except Exception as e:
            raise e

    def send_message(self, entity, message):
        try:
            self.loop.run_until_complete(self.send_message_(entity, message))
            print("发送成功！")
        except Exception as e:
            print("发送失败！")
            print(type(e), e)

    # async def send_message_to_known_one_(self, who, message):
    #     who = await self.client.get_entity(who)
    #     await self.send_message_(who, message)
    #
    # def send_message_to_known_one(self, who, message):
    #     try:
    #         self.loop.run_until_complete(self.send_message_to_known_one_(who, message))
    #         print("发送成功！")
    #     except Exception as e:
    #         print("发送失败！")
    #         print(e)

    async def get_dialogs_(self):
        self.friends = []
        self.channels = []
        self.contacts = []

        contacts = await self.client(GetContactsRequest(0))
        users = contacts.users
        self.contacts = [user for user in users]

        dialogs = await self.client.get_dialogs()

        for dialog in dialogs:
            entity = dialog.entity
            # 是User
            if isinstance(entity, User):
                self.friends.append(entity)

            # 是Channel
            elif isinstance(entity, Channel):
                self.channels.append(entity)

    def get_dialogs(self):
        try:
            self.loop.run_until_complete(self.get_dialogs_())
            print(
                "该用户共有{}个好友，{}个channel，{}个私聊对话，分别为：".format(len(self.contacts), len(self.channels), len(self.friends)))
            print("好友：{}".format(len(self.contacts)))
            for m in range(len(self.contacts)):
                print("第{}个好友：{}".format(m, self.contacts[m]))
            print("channel：{}".format(len(self.channels)))
            for i in range(len(self.channels)):
                print("第{}个channel：{}".format(i, self.channels[i]))
            print("私聊会话：{}".format(len(self.friends)))
            for j in range(len(self.friends)):
                print("第{}个私聊对话：{}".format(j, self.friends[j]))
        except Exception as e:
            print(e)

    async def get_messages_(self, entity, count):
        messages = await self.client.get_messages(entity, limit=count)
        for message in messages:
            if isinstance(message, Message):
                message_info = save_message_info(message)
                print(message_info)

    def get_messages(self, entity, count):
        try:
            self.loop.run_until_complete(self.get_messages_(entity, count))
        except Exception as e:
            print(e)

    async def end_(self):
        await self.client.disconnect()

    def end(self):
        try:
            self.loop.run_until_complete(self.end_())
        except Exception as e:
            print(e)

    def run(self):
        phone = input("请输入手机号登录...")

        if not self.sign_in(phone):
            return

        option = "0"
        while option != "-1":
            print("")
            print("0.******获取对话列表******")
            print("1.******添 加 好 友******")
            print("2.******加入channel******")
            print("3.******发 送 消 息******")
            print("4.******获 取 消 息******")
            print("-1.******退      出******")
            option = input()

            if option == "0":
                self.get_dialogs()
            elif option == "1":
                add_phone = input("请输入要添加好友的手机号")
                self.add_friend(add_phone)
            elif option == "2":
                add_channel = input("请输入要添加channel的username")
                self.add_channel(add_channel)
            elif option == "3":
                self.get_dialogs()
                print("******是私聊还是在channel中发消息******")
                print("1.******         私   聊         ******")
                print("2.******         channel         ******")
                print("3.******         好   友         ******")
                option = input()
                if option == "1":
                    for i in range(len(self.friends)):
                        print("第{}个私聊对话：{}".format(i, self.friends[i]))
                    n = input("需要给第几个会话发消息\n")
                    entity = self.friends[int(n)]
                elif option == "2":
                    for i in range(len(self.channels)):
                        print("第{}个channel：{}".format(i, self.channels[i]))
                    n = input("需要给第几个会话发消息\n")
                    entity = self.channels[int(n)]
                elif option == "3":
                    for i in range(len(self.contacts)):
                        print("第{}个好友：{}".format(i, self.contacts[i]))
                    n = input("需要给第几个会话发消息\n")
                    entity = self.contacts[int(n)]
                else:
                    print("无效的操作！")
                    continue
                message = input("请输入要发送的消息\n")
                self.send_message(entity, message)
            elif option == "4":
                self.get_dialogs()
                print("******是获取私聊还是在channel中的消息******")
                print("1.******          私   聊         ******")
                print("2.******          channel         ******")
                print("3.******         好   友         ******")
                option = input()
                if option == "1":
                    for i in range(len(self.friends)):
                        print("第{}个私聊对话：{}".format(i, self.friends[i]))
                    n = input("需要获取第几个会话的消息\n")
                    entity = self.friends[int(n)]
                elif option == "2":
                    for i in range(len(self.channels)):
                        print("第{}个channel：{}".format(i, self.channels[i]))
                    n = input("需要获取第几个会话的消息\n")
                    entity = self.channels[int(n)]
                elif option == "3":
                    for i in range(len(self.contacts)):
                        print("第{}个好友：{}".format(i, self.contacts[i]))
                    n = input("需要获取第几个会话的消息\n")
                    entity = self.contacts[int(n)]
                else:
                    print("无效的操作！")
                    continue
                count = input("获取多少条消息？\n")
                self.get_messages(entity, count=int(count))
            elif option == "-1":
                pass
            else:
                print("无效的操作！")
                continue
        self.end()


if __name__ == '__main__':
    tg = MyTG()
    tg.run()
    # tg.sign_in("8616719271863")
    # tg.sign_in("8618284189214")

    # tg.send_message_to_known_one("my2020channela", "hello")
    # tg.add_channel("my2020channela")
    # tg.send_message("8617121240943", "hello")
    # tg.get_dialogs()
    # tg.get_messages(tg.friends[0], 5)
    # tg.end()
