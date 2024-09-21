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

import threading
import logging

import pytest
from pytest_mock import MockFixture
from callee import StartsWith # type: ignore
from time import sleep

from actioncable_client.connection import Connection # type: ignore

HEADER = { 'Authorization': 'Bearer MyToken'}

@pytest.fixture
def connection() -> Connection:
    conn = Connection('ws://example.com/cable', header=HEADER)
    conn.logger.setLevel(logging.DEBUG)
    return conn


def test_instantiation(connection: Connection):
    assert connection is not None

def test_connect_should_start_run_forever_thread(connection: Connection, mocker: MockFixture):
    mocker.patch('threading.Thread', spec=threading.Thread)
    assert connection.auto_reconnect is False
    assert connection.ws_thread is None
    connection.connect()
    threading.Thread.assert_called_once_with(name=StartsWith('APIConnectionThread_'), target=connection._run_forever) # type: ignore
    assert connection.auto_reconnect is True
    assert connection.ws_thread.daemon is True
    connection.ws_thread.start.assert_called_once()

def test_run_forever_should_create_WS_and_call_run_forever(connection: Connection, WebsocketApp, mocker: MockFixture):
    connection.auto_reconnect = True
    assert connection.websocket is None
    connection.connect()
    sleep(0.001) # ensure _run_forever is called
    WebsocketApp.assert_called_once_with( # type: ignore
        'ws://example.com/cable', header=HEADER,
        on_message=connection._on_message, on_close=connection._on_close, on_open=connection._on_open
    )
    assert isinstance(connection.websocket, WebsocketApp.__class__)
    # No ping because already managed by server side.
    connection.websocket.run_forever.assert_called_once_with() # type: ignore
    assert connection.auto_reconnect
    # finish the loop.
    connection.disconnect()
    assert not connection.auto_reconnect
    connection.websocket.close.assert_called_once_with()
