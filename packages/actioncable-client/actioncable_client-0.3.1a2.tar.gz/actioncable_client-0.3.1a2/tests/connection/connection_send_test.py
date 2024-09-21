# Copyright 2024 Liant SASU
#
# License: MIT
# See: LICENSE file at root of the repository
#
# Author: Roland Laurès <roland@liant.dev>
"""
Here we intend to test the behavior of the send method
"""


from pytest_mock import MockFixture
import json
from typing import Any

from actioncable_client.connection import Connection # type: ignore


def test_send_when_not_connected(connection: Connection, a_message_dict: dict[str, Any], mocker: MockFixture):
    logger_warning = mocker.patch.object(connection.logger, 'warning')
    assert not connection.send(a_message_dict)
    logger_warning.assert_called_once_with('Connection not established. Return...')

def test_send_when_connected(connection_connected: Connection, a_message_dict: dict[str, Any]):
    assert connection_connected.send(a_message_dict)
    connection_connected.websocket.send.assert_called_once_with(json.dumps(a_message_dict))
