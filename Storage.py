import config
import os
import urllib


class Storage:
    def __init__(self):
        pass

    @staticmethod
    def recursive_walk(folder):
        dirs = []
        for root_dir, subdir_list, files_list in os.walk(folder):
            if subdir_list:
                for sub_dir in subdir_list:
                    dirs += Storage.recursive_walk(root_dir + os.sep + sub_dir)

            return dirs + [root_dir]

    @staticmethod
    def get_directories(user):
        #path = text.replace('saver save', '').lstrip().replace(' ', os.sep)
        path = config.DIR_TO_SAVE + os.sep + str(user.get_user_id())
        if not os.path.isdir(path):
            os.makedirs(path, 0755)

        exist_dirs = Storage.recursive_walk(path)
        response = ''
        for exist_dir in exist_dirs:
            if exist_dir != path:
                response += '"%s"<br>' % ' '.join(exist_dir.replace(path, '').split(os.sep)[1:])

        return response


    @staticmethod
    def save_tmp(message):
        wall = message['attachment']['wall']
        tmp_dir = os.sep.join([config.DIR_TO_SAVE, 'tmp', str(message['mid'])])
        if not os.path.isdir(tmp_dir):
            os.makedirs(tmp_dir, 0755)
        file_write = open(tmp_dir + os.sep + 'text', 'w')
        file_write.write(wall['text'].encode('utf-8'))
        file_write.close()

        index = 0
        for attach in wall['attachments']:
            if attach['type'].encode('utf-8') != 'photo':
                continue
            photo = attach['photo']
            if 'src_xbig' in photo:
                photo_url = photo['src_xbig'].encode('utf-8')
            elif 'src_big' in photo:
                photo_url = photo['src_big'].encode('utf-8')
            else:
                photo_url = photo['src'].encode('utf-8')
            img_filename = photo_url.split('/')[-1:][0]
            urllib.urlretrieve(photo_url, tmp_dir + os.sep + '%d_%s' % (index, img_filename))
            index += 1

        return tmp_dir