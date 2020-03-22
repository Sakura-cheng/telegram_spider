import asyncio
from threading import Thread
import os
import math
from multiprocessing import Process
import argparse
import datetime
import time

from telethon.tl.functions.contacts import ImportContactsRequest
from telethon.tl.types import InputPhoneContact

import config
from save_util import save_user_info
from sql_util import insert_check_user_info, get_session, update_session_time, get_login_phones
from my_test import login


class MyCheck:
    '''
    通过添加好友的方式检测手机号是否注册
    如果注册则获取user信息
    '''

    def __init__(self):
        self.client = None
        self.N = 0

    async def set_client(self, login_phone):
        self.client = await login(login_phone)

    async def check(self, phone_str, peer_num):
        '''
        检测手机号是否注册
        :param phone_str:
        :return:
        '''
        contact = InputPhoneContact(client_id=0, phone=phone_str, first_name="zhang",
                                    last_name="san")
        try:
            result = await self.client(ImportContactsRequest(contacts=[contact]))
            self.N += 1
            users = result.users
            if len(users) > 0:
                print(phone_str + "已注册------" + str(self.N) + "------" + str(peer_num))
            else:
                print(phone_str + "未注册------" + str(self.N) + "------" + str(peer_num))
        except Exception as e:
            raise e


def task(login_phone, add_user):
    # loop = asyncio.new_event_loop()
    check = MyCheck()
    loop = asyncio.new_event_loop()
    try:
        loop.run_until_complete(check.set_client(login_phone))
    except Exception as e:
        print(e)
        return


    phone_str = ''
    peer_num = 1

    Error = False
    rnum = 0
    for i in range(len(add_user)):
        phone_str = str(add_user[i])
        try:
            loop.run_until_complete(check.check(phone_str, peer_num))
            rnum += 1
            peer_num += 1
        except Exception as e:
            Error = True
            print(e)
            break
    # if Error:
    #     with open('my_just_test.txt', 'w') as f:
    #         f.write(phone_str)
    check.client.disconnect()
    return rnum


def main(phone):
    add_users = []
    with open("C:\\Users\\ljc\\Desktop\\add_user.txt", "r") as f:
        lines = f.readlines()
    for l in lines:
        add_users.append(l[:-1])

    login_phone = phone

    # check = MyCheck()
    # loop = asyncio.new_event_loop()
    # try:
    #     loop.run_until_complete(check.set_client(login_phone))
    # except Exception as e:
    #     print(e)
    #     return

    num = 0
    while num <= len(add_users):
        add = add_users[num:]
        num += task(login_phone, add)
        print("测试了" + str(num) + "个手机号")
        time.sleep(300)


if __name__ == '__main__':
    phone = ""
    main(phone)
