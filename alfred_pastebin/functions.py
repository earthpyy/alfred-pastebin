import sys
import urllib

from alfred_pastebin import exceptions
from alfred_pastebin.variables import *


# functions
def return_result(result):
    json_str = json.dumps(result)
    sys.stdout.write(json_str)

def get_name_text(query):
    return DEFAULT_NAME if query is None else query

def get_language_text(query):
    if query is None:
        return 'None'

    language_name = LANGUAGES.get(query, None)
    if language_name is None:
        raise exceptions.InvalidLanguage(query)

    return language_name

def get_subtitle(name_query, language_query, modified=False):
    name = get_name_text(name_query)
    language = get_language_text(language_query)
    modified_text = ' (' + CMD_PERMISSION + ')' if modified else ''

    return 'Name: ' + name + ', Language: ' + language + modified_text

# see: https://pastebin.com/doc_api#7
def get_permission_code(permission):
    if permission == 'public':
        return 0
    elif permission == 'unlisted':
        return 1
    elif permission == 'private':
        return 2
    raise exceptions.InvalidPermission(permission)

def create_paste(code, name=DEFAULT_NAME, language=None, permission=DEFAULT_PERMISSION, api_user_key=None):
    payload = {
        'api_dev_key': API_DEV_KEY,
        'api_option': 'paste',
        'api_paste_code': code,
        'api_paste_private': get_permission_code(permission),
        'api_paste_expire_date': EXPIRE_DATE
    }

    if name is not None:
        payload.update({'api_paste_name': name})
    if language is not None:
        payload.update({'api_paste_format': language})
    if api_user_key:
        payload.update({'api_user_key': api_user_key})

    return urllib.urlopen(API_ENDPOINT + 'api_post.php', data=urllib.urlencode(payload))


def get_filter_result():
    # get argv
    name_query = sys.argv[2] if len(sys.argv) > 2 else None
    language_query = sys.argv[3] if len(sys.argv) > 3 else None

    # check for API keys
    if not API_DEV_KEY:
        result = {
            'items': [
                {
                    'title': 'No API_DEV_KEY!',
                    'subtitle': 'Please check your workflow variable.'
                }
            ]
        }
        return_result(result)

    elif not API_USER_KEY:
        result = {
            'items': [
                {
                    'title': 'No API_USER_KEY!',
                    'subtitle': 'Please check workflow variable.'
                }
            ]
        }
        return_result(result)

    else:
        try:
            result = {
                'items': [
                    {
                        'title': 'Create a new paste from clipboard',
                        'subtitle': get_subtitle(name_query, language_query),
                        'arg': ' '.join(sys.argv[2:]),
                        'variables': {
                            'permission': DEFAULT_PERMISSION,
                            'name': name_query,
                            'language': language_query
                        },
                        'mods': {
                            'cmd': {
                                'subtitle': get_subtitle(name_query, language_query, modified=True),
                                'variables': {
                                    'permission': CMD_PERMISSION
                                }
                            }
                        }
                    }
                ]
            }
        except exceptions.InvalidLanguage as e:
            result = {
                'items': [
                    {
                        'title': 'Invalid language `%s`!' % e,
                        'subtitle': 'Please check your input, you can leave it empty if you not sure.'
                    }
                ]
            }
        except exceptions.InvalidPermission as e:
            result = {
                'items': [
                    {
                        'title': 'Invalid permission `%s`!' % e,
                        'subtitle': 'Please check your workflow variable.'
                    }
                ]
            }

        return_result(result)


def get_paste_result():
    clipboard = os.environ.get('clipboard', '')
    name = os.environ.get('name', DEFAULT_NAME)
    language = os.environ.get('language', None)
    permission = os.environ.get('permission', DEFAULT_PERMISSION)

    response = create_paste(
        clipboard,
        name=name,
        language=language,
        permission=permission,
        api_user_key=API_USER_KEY
    )

    sys.stdout.write(response.read() if response else '')
