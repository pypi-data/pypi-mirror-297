import inspect

import requests
from requests.auth import HTTPBasicAuth

from octopus_common.config import octopus_config
from octopus_common.model.LogRecord import LogRecord
from octopus_common.util.envirement_utils import get_client_code, get_password


def log(level, message, *tag_pairs):
    stack = inspect.stack()
    # [0]是当前方法, [1]是当前调用者, [2]是上一层调用者
    caller_frame = stack[2]
    filename = caller_frame.filename
    method_name = caller_frame.function
    line_number = caller_frame.lineno
    source = {
        "methodName": method_name,
        "filename": filename,
        "lineNumber": line_number,
        "nativeMethod": False
    }
    log_record = LogRecord(level, source, message, tag_pairs)
    requests.get(octopus_config.INTEGRATION_HOST,
                 json=log_record.__dict__,
                 auth=HTTPBasicAuth(get_client_code(), get_password()))


def info(message='', thrown=None, *tag_pairs):
    log(LogRecord.Level.I, message, thrown, *tag_pairs)


def warn(message='', thrown=None, *tag_pairs):
    log(LogRecord.Level.W, message, thrown, *tag_pairs)


def error(message='', thrown=None, *tag_pairs):
    log(LogRecord.Level.E, message, thrown, *tag_pairs)
