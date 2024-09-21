# Copyright 2024 Liant SASU
#
# License: MIT
# See: LICENSE file at root of the repository
#
# Author: Roland Laurès <roland@liant.dev>
"""
Here we intend to test the behavior when setting manually the headers field
of the Connection object
"""


from pytest_mock import MockFixture

from actioncable_client.connection import Connection # type: ignore
from actioncable_client.subscription import Subscription # type: ignore


def test_on_open(connection_connected: Connection, sub: Subscription, mocker: MockFixture):
    mocker.patch.object(sub, 'create')
    connection_connected._on_open(connection_connected.websocket)
    sub.create.assert_called_once_with()
