import asyncio
from threading import Thread
import os
import random
import math
from multiprocessing import Process
import argparse
import datetime
from myLogger import log_register
import time

from telethon.tl.functions.contacts import ImportContactsRequest
from telethon.tl.types import InputPhoneContact

import config
from save_util import save_user_info
from sql_util import insert_check_user_info, get_info_from_check_user_by_phone, get_the_count_of_check_user, \
    get_the_phone_from_check_user_by_index
from test import login


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
        if not await self.client.is_user_authorized():
            raise RuntimeError(str(login_phone) + "登录失败")

    async def check(self, phone_str, peer_num):
        '''
        检测手机号是否注册
        :param phone_str:
        :return:
        '''
        me = await self.client.get_me()
        by_phone = me.phone
        contact = InputPhoneContact(client_id=0, phone=phone_str, first_name="zhang",
                                    last_name="san")
        try:
            result = await self.client(ImportContactsRequest(contacts=[contact]))
            self.N += 1
            users = result.users
            if len(users) > 0:
                log_register.logger.info(phone_str + "已注册------" + str(self.N) + "------" + str(peer_num))
                print(phone_str + "已注册------" + str(self.N) + "------" + str(peer_num))
                if not get_info_from_check_user_by_phone(phone_str):
                    for user in users:
                        # 保存到数据库
                        user_info = save_user_info(user)
                        print(user_info)
                        insert_check_user_info(user_info, phone_str, by_phone)
            else:
                log_register.logger.info(phone_str + "未注册------" + str(self.N) + "------" + str(peer_num))
                print(phone_str + "未注册------" + str(self.N) + "------" + str(peer_num))
                if get_info_from_check_user_by_phone(phone_str):
                    log_register.logger.error("已注册的却没检测出来...")
                    print("已注册的却没检测出来...")
                    print(datetime.datetime.now())
                    # exit(-1)
        except Exception as e:
            raise e


def task(login_phone, add_user, end):
    # loop = asyncio.new_event_loop()
    check = MyCheck()
    loop = asyncio.new_event_loop()
    try:
        loop.run_until_complete(check.set_client(login_phone))
    except Exception as e:
        print(e)
        log_register.logger.error(e)
        return

    phone_str = ''
    peer_num = 1

    Error = False
    rnum = 0

    # 随机获取两个已知的手机号
    count = get_the_count_of_check_user()
    index1 = random.randint(0, count - 1)
    index2 = random.randint(0, count - 1)
    friend_phone1 = get_the_phone_from_check_user_by_index(index1)
    friend_phone2 = get_the_phone_from_check_user_by_index(index2)
    log_register.logger.info("两个随机的已知手机号：" + friend_phone1 + "和" + friend_phone2)

    for i in range(len(add_user)):
        # 添加一个已注册的作为判断是否失效
        if i == 34:
            try:
                loop.run_until_complete(check.check(friend_phone1, peer_num))
                rnum += 1
                peer_num += 1
            except Exception as e:
                Error = True
                print(e)
                break
        elif i == 15:
            try:
                loop.run_until_complete(check.check(friend_phone2, peer_num))
                rnum += 1
                peer_num += 1
            except Exception as e:
                Error = True
                print(e)
                break
        else:
            # 防止添加一个已注册的作为判断是否失效漏掉测试手机号
            if 15 < i < 34:
                i -= 1
            phone_str = str(add_user[i])
            try:
                loop.run_until_complete(check.check(phone_str, peer_num))
                rnum += 1
                peer_num += 1
            except Exception as e:
                Error = True
                print(e)
                break
    if Error:
        with open("{}.txt".format(end), 'w') as f:
            f.write(phone_str)
    else:
        phone_str = str(int(phone_str) + 1)
        with open("{}.txt".format(end), 'w') as f:
            f.write(phone_str)
    check.client.disconnect()
    return rnum


def main_check(phone, end):
    add = []
    if not os.path.exists("{}.txt".format(end)):
        log_register.logger.error("{}.txt 文件不存在，请手动创建".format(end))
        exit()

    with open("{}.txt".format(end), "r") as f:
        start_phone = f.read()

    # 如果测试完了所有的号码段
    if start_phone > end:
        log_register.logger.info("所有号码段都测试完毕！")
        return

    login_phone = phone
    for i in range(35):
        add.append(str(int(start_phone) + i))

    task(login_phone, add, end)


if __name__ == '__main__':
    phone = "8617035274163"
    end = "85262999999"
    # start = "85262000000"
    # with open(end + ".txt", 'w') as f:
    #     f.write(start)
    main_check(phone, end)
