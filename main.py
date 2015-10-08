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


def process_received_message(vk_api, uid, message):
    try:
        text = message['body'].encode('utf-8')
        if text.find('saver') == -1 or text.find('saver response') != -1:
            return False

        if text.find('saver save') != -1:
            path = text.replace('saver save', '').lstrip().replace(' ', os.sep)
            path = config.DIR_TO_SAVE + os.sep + path
            if not os.path.isdir(path):
                raise Exception('path for save not found')
            #for dirName, subdirList, fileList in os.walk(config.DIR_TO_SAVE):
            #    print('Found directory: %s' % dirName)
            #    for fname in fileList:
            #        print('\t%s' % fname)

            if 'attachment' not in message or message['attachment']['type'].encode('utf-8') != 'wall':
                raise Exception('attachment for message not found')

            content = parse_message(message['attachment'])
            save_content(content)
            back_message = ''
        elif text.find('saver pdf') != -1:
            back_message = ''
        elif text.find('saver link') != -1:
            back_message = ''
        else:
            back_message = 'usage:<br>' \
                           '"saver save {path}" - save repost in {path}<br>' \
                           '"saver pdf {path}" - return pdf for repost from {path}<br>' \
                           '"saver link" - return dropbox link to root dir<br>'
    except Exception as e:  # todo:use specific exception
        back_message = e.message

    now = time.strftime('%H:%M:%S %d.%m.%Y', time.gmtime())
    return vk_api.messages.send(user_id=uid, message='saver response (%s):<br>%s' % (now, back_message))


def parse_message(message):
    return []


def save_content(content):
    pass


def main():
    if not os.path.isdir(config.DIR_TO_SAVE):
        print 'save dir does not exist'
        return 1

    try:
        vk_api = connect()
    except Exception:  # todo:use specific exception
        print 'no connect to vk.com'
        return 2


    user_info = vk_api.users.get()
    uid = user_info[0]['uid']
    last_message_id = 0
    while True:
        time.sleep(config.CHECK_PERIOD)

        messagesHistory = vk_api.messages.getHistory(user_id=uid, count=1)
        messageArr = messagesHistory[1]
        message_id = messageArr['mid']
        if last_message_id == message_id:
            continue

        response_message_id = process_received_message(vk_api=vk_api, uid=uid, message=messageArr)
        if response_message_id == False:
            last_message_id = message_id
        else:
            last_message_id = response_message_id


main()