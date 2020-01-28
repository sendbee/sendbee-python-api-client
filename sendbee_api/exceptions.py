class SendbeeException(Exception):
	"""Handle All Sendbee Exceptions"""


class SendbeeRequestApiException(SendbeeException):
	"""Handle Request Exceptions"""


class SendbeeFormatterException(SendbeeException):
	"""Handle Formatter Exceptions"""
