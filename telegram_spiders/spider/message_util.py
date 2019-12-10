import requests
from config import message_name, message_sid, message_password
import time

url = "http://api.xinheyz.com/api/do.php"


def login():
    '''
    登录信盒获取token
    :return:
    '''
    params = {
        "action": "loginIn",
        "name": message_name,
        "password": message_password
    }
    response = requests.get(url, params=params).text
    result = response.split("|")
    return result[0], result[1]


def get_phone(token, phone):
    params = {
        "action": "getPhone",
        "sid": message_sid,
        "token": token,
        "phone": phone
    }
    response = requests.get(url, params=params).text
    result = response.split("|")
    return result[0], result[1]


def get_message(token, phone):
    params = {
        "action": "getMessage",
        "sid": message_sid,
        "phone": phone,
        "token": token,
        "author": message_name
    }
    response = requests.get(url, params=params).text
    result = response.split("|")
    return result[0], result[1]


def get_code(phone):
    '''
    获取对应手机号的验证码
    :param phone:
    :return:
    '''
    try:
        login_status, token = login()
    except Exception as e:
        print(e)
        raise RuntimeError('{"error_code": 505, "msg": "信盒api登录失败..."}')
    phone_status, phone_ = get_phone(token, phone)
    if phone_status == '0':
        raise RuntimeError('{"error_code": 503, "msg": "无法获取该手机号..."}')
    message_status, message = get_message(token, phone_)

    try_num = 50
    while message_status == '0' and try_num > 0:
        print(message)
        time.sleep(3)
        message_status, message = get_message(token, phone)
        try_num -= 1

    if try_num <= 0:
        raise RuntimeError('{"error_code": 504, "msg": "获取验证码失败..."}')

    print("message: " + message)
    if message.startswith("【CMK】"):
        code = message.split("】")[1]
    elif message.startswith("[MTTO]"):
        code = message.split(": ")[1]
    else:
        code = message.split(": ")[1]

    print("code: " + code)
    return code


if __name__ == '__main__':
    def te():
        try:
            login_status, token = login()
        except Exception as e:
            print(e)
            raise RuntimeError('{"error_code": 505, "msg": "信盒api登录失败..."}')
    try:
        te()
    except Exception as e:
        print(e)
