import unittest
import json
from unittest.mock import patch, AsyncMock
from src.vyper_client_py.websocket_client import VyperWebsocketClient, FeedType, SubscriptionType, SubscriptionMessageType
from src.vyper_client_py.exceptions import VyperWebsocketException

class TestVyperWebsocketClient(unittest.IsolatedAsyncioTestCase):
    def setUp(self):
        self.client = VyperWebsocketClient(api_key="test_api_key")
        self.test_feed_type = FeedType.TOKEN_EVENTS

    @patch("src.vyper_client_py.websocket_client.websockets.connect", new_callable=AsyncMock)
    async def test_connect_success(self, mock_connect):
        await self.client.connect(feed_type=self.test_feed_type)
        expected_url = f"wss://api.vyper.trade/api/v1/ws/{self.test_feed_type.value}?apiKey=test_api_key"
        mock_connect.assert_called_once_with(expected_url)

    @patch("src.vyper_client_py.websocket_client.websockets.connect", new_callable=AsyncMock)
    async def test_subscribe_success(self, mock_connect):
        mock_connection = AsyncMock()
        mock_connect.return_value = mock_connection
        await self.client.connect(feed_type=self.test_feed_type)

        subscription_message = {
            "action": SubscriptionMessageType.SUBSCRIBE.value,
            "types": [SubscriptionType.PUMPFUN_TOKENS.value, SubscriptionType.RAYDIUM_AMM_TOKENS.value]
        }
        await self.client.subscribe(feed_type=self.test_feed_type, subscription_message=subscription_message)

        mock_connection.send.assert_called_once_with(json.dumps(subscription_message))

    @patch("src.vyper_client_py.websocket_client.websockets.connect", new_callable=AsyncMock)
    async def test_unsubscribe_success(self, mock_connect):
        mock_connection = AsyncMock()
        mock_connect.return_value = mock_connection
        await self.client.connect(feed_type=self.test_feed_type)

        unsubscribe_message = {
            "action": SubscriptionMessageType.UNSUBSCRIBE.value,
            "types": [SubscriptionType.PUMPFUN_TOKENS.value]
        }
        await self.client.unsubscribe(feed_type=self.test_feed_type, subscription_message=unsubscribe_message)

        mock_connection.send.assert_called_once_with(json.dumps(unsubscribe_message))

    @patch("src.vyper_client_py.websocket_client.websockets.connect", new_callable=AsyncMock)
    async def test_listen_success(self, mock_connect):
        mock_connection = AsyncMock()
        mock_connect.return_value = mock_connection
        mock_connection.recv = AsyncMock(
            side_effect=[
                json.dumps({"event": "test_message_1"}),
                json.dumps({"event": "test_message_2"}),
                Exception("Connection closed unexpectedly")  
            ]
        )

        async def message_handler(message):
            self.received_messages.append(message)

        self.client.set_message_handler(message_handler)
        self.received_messages = []
        await self.client.connect(feed_type=self.test_feed_type)
        
        with self.assertRaises(VyperWebsocketException):
            await self.client.listen()

        self.assertEqual(len(self.received_messages), 2)
        self.assertEqual(self.received_messages[0], {"event": "test_message_1"})
        self.assertEqual(self.received_messages[1], {"event": "test_message_2"})


    @patch("src.vyper_client_py.websocket_client.websockets.connect", new_callable=AsyncMock)
    async def test_handle_message_success(self, mock_connect):
        mock_connection = AsyncMock()
        mock_connect.return_value = mock_connection

        async def mock_handler(message):
            self.handled_message = message

        self.client.set_message_handler(mock_handler)
        await self.client.connect(feed_type=self.test_feed_type)

        message = json.dumps({"type": "test", "data": "message"})
        await self.client.handle_message(message)

        self.assertEqual(self.handled_message, {"type": "test", "data": "message"})

    @patch("src.vyper_client_py.websocket_client.websockets.connect", new_callable=AsyncMock)
    async def test_disconnect_success(self, mock_connect):
        mock_connection = AsyncMock()
        mock_connect.return_value = mock_connection
        await self.client.connect(feed_type=self.test_feed_type)
        await self.client.disconnect()
        mock_connection.close.assert_called_once()

    @patch("src.vyper_client_py.websocket_client.websockets.connect", new_callable=AsyncMock)
    async def test_cleanup_success(self, mock_connect):
        mock_connection = AsyncMock()
        mock_connect.return_value = mock_connection
        await self.client.connect(feed_type=self.test_feed_type)
        await self.client.cleanup()
        mock_connection.close.assert_called_once()

    @patch("src.vyper_client_py.websocket_client.websockets.connect", new_callable=AsyncMock)
    async def test_ping_pong_success(self, mock_connect):
        mock_connection = AsyncMock()
        mock_connect.return_value = mock_connection
        await self.client.connect(feed_type=self.test_feed_type)

        await self.client.ping()
        mock_connection.ping.assert_called_once()
        mock_connection.ping.reset_mock()

        await self.client.pong()
        mock_connection.pong.assert_called_once()

    @patch("src.vyper_client_py.websocket_client.websockets.connect", new_callable=AsyncMock)
    async def test_network_error(self, mock_connect):
        mock_connect.side_effect = Exception("Network error")

        with self.assertRaises(VyperWebsocketException):
            await self.client.connect(feed_type=self.test_feed_type)

    @patch("src.vyper_client_py.websocket_client.websockets.connect", new_callable=AsyncMock)
    async def test_unexpected_error(self, mock_connect):
        mock_connect.side_effect = Exception("Unexpected error")

        with self.assertRaises(VyperWebsocketException):
            await self.client.connect(feed_type=self.test_feed_type)


if __name__ == "__main__":
    unittest.main()
