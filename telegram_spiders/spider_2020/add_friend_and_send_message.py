import asyncio
from telethon.tl.functions.contacts import ImportContactsRequest
from telethon.tl.functions.channels import JoinChannelRequest
from telethon.tl.types import InputPhoneContact
from telethon.tl.types import Channel, User

from test import login

'''
add some friends and send some messages to pretend to be a real user.
'''


async def add_friends(client, phone_str):
    me = await client.get_me()
    by_phone = me.phone
    contact = InputPhoneContact(client_id=0, phone=phone_str, first_name=phone_str,
                                last_name="test")
    try:
        result = await client(ImportContactsRequest(contacts=[contact]))
    except Exception as e:
        raise e


async def send_messages(client, entity, message):
    try:
        await client.send_message(entity, message)
    except Exception as e:
        raise e


async def add_channel(client, entity):
    try:
        result = await client(JoinChannelRequest(entity))
        print(result.stringify())
    except Exception as e:
        raise e


async def just_test():
    phone = input('phone...')
    print(phone)
    client = await login(phone)
    await add_friends(client, phone_str="8617121240943")
    await add_channel(client, entity="mypublicchannel3a")

    friends = []
    channels = []
    print("获得会话列表信息...")
    dialogs = await client.get_dialogs()
    me = await client.get_me()
    for dialog in dialogs:
        entity = dialog.entity
        # 是User
        if isinstance(entity, User):
            print("私聊会话...")
            friends.append(entity)

        # 是Channel
        elif isinstance(entity, Channel):
            channels.append(entity)

    for f in friends:
        await send_messages(client, entity=f, message="test")
    for c in channels:
        await send_messages(client, entity=c, message="test")


if __name__ == '__main__':
    loop = asyncio.get_event_loop()
    try:
        loop.run_until_complete(just_test())
        # loop.run_until_complete(register(phone))
    except Exception as e:
        print(e)
