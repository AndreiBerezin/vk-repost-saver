import time


class Dialog:
    _saver_response_prefix = 'saver response'

    def __init__(self):
        pass

    @staticmethod
    def process(user):
        try:
            message = user.get_last_message()
            if not message:
                return False
            if not message['attachment']:
                return False
            text = message['body'].encode('utf-8')
            if text.find(Dialog._saver_response_prefix) != -1:
                return False
        except Exception as e:  # todo:use specific exception
            return False

        response_message_text = Dialog._read(message)
        response_message_id = Dialog._send_response(user=user, message_text=response_message_text)
        user.set_last_message_id(response_message_id)

        return True

    @staticmethod
    def _read(message):
        try:
            text = message['body'].encode('utf-8')
            if text.find('save') != -1:
                '''
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
                '''
                back_message = ''
            elif text.find('pdf') != -1:
                back_message = ''
            elif text.find('link') != -1:
                back_message = ''
            else:
                back_message = 'usage:<br>' \
                               '"save {path}" - save repost in {path}<br>' \
                               '"pdf {path}" - return pdf for repost from {path}<br>' \
                               '"link" - return dropbox link to root dir<br>'
        except Exception as e:  # todo:use specific exception
            back_message = e.message

        return back_message

    @staticmethod
    def _send_response(user, message_text):
        now = time.strftime('%H:%M:%S %d.%m.%Y', time.gmtime())

        return user.get_connection().messages.send(
            user_id=user.get_user_id(),
            message='%s (%s):<br>%s' % (Dialog._saver_response_prefix, now, message_text)
        )