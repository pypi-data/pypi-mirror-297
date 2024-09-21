# Copyright 2024 Liant SASU
#
# License: MIT
# See: LICENSE file at root of the repository
#
# Author: Roland Laurès <roland@liant.dev>
"""
Test file for BaseChannel module
"""

from actioncable_client.action_base_channel import ActionBaseChannel # type: ignore
from actioncable_client.connection import Connection # type: ignore
from actioncable_client.subscription import Subscription # type: ignore
from actioncable_client.message import Message # type: ignore

import pytest
from pytest_mock import MockFixture

# Create a sub-class that will implement the mechanism of ActionBaseChannel
class ChannelA(ActionBaseChannel):
    def __init__(self, connection: Connection):
        super().__init__(connection, self._on_unkonwn_action_message)
    def _on_unkonwn_action_message(self, message: Message):
        pass
    def my_action(self, param1):
        pass

# Create a sub-class that doen't use on_message argument
class ChannelB(ActionBaseChannel):
    def __init__(self, connection: Connection):
        super().__init__(connection)
    def _on_unkonwn_action_message(self, message: Message):
        pass
    def my_action(self, param1):
        pass

# Mock the connection
@pytest.fixture
def connection(mocker: MockFixture):
    MockedConnection = mocker.MagicMock(spec=Connection)
    return MockedConnection()

# Test initialization
def test_init_when_not_connected(connection: Connection, mocker: MockFixture):
    spied_sub = mocker.spy(Subscription, '__init__')
    spied_sub_on_receive = mocker.spy(Subscription, 'on_receive')
    spied_sub_create = mocker.spy(Subscription, 'create')
    connection.connected = False
    obj = ChannelA(connection)
    assert isinstance(obj._subscription, Subscription)
    spied_sub.assert_called_once_with(obj._subscription, connection, { 'channel': 'ChannelA' })
    spied_sub_on_receive.assert_called_once_with(obj._subscription, obj._on_receive)
    spied_sub_create.assert_not_called()

def test_init_with_on_message(connection: Connection, mocker: MockFixture):
    spied_sub = mocker.spy(Subscription, '__init__')
    spied_sub_on_receive = mocker.spy(Subscription, 'on_receive')
    spied_sub_create = mocker.spy(Subscription, 'create')
    obj = ChannelA(connection)
    assert isinstance(obj._subscription, Subscription)
    spied_sub.assert_called_once_with(obj._subscription, connection, { 'channel': 'ChannelA' })
    spied_sub_on_receive.assert_called_once_with(obj._subscription, obj._on_receive)
    assert obj.on_unkonwn_action_message is not None
    spied_sub_create.assert_called_once()

def test_init_without_on_message(connection: Connection, mocker: MockFixture):
    spied_sub = mocker.spy(Subscription, '__init__')
    spied_sub_on_receive = mocker.spy(Subscription, 'on_receive')
    spied_sub_create = mocker.spy(Subscription, 'create')
    obj = ChannelB(connection)
    assert isinstance(obj._subscription, Subscription)
    spied_sub.assert_called_once_with(obj._subscription, connection, { 'channel': 'ChannelB' })
    spied_sub_on_receive.assert_called_once_with(obj._subscription, obj._on_receive)
    spied_sub_create.assert_called_once()
    assert obj.on_unkonwn_action_message is None

# Test when receiving a message
@pytest.fixture
def channel_a(connection: Connection, mocker: MockFixture):
    return ChannelA(connection)

@pytest.fixture
def channel_b(connection: Connection, mocker: MockFixture):
    return ChannelB(connection)

@pytest.fixture
def message_known_action():
    return Message(action='my_action', data={ 'param1': 'value1' })
@pytest.fixture
def message_unknown_action():
    return Message(action='unknown', data={ 'param1': 'value1' })

def test_on_receive_with_on_message_when_receiving_a_known_action(channel_a: ChannelA, message_known_action: Message, mocker: MockFixture):
    spied_on_unkonwn_action_message = mocker.spy(channel_a, 'on_unkonwn_action_message')
    spied_action = mocker.spy(channel_a, 'my_action')
    channel_a._on_receive(message_known_action)
    spied_on_unkonwn_action_message.assert_not_called()
    spied_action.assert_called_once_with(**message_known_action.data)

def test_on_receive_with_on_message_when_receiving_a_unknown_action(channel_a: ChannelA, message_unknown_action, mocker: MockFixture):
    spied_on_unkonwn_action_message = mocker.spy(channel_a, 'on_unkonwn_action_message')
    spied_action = mocker.spy(channel_a, 'my_action')
    channel_a._on_receive(message_unknown_action)
    spied_on_unkonwn_action_message.assert_called_once_with(message_unknown_action)
    spied_action.assert_not_called()

def test_on_receive_without_on_message_when_receiving_a_known_action(channel_b: ChannelB, message_known_action: Message, mocker: MockFixture):
    spied_action = mocker.spy(channel_b, 'my_action')
    channel_b._on_receive(message_known_action)
    spied_action.assert_called_once_with(**message_known_action.data)

def test_on_receive_without_on_message_when_receiving_a_unknown_action(channel_b: ChannelB, message_unknown_action, mocker: MockFixture):
    spied_action = mocker.spy(channel_b, 'my_action')
    channel_b._on_receive(message_unknown_action)
    spied_action.assert_not_called()

def test_transmit(channel_b: ChannelB, mocker: MockFixture):
    my_data = { 'param1': 'value1', 'param2': 2 }
    myMessage = Message(action='my_action', data=my_data)
    mocker.patch('actioncable_client.message.Message', return_value=myMessage)
    # mocker.patch.object(Message, '__call__', return_value=myMessage)
    mocker.patch.object(channel_b._subscription, 'send')
    channel_b.transmit(action='my_action', data=my_data)
    channel_b._subscription.send.assert_called_once_with(myMessage)
