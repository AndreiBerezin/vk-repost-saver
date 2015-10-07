import config
from vk.api import API, Session
from vk.mixins import AuthMixin
import os

def main():
    auth = AuthMixin(app_id=config.VK_APP_ID, user_login=config.VK_LOGIN, user_password=config.VK_PASSWORD)
    #auth = InteractiveMixin()
    #auth_session = APISession(app_id=config.VK_APP_ID, user_login=config.VK_LOGIN, user_password=config.VK_PASSWORD)
    access_token, _ = auth.get_access_token()
    session = Session(access_token=access_token)
    vk_api = API(session, lang='ru')
    print vk_api.users.get(user_ids=1)


main()