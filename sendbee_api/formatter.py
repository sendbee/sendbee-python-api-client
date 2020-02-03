import ujson

from abc import ABCMeta, abstractmethod

from sendbee_api import constants


class Formatter(metaclass=ABCMeta):
    """Abstract formatter class."""

    def __init__(self, response):
        self._response = response

    @abstractmethod
    def _format_data(self, data):
        """Format method in formatter classes."""

        return data

    @abstractmethod
    def _format_meta(self, data):
        """Format method in formatter classes."""

        return data

    @abstractmethod
    def _format_warning(self, data):
        """Format method in formatter classes."""

        return data

    def format_data(self, data):
        """Main format method."""

        return self._format_data(data)

    def format_meta(self, data):
        """Main format method."""

        return self._format_meta(data)

    def format_warning(self, data):
        """Main format method."""

        return self._format_warning(data)

    @staticmethod
    def _default_meta_data(total_results):
        """Create default data set if there aren't one from the response."""

        return {
            constants.ResponseDataConst.TOTAL_RESULTS: total_results,
            constants.ResponseDataConst.TOTAL_PAGES: 1,
            constants.ResponseDataConst.CURRENT_PAGE: 1
        }

    @staticmethod
    def _meta_data_to_int(meta_data):
        """Cast all data to int."""

        return {
            constants.ResponseDataConst.TOTAL_RESULTS:
                int(meta_data.get(constants.ResponseDataConst.TOTAL_RESULTS, 1)),
            constants.ResponseDataConst.TOTAL_PAGES:
                int(meta_data.get(constants.ResponseDataConst.TOTAL_PAGES, 1)),
            constants.ResponseDataConst.CURRENT_PAGE:
                int(meta_data.get(constants.ResponseDataConst.CURRENT_PAGE, 1)),
        }


class Json(Formatter):
    """JSON data formatter class."""

    def _unpack_response(self, data):
        """JSON decode"""

        try:
            return ujson.loads(data)
        except ValueError:
            return constants.ResponseConst.DEFAULT_ERROR_MESSAGE

    def _format_data(self, data):
        """Transform raw data from server into python native type."""

        formatted_data = self._unpack_response(data)
        if isinstance(formatted_data, dict):
            return formatted_data.get(
                constants.ResponseDataConst.DATA, formatted_data
            )
        else:
            return formatted_data

    def _format_meta(self, data):
        """Transform raw data from server into python native type."""

        formatted_data = self._unpack_response(data)
        if isinstance(formatted_data, dict):
            return formatted_data.get(constants.ResponseDataConst.META, {})
        else:
            return self.__class__._default_meta_data(len(formatted_data))

    def _format_warning(self, data):
        """Transform raw warning data from server into python native type."""

        formatted_data = self._unpack_response(data)
        if isinstance(formatted_data, dict):
            return formatted_data.get(constants.WarningConst.WARNING)


class FormatterFactory:
    """Formatter factory class."""

    formatters = {
        constants.FormatterConst.JSON: Json,
    }

    def __init__(self, name: str):
        self._name = name

    def get_formatter(self):
        """Get the formatter class using string key."""

        return FormatterFactory.formatters.get(self._name)
