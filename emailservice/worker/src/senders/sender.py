"""Abstract class."""

from abc import ABC, abstractmethod


class AbstractSender(ABC):
    """Abstract class AbstractSender."""

    @abstractmethod
    def match_shipment_method(self, methods):
        """Match shipment method.

        :param methods:
        :return:
        """
        pass

    @abstractmethod
    def send_one(self, *args, **kwargs):
        """Senf=d one.

        :param args:
        :param kwargs:
        :return:
        """
        pass

    @abstractmethod
    def send_many(self, *args, **kwargs):
        """Send many.

        :param args:
        :param kwargs:
        :return:
        """
        pass
