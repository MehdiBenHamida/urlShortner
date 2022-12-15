import pytest

from src.app.utils import get_random_string, retry


class SomeException(Exception):
    pass


class TestUtils:
    counter = 0

    def test_get_random_string(self):
        """Should return a random string with the given length, default 10."""
        assert len(get_random_string()) == 10
        assert len(get_random_string(5)) == 5

    def test_retry(self):
        """Should retry the broken function `max_retries` times."""
        max_retries = 3

        @retry(exceptions=SomeException, max_retries=max_retries)
        def broken_function():
            self.counter += 1
            raise SomeException

        with pytest.raises(SomeException):
            broken_function()

        assert self.counter == max_retries
