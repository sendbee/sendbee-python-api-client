import ujson

from abc import ABCMeta, abstractmethod
from typing import AnyStr, Any, Dict, Union, Type

from sendbee_api.constants import FormatterConst, ResponseDataConst, \
    ResponseConst


class Formatter(metaclass=ABCMeta):
    """Abstract formatter class."""

    def __init__(self, response):
        self._response = response

    @abstractmethod
    def _format(self, data: AnyStr) -> Any:
        """Format method in formatter classes."""

        return data

    def format(self, data: AnyStr) -> Any:
        """Main format method."""

        return self._format(data)

    @abstractmethod
    def _format_meta(self, data: AnyStr) -> Any:
        """Format method in formatter classes."""

        return data

    def format_meta(self, data: AnyStr) -> Any:
        """Main format method."""

        return self._format_meta(data)

    @staticmethod
    def _default_meta_data(total_results: int) -> Dict:
        """Create default data set if there aren't one from the response."""

        return {
            ResponseDataConst.TOTAL_RESULTS: total_results,
            ResponseDataConst.TOTAL_PAGES: 1,
            ResponseDataConst.CURRENT_PAGE: 1
        }

    @staticmethod
    def _meta_data_to_int(meta_data: Dict) -> Dict:
        """Cast all data to int."""

        return {
            ResponseDataConst.TOTAL_RESULTS:
                int(meta_data.get(ResponseDataConst.TOTAL_RESULTS, 1)),
            ResponseDataConst.TOTAL_PAGES:
                int(meta_data.get(ResponseDataConst.TOTAL_PAGES, 1)),
            ResponseDataConst.CURRENT_PAGE:
                int(meta_data.get(ResponseDataConst.CURRENT_PAGE, 1)),
        }


class Json(Formatter):
    """JSON data formatter class."""

    def _unpack_response(self, data: Any) -> Dict:
        """JSON decode"""

        try:
            return ujson.loads(data)
        except ValueError:
            print(data)
            return ResponseConst.DEFAULT_ERROR_MESSAGE

    def _format(self, data: AnyStr) -> Dict:
        """Transform raw data from server into python native type."""

        formatted_data = self._unpack_response(data)
        if isinstance(formatted_data, dict):
            return formatted_data.get(ResponseDataConst.DATA, formatted_data)
        else:
            return formatted_data

    def _format_meta(self, data: AnyStr) -> Dict:
        """Transform raw data from server into python native type."""

        formatted_data = self._unpack_response(data)
        if isinstance(formatted_data, dict):
            return formatted_data.get(ResponseDataConst.META, {})
        else:
            return self.__class__._default_meta_data(len(formatted_data))


class FormatterFactory:
    """Formatter factory class."""

    formatters = {
        FormatterConst.JSON: Json,
    }

    def __init__(self, name: str):
        self._name = name

    def get_formatter(self) -> Union[Type[Json], None]:
        """Get the formatter class using string key."""

        return FormatterFactory.formatters.get(self._name)
