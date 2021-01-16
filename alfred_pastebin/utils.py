import json
import sys
from subprocess import Popen, PIPE

from alfred_pastebin.variables import DEFAULT_NAME


def return_result(result):
    json_str = json.dumps(result)
    sys.stdout.write(json_str)


def get_name_text(query):
    return query or DEFAULT_NAME


def save_workflow_variable(key, value):
    script = '''
        set bundleID to (system attribute "alfred_workflow_bundleid")

        tell application id "com.runningwithcrayons.Alfred"
            set configuration "%s" to value "%s" in workflow bundleID with exportable
        end tell
    ''' % (key, value)

    p = Popen(['osascript', '-'], stdin=PIPE, stdout=PIPE, stderr=PIPE, universal_newlines=True)
    p.communicate(script)
