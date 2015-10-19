# -*- coding: utf-8 -*-
import config


class Translator:
    _texts = {
        'en': {
            'save': 'save',
            'pdf': 'pdf',
            'link': 'link',
            'usage': 'usage:<br>'
                    '"save" - save repost in selected path<br>'
                    '"pdf" - return pdf for repost from path<br>'
                    '"link" - return dropbox link to root dir<br>',
            'saverResponse': 'saver response',
            'chooseDir': 'Choose dir for save'
        },
        'ru': {
            'save': 'сохранить',
            'pdf': 'pdf',
            'link': 'ссылка',
            'usage': 'использование:<br>'
                    '"сохранить" - сохраняет репост в выбранную папку<br>'
                    '"pdf" - возвращает сформированный pdf из папки<br>'
                    '"link" - возвращает ссылку на dropbox папку<br>',
            'saverResponse': 'ответ',
            'chooseDir': 'Выберите папку для сохранения'
        }
    }

    def __init__(self):
        pass

    @staticmethod
    def translate(text):
        locale = config.LOCALE
        if locale not in Translator._texts:
            raise Exception('%s locale is not exists' % locale)  # todo:use specific exception

        texts = Translator._texts[locale]
        if text not in texts:
            raise Exception('translated text not found for %s' % text)  # todo:use specific exception

        return texts[text]