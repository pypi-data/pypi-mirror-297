# Copyright 2024 Liant SASU
#
# License: MIT
# See: LICENSE file at root of the repository
#
# Author: Roland Laurès <roland@liant.dev>
"""
Test file for about section
"""

from actioncable_client.__about__ import __version__ # type: ignore
from semantic_version import validate # type: ignore

# Test initialization
def test_version():
    assert isinstance(__version__, str)
    assert validate(__version__)
