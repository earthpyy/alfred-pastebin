import json
import os
import sys
import urllib


# variables (more info: https://pastebin.com/api)
API_DEV_KEY = '***REMOVED***'
API_ENDPOINT = 'https://pastebin.com/api/'
LANGUAGE_FILE = 'language.json'
DEFAULT_PERMISSION = 'public'
CMD_PERMISSION = 'unlisted'
DEFAULT_EXPIRE_DATE = '1W'  # see: https://pastebin.com/api#6


# load language list
with open(LANGUAGE_FILE, 'r') as f:
	LANGUAGES = json.load(f)


# functions
def return_result(result):
    json_str = json.dumps(result)
    sys.stdout.write(json_str)

def get_language_text(query):
	if query is None:
		return 'No language specified'

	language_name = LANGUAGES.get(query, None)
	if language_name is None:
		raise ValueError(query)

	return 'Language: ' + language_name

# see: https://pastebin.com/api#7
def get_permission_code(permission):
	if permission == 'public':
		return 0
	elif permission == 'unlisted':
		return 1
	elif permission == 'private':
		return 2
	raise ValueError

def create_paste(code, language=None, permission=DEFAULT_PERMISSION, user_key=None):
	payload = {
		'api_dev_key': API_DEV_KEY,
		'api_option': 'paste',
		'api_paste_code': code,
		'api_paste_private': get_permission_code(permission),
		'api_paste_expire_date': os.environ.get('EXPIRE_DATE', DEFAULT_EXPIRE_DATE)
	}

	if language is not None:
		payload.update({'api_paste_format': language})
	if user is not None:
		payload.update({'api_user_key': user_key})

	return urllib.urlopen(API_ENDPOINT + 'api_post.php', data=urllib.urlencode(payload))


# get argv
command = sys.argv[1]
language_query = sys.argv[2] if len(sys.argv) > 2 else None


# run command
if command == 'filter':
	try:
		language_name = get_language_text(language_query)

		result = {
			'items': [
				{
					'title': 'Create a new paste from clipboard',
					'subtitle': language_name,
					'arg': ' '.join(sys.argv[2:]),
					'variables': {
						'permission': DEFAULT_PERMISSION,
						'language': language_query
					},
					'mods': {
						'cmd': {
							'subtitle': language_name + ' (unlisted)',
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
	user_key = os.environ.get('USER_KEY', None)

	response = create_paste(
		clipboard,
		language=os.environ.get('language', None),
		permission=os.environ.get('permission', DEFAULT_PERMISSION),
		user_key=user_key
	)

	sys.stdout.write(response.read())
