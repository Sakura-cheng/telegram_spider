import requests
from config import message_name, message_sid, message_password
import time

url = "http://api.xinheyz.com/api/do.php"


def login():
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
    login_status, token = login()
    phone_status, phone_ = get_phone(token, phone)
    message_status, message = get_message(token, phone_)

    try_num = 50
    while message_status == '0' and try_num > 0:
        print(message)
        time.sleep(3)
        message_status, message = get_message(token, phone)
        try_num -= 1

    print("message: " + message)
    if message.startswith("[MTTO]"):
        code = message.split(": ")[1]
    elif message.startswith("【CMK】"):
        code = message.split("】")[1]
    print("code: " + code)
    return code


if __name__ == '__main__':
    get_code(16510456792)
