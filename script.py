import json
import os
import sys
import urllib


API_ENDPOINT = 'https://pastebin.com/api/'
LANGUAGE_FILE = 'language.json'

# variables
# (more info: https://pastebin.com/doc_api)
# (change these in workflow variables)
DEFAULT_NAME = os.environ.get('DEFAULT_NAME', 'Untitled')
EXPIRE_DATE = os.environ.get('EXPIRE_DATE', '1W')  # see: https://pastebin.com/doc_api#6
DEFAULT_PERMISSION = os.environ.get('DEFAULT_PERMISSION', 'public')
CMD_PERMISSION = os.environ.get('CMD_PERMISSION', 'unlisted')
API_DEV_KEY = os.environ.get('API_DEV_KEY')
API_USER_KEY = os.environ.get('API_USER_KEY')


# load language list
with open(LANGUAGE_FILE, 'r') as f:
	LANGUAGES = json.load(f)


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
		raise ValueError(query)

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
	raise ValueError

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
	if api_user_key is not None:
		payload.update({'api_user_key': api_user_key})

	return urllib.urlopen(API_ENDPOINT + 'api_post.php', data=urllib.urlencode(payload))


# get argv
command = sys.argv[1]
name_query = sys.argv[2] if len(sys.argv) > 2 else None
language_query = sys.argv[3] if len(sys.argv) > 3 else None


# run command
if command == 'filter':
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
	except ValueError:
		result = {
			'items': [
				{
					'title': 'Invalid language!',
					'subtitle': 'Please check your input'
				}
			]
		}

	return_result(result)

elif command == 'paste':
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
