from collections import namedtuple



RequestConst = namedtuple(
    'RequestConst', [
        'GET', 'POST', 'PUT', 'DELETE', 'PATH', 'QUERY', 'METHOD', 'TIMEOUT',
        'API_PATH', 'PROTOCOL', 'QUERY_PARAMETERS', 'DEFAULT_PARAMETERS',
        'BLOCK_NOTIFICATIONS', 'BLOCK_AUTOMATION'
    ]
)(
    'GET', 'POST', 'PUT', 'DELETE', 'path', 'query', 'method', 'timeout',
    'api_path', 'protocol', 'query_parameters', 'default_parameters',
    'block_notifications', 'block_automation'
)

ErrorConst = namedtuple(
    'ErrorConst', ['ERROR', 'UNRECOGNIZED_ERROR', 'DETAIL']
)('error', 'Unrecognized error', 'detail')

WarningConst = namedtuple(
    'WarningConst', ['WARNING', 'MESSAGE']
)('warning', '[Sendbee API] WARNING: ')

ResponseConst = namedtuple(
    'ResponseConst', [
        'RESPONSE', 'STATUS_CODE', 'RESPONSE_OBJECT', 'DEFAULT_ERROR_MESSAGE'
    ]
)(
    'response', 'status_code', 'response_object',
    {
        ErrorConst.ERROR: {
            ErrorConst.DETAIL: ErrorConst.UNRECOGNIZED_ERROR,
            'type': 'unrecognized_error'
        }
    }
)

ClientConst = namedtuple(
    'ClientConst', [
        'META', 'MODEL', 'MODELS', 'FORMATTER', 'DESCRIPTION'
    ]
)('meta', 'model', 'models', 'formatter', 'description')

FormatterConst = namedtuple(
    'FormatterConst', ['JSON', 'FORMATTED']
)('json', 'formatted')

TestConst = namedtuple('TestConst', ['FAKE_RESPONSE_PATH'])('fake_response_path')

ResponseCode = namedtuple(
    'ResponseCode', ['OK', 'NOT_FOUND', 'BAD_REQUEST']
)(200, 404, 400)

BoolConst = namedtuple('BoolConst', ['TRUE', 'FALSE'])('1', '0')

MiscConst = namedtuple(
    'MiscConst', ['FORMAT', 'PRINT_PARAMS']
)('format', 'print_params')

ResponseDataConst = namedtuple(
    'ResponseDataConst', ['DATA', 'META']
)('data', 'meta')

AutomationConst = namedtuple(
    'AutomationConst', ['TOGGLE_BOT']
)('toggle_bot')
