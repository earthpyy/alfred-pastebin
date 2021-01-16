import json
import os


API_ENDPOINT = 'https://pastebin.com/api/'
LANGUAGE_FILE = 'language.json'

# variables
# (more info: https://pastebin.com/doc_api)
# (change these in workflow variables)
DEFAULT_NAME = os.environ.get('DEFAULT_NAME', 'Untitled')
# see: https://pastebin.com/doc_api#6
EXPIRE_DATE = os.environ.get('EXPIRE_DATE', '1W')
DEFAULT_PERMISSION = os.environ.get('DEFAULT_PERMISSION', 'public')
CMD_PERMISSION = os.environ.get('CMD_PERMISSION', 'unlisted')
API_DEV_KEY = os.environ.get('API_DEV_KEY')
API_USER_KEY = os.environ.get('API_USER_KEY')


# load language list
with open(LANGUAGE_FILE, 'r') as f:
    LANGUAGES = json.load(f)
