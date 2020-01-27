class SendbeeException(Exception):
	"""Handle All Marine Traffic Exceptions"""


class SendbeeRequestApiException(SendbeeException):
	"""Handle Request Exceptions"""


class SendbeeFormatterException(SendbeeException):
	"""Handle Formatter Exceptions"""
