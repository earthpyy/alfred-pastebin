import sys

from alfred_pastebin.functions import get_filter_result, get_paste_result


command = sys.argv[1]

# run command
if command == 'filter':
    get_filter_result()

elif command == 'paste':
    get_paste_result()
