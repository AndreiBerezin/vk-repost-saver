class User:
    _connection = False
    _last_message_id = 0
    _user_id = 0

    def __init__(self, connection):
        if not connection:
            raise Exception('connection must be init')
        self._connection = connection
        user_info = connection.users.get()
        self._user_id = user_info[0]['uid']

    def get_connection(self):
        return self._connection

    def set_last_message_id(self, message_id):
        self._last_message_id = message_id

    def get_user_id(self):
        return self._user_id

    def get_last_message(self):
        messages_history = self._connection.messages.getHistory(user_id=self._user_id, count=1)
        message = messages_history[1]
        message_id = message['mid']
        if self._last_message_id == message_id:
            return False
        self.set_last_message_id(message_id)

        return message
        '''
        response_message_id = process_received_message(vk_api=vk_api, uid=uid, message=messageArr)
        if response_message_id == False:
            last_message_id = message_id
        else:
            last_message_id = response_message_id
'''

