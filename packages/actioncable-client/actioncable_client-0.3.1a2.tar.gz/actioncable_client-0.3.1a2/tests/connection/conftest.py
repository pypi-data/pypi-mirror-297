# File automatically loaded by pytest
# This allow to share fixtures

from websocket import WebSocketApp
from actioncable_client.connection import Connection # type: ignore
from actioncable_client.subscription import Subscription # type: ignore
from actioncable_client.message import Message # type: ignore

import pytest
from pytest_mock import MockFixture

@pytest.fixture
def WebsocketApp(mocker: MockFixture):
    """Fixture """
    return mocker.patch('websocket.WebSocketApp', spec=WebSocketApp)

@pytest.fixture
def connection(WebsocketApp) -> Connection:
    import logging
    conn = Connection('ws://example.com/cable', origin='http://example.com')
    conn.logger.setLevel(logging.DEBUG)
    return conn

@pytest.fixture
def connection_connected(connection, WebsocketApp, mocker: MockFixture) -> Connection:
    connection.connect()
    connection.websocket.sock = mocker.MagicMock()
    connection.websocket.sock.connected = True
    return connection

@pytest.fixture
def channel_id():
    return { 'channel': 'MyChannel' }

@pytest.fixture
def channel_id_str(channel_id):
    from json import dumps
    return dumps(channel_id)

@pytest.fixture
def sub(connection, channel_id):
    return Subscription(connection, identifier=channel_id)

@pytest.fixture
def a_message():
    return Message(action='my_action', data={ 'param1': 'value1' })

@pytest.fixture
def a_message_dict():
    return {
        'identifier': '"{"channel":"ChannelB"}"',
        'message': {
            'action': 'my_action',
            'param1': 'value1'
        }
    }
