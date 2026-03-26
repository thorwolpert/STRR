import os
import random
import string

import pytest


@pytest.fixture(scope="function")
def random_string():
    """Returns a random string, defult length is 10."""

    def _generate(length=10):
        characters = string.ascii_letters + string.digits
        return "".join(random.choices(characters, k=length))

    return _generate


@pytest.fixture(scope="function")
def random_integer():
    """Returns a random integer, defult max is 1000."""

    def _generate(max=1000):
        return random.randint(1, max)

    return _generate
