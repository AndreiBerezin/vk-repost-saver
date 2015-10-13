from vk.api import API, Session
from vk.mixins import AuthMixin
import os
import config


class ConnectionManager:
    _scope = 'messages, offline'

    def __init__(self):
        pass

    @staticmethod
    def get_connection(login, password):
        token_lock_filename = login + '.token'
        if os.path.isfile(token_lock_filename):
            file_read = open(token_lock_filename, 'r')
            access_token = file_read.read()
            file_read.close()
        else:
            auth = AuthMixin(
                app_id=config.VK_APP_ID,
                user_login=login,
                user_password=password,
                scope=ConnectionManager._scope
            )
            access_token, _ = auth.get_access_token()
            file_write = open(token_lock_filename, 'w')
            file_write.write(access_token)
            file_write.close()

        session = Session(access_token=access_token)
        vk_api = API(session, lang='ru')

        return vk_api