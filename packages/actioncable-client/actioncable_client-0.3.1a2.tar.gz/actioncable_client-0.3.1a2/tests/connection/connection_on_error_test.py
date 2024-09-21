# Copyright 2024 Liant SASU
#
# License: MIT
# See: LICENSE file at root of the repository
#
# Author: Roland Laurès <roland@liant.dev>
"""
Here we intend to test the behavior of _run_forever method when an exception is raised
in the websocket creation.
"""

import logging

import pytest
from pytest_mock import MockFixture
from time import sleep

from actioncable_client.connection import Connection # type: ignore

HEADER = { 'Authorization': 'Bearer MyToken'}

@pytest.fixture
def connection() -> Connection:
    conn = Connection('ws://example.com/cable', header=HEADER)
    conn.logger.setLevel(logging.DEBUG)
    return conn

def test_run_forever_with_exception(connection: Connection, mocker: MockFixture):
    connection.auto_reconnect = True
    assert connection.websocket is None
    exc = RuntimeError('An error')
    WebsocketApp = mocker.patch('websocket.WebSocketApp', side_effect=exc)
    logger_error = mocker.patch.object(connection.logger, 'error')
    connection.connect()
    sleep(0.001) # ensure _run_forever is called
    WebsocketApp.assert_called_once_with( # type: ignore
        'ws://example.com/cable', header=HEADER,
        on_message=connection._on_message, on_close=connection._on_close, on_open=connection._on_open
    )
    logger_error.assert_called_once_with('Connection loop raised exception. Exception: %s', exc)
    # No ping because already managed by server side.
    assert connection.auto_reconnect
    assert connection.websocket is None

def test_connect_when_already_connected(connection_connected: Connection, mocker: MockFixture):
    logger_warning = mocker.patch.object(connection_connected.logger, 'warning')
    connection_connected.connect()
    logger_warning.assert_called_once_with('Connection already established. Return...')
