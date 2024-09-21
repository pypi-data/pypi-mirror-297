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

from actioncable_client.connection import Connection # type: ignore


def test_log_ping(connection: Connection):
    assert not connection.log_ping
    connection.log_ping = True
    assert connection.log_ping

def test_socket_present_when_not_connected(connection: Connection):
    assert not connection.socket_present

def test_socket_present_when_connected(connection_connected: Connection):
    assert connection_connected.socket_present


def test_connected_when_not_connected(connection: Connection):
    assert not connection.connected

def test_connected_when_connected(connection_connected: Connection):
    assert connection_connected.connected
