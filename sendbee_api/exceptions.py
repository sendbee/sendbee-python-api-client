class SendbeeException(Exception):
	"""Handle All Sendbee Exceptions"""

	def __init__(self, *args, **kwargs):
		self.response = kwargs.get('response')


class SendbeeRequestApiException(SendbeeException):
	"""Handle Request Exceptions"""


class SendbeeFormatterException(SendbeeException):
	"""Handle Formatter Exceptions"""


class PaginationException(SendbeeException):
	"""Handle Pagination Exceptions"""
