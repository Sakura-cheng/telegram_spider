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
from test import login


class MyCheck:
    '''
    通过添加好友的方式检测手机号是否注册
    如果注册则获取user信息
    '''

    def __init__(self):
        self.client = None

    async def set_client(self, login_phone):
        self.client = await login(login_phone)

    async def check(self, phone_str):
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
            users = result.users
            if len(users) > 0:
                print(phone_str + "已注册")
                for user in users:
                    # 保存到数据库
                    user_info = save_user_info(user)
                    print(user_info)
                    insert_check_user_info(user_info, phone_str, by_phone)
            else:
                print(phone_str + "未注册")
        except Exception as e:
            # print(e)
            raise e

    async def check_main(self):
        pass


def task(start, end, login_phone, try_count):
    check = MyCheck()
    loop = asyncio.new_event_loop()
    try:
        loop.run_until_complete(check.set_client(login_phone))
    except Exception as e:
        print(e)
        return

    # 从文件中查找上次停止时的phone
    check_end = int(end)
    if os.path.exists(start + '-' + end + '.txt'):
        with open(start + '-' + end + '.txt', 'r') as f:
            check_start = int(f.read())
    else:
        check_start = int(start)

    phone_str = ''
    Error = False
    for phone in range(check_start,
                       check_start + try_count if check_start + try_count < check_end + 1 else check_end + 1):
        phone_str = str(phone)
        try:
            loop.run_until_complete(check.check(phone_str))
        except Exception as e:
            Error = True
            print(e)
            break
    if Error:
        with open(start + '-' + end + '.txt', 'w') as f:
            f.write(phone_str)
    else:
        phone_str = str(int(phone_str) + 1)
        with open(start + '-' + end + '.txt', 'w') as f:
            f.write(phone_str)
    check.client.disconnect()


def main(start, end, login_phones, try_count, wait_seconds):
    restart_num = 0

    # 写文件记录起始位置
    if not os.path.exists(start + '-' + end + '.txt'):
        with open(start + '-' + end + '.txt', 'w') as f:
            f.write(start)

    # 读文件看做到哪了
    with open(start + '-' + end + '.txt', 'r') as f:
        phone_str = int(f.read())

    can_use_login_phone = ''

    while int(end) - int(phone_str) > 0:
        now_time = datetime.datetime.now()
        # 检查手机号是否可用
        for login_phone in login_phones:
            session, use_time = get_session(login_phone)
            if use_time is not None and now_time - use_time > datetime.timedelta(seconds=wait_seconds):
                can_use_login_phone = login_phone
                break
            if session is None:
                login_phones.remove(login_phone)

        if can_use_login_phone == '':
            print('暂无可用手机号，请等待一段时间...')
            time.sleep(10)
            continue
        else:
            print('找到一个可用手机号: ' + can_use_login_phone)
            t = Thread(target=task, args=(start, end, can_use_login_phone, try_count))
            # start_time = time.time()
            t.start()
            t.join()
            # end_time = time.time()
            # log_time.logger.info(end_time - start_time)
            update_session_time(can_use_login_phone, datetime.datetime.now())
            can_use_login_phone = ''

            with open(start + '-' + end + '.txt', 'r') as f:
                phone_str = int(f.read())

    print("process end")


def run():
    processes = []
    size = math.ceil((end - start + 1) / process_num)

    # fs = os.listdir(config.sessions_dir)
    # for f in fs:
    #     login_phones.append(f.split('_')[0])
    # size2 = len(login_phones) // process_num
    # 从数据库中获取手机号
    login_phones = []
    for phone in get_login_phones():
        login_phones.append(phone[0])

    size2 = len(login_phones) // process_num

    i = 0
    for phone in range(start, end + 1, size):
        phone_start_str = str(phone)
        phone_end_str = str(phone + size - 1) if (phone + size - 1) < end else str(end)

        p = Process(target=main,
                    args=(phone_start_str, phone_end_str, login_phones[i:i + size2], try_count, wait_seconds))
        print(phone_start_str, phone_end_str, login_phones[i:i + size2])
        processes.append(p)
        p.start()
        i += size2

    for p in processes:
        p.join()
    print("end")


if __name__ == '__main__':
    # parser = argparse.ArgumentParser(prog='telegramChecker',
    #                                  description="Check if the phone number is registered with telegram")
    # parser.add_argument(
    #     '-s', '--start', metavar='start_phone', dest='start',
    #     type=int, required=True,
    #     help="the start phone number"
    # )
    # parser.add_argument(
    #     '-e', '--end', metavar='end_phone', dest='end',
    #     type=int, required=True,
    #     help="the end phone number"
    # )
    # parser.add_argument(
    #     '-n', metavar='process_num', dest='process_num',
    #     default=1, type=int,
    #     help='the number of process, default=1'
    # )
    # parser.add_argument(
    #     '-t', metavar='try_count', dest='try_count',
    #     default=5, type=int,
    #     help='the number of API calls, default=5'
    # )
    # parser.add_argument(
    #     '-s', metavar='wait_seconds', dest='wait_seconds',
    #     default=60 * 60 * 24, type=int,
    #     help='the seconds to wait for API calls, default=60 * 60 * 24'
    # )
    # args = parser.parse_args()
    # start = args.start
    # end = args.end
    # process_num = args.process_num
    # try_count = args.try_count
    # wait_seconds = args.wait_seconds

    # print(start, end, process_num)

    start = 85366000000
    end = 85366999999
    process_num = 3
    try_count = 1
    wait_seconds = 60 * 60 * 24

    # start = 8615760572246
    # end = 8615760572247
    # process_num = 1
    # try_count = 50
    # wait_seconds = 300

    run()
