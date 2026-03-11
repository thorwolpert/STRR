from contextlib import contextmanager
import random
import string

import pytest
from strr_api import jwt as _jwt
from structlog.testing import capture_logs


@pytest.fixture
def log_capture():
    """Intercepts structlog messages and returns them as a list of dicts."""
    with capture_logs() as caps:
        yield caps


@pytest.fixture(scope="function")
def random_string():
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


@pytest.fixture(scope="session")
def jwt():
    return _jwt


@contextmanager
def not_raises(exception):
    try:
        yield
    except exception:
        raise pytest.fail(f"DID RAISE {exception}")


@pytest.fixture
def inject_config(app, request):
    """
    Safely injects config variables for a single test and reverts them afterwards.
    Usage: @pytest.mark.conf(KEY="value")
    """
    marker = request.node.get_closest_marker("conf")

    if not marker:
        yield
        return

    new_config = marker.kwargs
    original_values = {}

    for key in new_config:
        original_values[key] = app.config.get(key)

    app.config.update(new_config)

    yield

    # RESTORE: Revert to original values
    for key, old_value in original_values.items():
        if old_value is None:
            app.config.pop(key, None)
        else:
            app.config[key] = old_value
