import os
from config import sessions_dir
import json
import pytz
from sql_util import *
from telethon.tl.types import UserStatusOnline, UserStatusOffline, UserProfilePhoto, Message


def session_file_exists(phone):
    '''
    判断session文件是否存在
    :param phone:
    :return:
    '''
    return os.path.exists(sessions_dir + str(phone) + "_session.txt")


def save_session_file(phone, session):
    '''
    保存session文件
    :param phone:
    :param session:
    :return:
    '''
    with open(sessions_dir + str(phone) + "_session.txt", 'w') as f:
        f.write(session)


def read_session_file(phone):
    '''
    读取session文件
    :param phone:
    :return:
    '''
    with open(sessions_dir + str(phone) + "_session.txt", 'r') as f:
        session = f.read()
    return session


def save_user_info(user):
    '''
    保存user信息
    :param user:
    :return:
    '''
    user_info = {
        "id": user.id,
        "phone": user.phone,
        "first_name": user.first_name,
        "last_name": user.last_name,
        "username": user.username,
        "bot": user.bot,
        "photo": user.photo,
        "status": user.status
    }

    # 判断是否有头像
    photo = user_info["photo"]
    if photo:
        if isinstance(photo, UserProfilePhoto):
            user_info["photo"] = {
                "photo_id": photo.photo_id,
                "photo_small": {
                    "volume_id": photo.photo_small.volume_id,
                    "local_id": photo.photo_small.local_id,
                },
                "photo_big": {
                    "volume_id": photo.photo_big.volume_id,
                    "local_id": photo.photo_big.local_id,
                },
                "dc_id": photo.dc_id
            }
        else:
            user_info["photo"] = None

    # 判断status是否为空
    status = user_info["status"]
    if status:
        if isinstance(status, UserStatusOffline):
            user_info["status"] = {
                "was_online": change_timezone(status.was_online)
            }
        elif isinstance(status, UserStatusOnline):
            user_info["status"] = {
                "expires": change_timezone(status.expires)
            }
        else:
            user_info["status"] = None

    # return json.dumps(user_info, ensure_ascii=False)
    return user_info


def save_channel_info(channel):
    channel_info = {
        "id": channel.id,
        "title": channel.title,
        "username": channel.username,
        "participants_count": channel.participants_count
    }
    # return json.dumps(channel_info, ensure_ascii=False)
    return channel_info


def save_group_info(group):
    group_info = {
        "id": group.id,
        "title": group.title,
        "participants_count": group.participants_count
    }
    # return json.dumps(group_info, ensure_ascii=False)
    return group_info


def save_message_info(message):
    message_info = {
        "id": message.id,
        "message": message.message,
        "date": change_timezone(message.date),
        "from_id": message.from_id
    }
    # return json.dumps(message_info, ensure_ascii=False)
    return message_info


def save_authorization_info(authorization):
    authorization_info = {
        "hash": authorization.hash,
        "device_model": authorization.device_model,
        "platform": authorization.platform,
        "system_version": authorization.system_version,
        "app_name": authorization.app_name,
        "app_version": authorization.app_version,
        "date_created": change_timezone(authorization.date_created),
        "date_active": change_timezone(authorization.date_active),
        "ip": authorization.ip,
        "country": authorization.country,
        "region": authorization.region,
        "official_app": authorization.official_app
    }
    # return json.dumps(authorization_info, ensure_ascii=False)
    return authorization_info


async def get_participants(client, entity):
    participants = await client.get_participants(entity)
    participants_count = len(participants)
    participant_list = []
    print("共有" + str(participants_count) + "名成员")
    for participant in participants:
        participant_info = save_user_info(participant)
        print(participant_info)
        participant_list.append(participant_info)
    return participant_list


async def get_messages(client, entity):
    print("历史消息...")
    messages = await client.get_messages(entity)
    message_list = []
    for message in messages:
        if isinstance(message, Message):
            message_info = save_message_info(message)
            print(message_info)
            message_list.append(message_info)
    return message_list


def change_timezone(datetime):
    return datetime.astimezone(pytz.timezone('Asia/Shanghai')).strftime("%Y-%m-%d %H:%M:%S")


if __name__ == '__main__':
    pass
