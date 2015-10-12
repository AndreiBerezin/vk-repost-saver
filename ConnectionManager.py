from vk.api import API, Session
from vk.mixins import AuthMixin
import os
import config


class ConnectionManager:
    _connections = {}
    _scope = 'messages, offline'

    def __init__(self):
        pass

    def add_connection(self, login, password):
        if login in self._connections:
            return
        self._connections[login] = self._connect(login, password)

    def _connect(self, login, password):
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
                scope=self._scope
            )
            access_token, _ = auth.get_access_token()
            file_write = open(token_lock_filename, 'w')
            file_write.write(access_token)
            file_write.close()

        session = Session(access_token=access_token)
        vk_api = API(session, lang='ru')

        return vk_api

    def get_connection(self, login):
        if login not in self._connections:
            raise Exception('connection not found')

        return self._connections[login]

    def get_connections(self):
        return self._connections