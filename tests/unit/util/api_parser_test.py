from util import api


class TestApiParser:

    def test_when_api_returns_success(self):
        """
        This scenario emulates when the API returns status_code=200 and its content
        :return:
        """
        ...

    def test_when_api_returns_error(self):
        """
        This scenario emulates when the API returned status code=400 (error)
        """
        ...

    def test_when_api_fails_communication(self):
        """
        This scenario emulates a ConnectionError exception
        """
        ...
