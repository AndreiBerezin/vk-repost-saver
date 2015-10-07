import config
from vk.api import API, Session
from vk.mixins import AuthMixin
import os
import time


def connect():
    token_lock_filename = 'token.lock'
    if os.path.isfile(token_lock_filename):
        file_read = open(token_lock_filename, 'r')
        access_token = file_read.read()
        file_read.close()
    else:
        auth = AuthMixin(
            app_id=config.VK_APP_ID,
            user_login=config.VK_LOGIN,
            user_password=config.VK_PASSWORD,
            scope='messages, offline'
        )
        access_token, _ = auth.get_access_token()
        file_write = open(token_lock_filename, 'w')
        file_write.write(access_token)
        file_write.close()

    session = Session(access_token=access_token)
    vk_api = API(session, lang='ru')

    return vk_api


def parse_message(message):
    return []


def save_content(content):
    pass


def main():
    try:
        vk_api = connect()
    except Exception:  # todo:use specific exception
        print 'no connect to vk.com'
        return 1


    user_info = vk_api.users.get()
    uid = user_info[0]['uid']
    last_message_id = 0
    while True:
        time.sleep(1)

        messagesHistory = vk_api.messages.getHistory(user_id=uid, count=1)
        messageArr = messagesHistory[1]
        message_id = messageArr['mid']
        if last_message_id == message_id:
            continue

        if 'attachment' not in messageArr or messageArr['attachment']['type'].encode('utf-8') != 'wall':
            last_message_id = message_id
            continue

        try:
            content = parse_message(messageArr)
        except Exception:  # todo:use specific exception
            content = []
            print 'unable to parse message %s' % message_id

        try:
            save_content(content)
        except Exception:  # todo:use specific exception
            print 'unable to save content for message %s' % message_id

        back_message = 'message %s processed and deleted' % message_id
        last_message_id = vk_api.messages.send(user_id=uid, message=back_message)
        vk_api.messages.delete(message_ids=message_id)

main()