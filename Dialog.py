import time
import os
from Storage import Storage
from Translator import Translator


class Dialog:
    _saver_response_prefix = Translator.translate('saverResponse')
    _waiting_input_save = 'input.save'
    _waiting_input_pdf = 'input.pdf'

    def __init__(self):
        pass

    @staticmethod
    def process(user):
        try:
            message = user.get_last_message()
            if not message:
                return False

            text = message['body'].encode('utf-8')
            if text.find(Dialog._saver_response_prefix) != -1:
                return False

            response = Dialog._read(user=user, message=message)
            if not response:
                return False
            response_message_id = Dialog._send_response(user=user, message_text=response)
            user.set_last_message_id(response_message_id)

            return True
        except Exception as e:  # todo:use specific exception
            return False

    @staticmethod
    def _read(user, message):
        text = message['body'].encode('utf-8')
        lower_text = text.lower()

        if lower_text == Translator.translate('save'):
            if not message['attachment'] or message['attachment']['type'].encode('utf-8') != 'wall':
                return False
            tmp_dir = Storage.save_tmp(message=message)
            Dialog._start_waiting_input(user, Dialog._waiting_input_save, tmp_dir)
            back_message = '%s:<br>%s' % (Translator.translate('chooseDir'), Storage.get_directories(user=user))
        elif lower_text == Translator.translate('pdf'):
            back_message = ''
        elif lower_text == Translator.translate('link'):
            back_message = ''
        elif Dialog._is_waiting_input(user, Dialog._waiting_input_save):
            back_message = ''
        elif Dialog._is_waiting_input(user, Dialog._waiting_input_pdf):
            back_message = ''
        else:
            back_message = Translator.translate('usage')

        return back_message

    @staticmethod
    def _send_response(user, message_text):
        now = time.strftime('%H:%M:%S %d.%m.%Y', time.localtime())

        return user.get_connection().messages.send(
            user_id=user.get_user_id(),
            message='%s (%s):<br>%s' % (Dialog._saver_response_prefix, now, message_text)
        )


    @staticmethod
    def _start_waiting_input(user, prefix, info):
        filename = '%s.%s' % (user.get_user_id(), prefix)
        file_write = open(filename, 'w')
        file_write.write(info)
        file_write.close()

    @staticmethod
    def _is_waiting_input(user, prefix):
        filename = '%s.%s' % (user.get_user_id(), prefix)
        return os.path.isfile(filename)

    @staticmethod
    def _get_waiting_input(user, prefix):
        filename = '%s.%s' % (user.get_user_id(), prefix)
        file_read = open(filename, 'r')
        info = file_read.read()
        file_read.close()
        
        return info

    @staticmethod
    def _stop_waiting_input(user, prefix):
        filename = '%s.%s' % (user.get_user_id(), prefix)
        os.remove(filename)