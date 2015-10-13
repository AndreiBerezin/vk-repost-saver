import config

import os
import time
from ConnectionManager import ConnectionManager
from User import User
from Dialog import Dialog


def main():
    if not os.path.isdir(config.DIR_TO_SAVE):
        print 'save dir does not exist'
        return 1

    users = {}
    for login in config.VK_USERS:
        try:
            users[login] = User(ConnectionManager.get_connection(login=login, password=config.VK_USERS[login]))
        except Exception as e:  # todo:use specific exception
            print 'no connect to vk.com for ' + login
            return 2

    while True:
        time.sleep(config.CHECK_PERIOD)

        for login in users:
            user = users[login]
            Dialog.process(user=user)

            #response_message_id =
            #if response_message_id:
            #    user.set_last_message_id(response_message_id)

main()