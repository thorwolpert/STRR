import os
from unittest import mock

from strr_api.common.run_version import _get_commit_hash, get_run_version

ref = "de9d3e669f9ef35a7031d9cea7013984b8a87000"
version = "0.0.2"


def test_get_commit_hash():
    assert _get_commit_hash() is None

    with mock.patch.dict(os.environ, {"VCS_REF": ref}):
        assert _get_commit_hash() == ref


def test_get_run_version():
    assert get_run_version() == version
    ref = "de9d3e669f9ef35a7031d9cea7013984b8a87000"
    with mock.patch.dict(os.environ, {"VCS_REF": ref}):
        assert get_run_version() == f"{version}-{ref}"
