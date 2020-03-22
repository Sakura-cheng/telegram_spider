from telethon.tl.functions.contacts import ImportContactsRequest
from telethon.tl.types import InputPhoneContact
import asyncio
import time
from sql_util import insert_check_user_info, selcet_the_last_check_user
from save_util import save_user_info
import os
import sys

from config import message_token, check_start, check_end, check_base_phone
from message_util import get_phone_test, get_summary, add_black, cancel_all_recv, cancel_recv
from telegram import login


class Check:
    def __init__(self):
        self.client = None

    async def init(self, phone_logined):
        # '8617121240943'
        self.client = await login(phone_logined)

    async def check(self, phone_num):
        contact = InputPhoneContact(client_id=0, phone=phone_num, first_name="zhang{}",
                                    last_name="san")
        try:
            result = await self.client(ImportContactsRequest(contacts=[contact]))
            users = result.users
            if len(users) > 0:
                print(phone_num + "已注册")
                # code, r = cancel_recv(message_token, phone_num[2:])
                # print("释放", code, r)
                return True
            else:
                print(phone_num + "未注册")
                # add_black(message_token, phone_num[2:])
                return False
        except Exception as e:
            print(e)

    async def just_check(self, phone_num):
        contact = InputPhoneContact(client_id=0, phone=phone_num, first_name="zhang{}",
                                    last_name="san")
        try:
            result = await self.client(ImportContactsRequest(contacts=[contact]))
            # print(phone_num)
            # print(result.stringify())
            users = result.users
            if len(users) > 0:
                print(phone_num + "已注册")

                for user in users:
                    # 保存到数据库
                    user_info = save_user_info(user)
                    print(user_info)
                    insert_check_user_info(user_info, phone_num)
            else:
                print(phone_num + "未注册")
        except Exception as e:
            print(e)
            raise RuntimeError('检查api失败...')


def check_main(phone_logined, phone_num):
    c = Check()
    loop = asyncio.get_event_loop()
    loop.run_until_complete(c.init(phone_logined))
    get_future = asyncio.ensure_future(c.check(phone_num))
    loop.run_until_complete(get_future)
    return get_future.result()


def just_check_main(logined_phone):
    c = Check()
    loop = asyncio.get_event_loop()
    loop.run_until_complete(c.init(logined_phone))

    # 香港
    total_num = 0
    base_phone = check_base_phone

    # 从文件中查找上次停止时的phone
    if os.path.exists(base_phone + '.txt'):
        with open(base_phone + '.txt', 'r') as f:
            start = int(f.read())
    else:
        start = check_start

    start_time = time.time()
    for i in range(start, check_end):
        phone_str = str(i)
        # phone_str = '8618580391160'
        print('------开始检测' + phone_str + '是否注册------')
        # time.sleep(3)
        try:
            loop.run_until_complete(c.just_check(phone_str))
            total_num += 1
            print('------' + str(total_num) + '------')
        except Exception as e:
            print(e)
            # 记录此时的phone
            with open(base_phone + '.txt', 'w') as f:
                f.write(phone_str)
            break
    end_time = time.time()
    print(end_time - start_time)


if __name__ == '__main__':
    just_check_main(sys.argv[1])

    # c = Check()
    # loop = asyncio.get_event_loop()
    # loop.run_until_complete(c.init('8615201615409'))
    # loop.run_until_complete(c.just_check('8619981451265'))


    # just_check_main('8617121240943')
    #'8618580391160''8617121240943'
    # if len(sys.argv) == 2:
    #     just_check_main(sys.argv[1])
    # else:
    #     just_check_main('8618580391160')

'''
    with open('phones.txt', 'r') as f:
        phones = f.readlines()

    total_num = 0
    for phone in phones:
        phone = phone[:-1]
        for i in range(10000):
            i_str = str(i)
            num = 4 - len(i_str)
            phone_str = '86' + str(phone) + '0' * num + i_str
            print('------开始检测' + phone_str + '是否注册------')
            time.sleep(3)
            try:
                loop.run_until_complete(c.just_check(phone_str))
                total_num += 1
                print('------' + str(total_num) + '------')
            except RuntimeError as e:
                print(e)
            except Exception as e:
                print(e)'''

# status, phone_ = cancel_all_recv(message_token)
# print(status, phone_)
# get_summary(message_token)

# for i in range(2):
#    status, phone_ = get_phone_test(message_token)
#    print(status, phone_)
#   loop.run_until_complete(c.check('86' + str(phone_)))
#    time.sleep(3)
