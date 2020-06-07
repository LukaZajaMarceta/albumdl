import os
import configparser

config = configparser.ConfigParser()
path = os.path.dirname(os.path.realpath(__file__))

try:
    config.read_file(open(path + '/config.ini'))
except FileNotFoundError:
    config.read('config.ini')
    config.add_section('api')
    config.add_section('paths')


def get_default():
    music_folder = os.path.expanduser('~') + '/Music'
    albumdl_folder = music_folder + 'albumdl'
    if os.path.exists(albumdl_folder):
        return albumdl_folder
    elif os.path.exists(music_folder):
        return music_folder
    else:
        os.mkdir(albumdl_folder)
        return albumdl_folder


def set_default(new_path):
    if not os.path.exists(new_path):
        print('[SAVE DIRECTORY] specified directory does not exist, creating directory')
        os.mkdir(new_path)
        print('[SAVE DIRECTORY] {} folder created'.format(new_path))
    config.set('paths', 'save_folder', new_path)
    save()
    return None


def get_path():
    return config.get('paths', 'save_folder', fallback=get_default())


def get_key():
    if not config.has_option('api', 'key'):
        config.set('api', 'key', api_key_user_prompt())
    save()
    return config.get('api', 'key')


def set_key(s):
    print('[saving] setting api-key')
    config.set('api', 'key', s)


def save():
    with open(path + '/config.ini', 'w') as configfile:
        config.write(configfile)


def api_key_user_prompt():
    print("""This program requires youtube api-key to work, 
    refer to https://developers.google.com/youtube/v3/getting-started for setup
    This key will only be stored locally in config.ini file
    """)
    api_key = input("your api-key: ")
    return api_key
