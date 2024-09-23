import websockets
import json
from enum import Enum
from .exceptions import VyperWebsocketException
from typing import Dict, List, Callable

class FeedType(Enum):
    TOKEN_EVENTS = "token-events"
    MIGRATION_EVENTS = "migration-events"
    WALLET_EVENTS = "wallet-events"

class SubscriptionMessageType(Enum):
    SUBSCRIBE = "subscribe"
    UNSUBSCRIBE = "unsubscribe"

class SubscriptionType(Enum):
    PUMPFUN_TOKENS = "PumpfunTokens"
    RAYDIUM_AMM_TOKENS = "RaydiumAmmTokens"
    RAYDIUM_CPMM_TOKENS = "RaydiumCpmmTokens"
    RAYDIUM_CLMM_TOKENS = "RaydiumClmmTokens"

class TokenSubscriptionMessage:
    def __init__(self, types: List[SubscriptionType]):
        self.action = SubscriptionMessageType.SUBSCRIBE.value
        self.types = [t.value for t in types]

    def to_dict(self) -> Dict:
        return {
            "action": self.action,
            "types": self.types
        }

class WalletSubscriptionMessage:
    def __init__(self, wallets: List[str]):
        self.action = SubscriptionMessageType.SUBSCRIBE.value
        self.wallets = wallets

    def to_dict(self) -> Dict:
        return {
            "action": self.action,
            "wallets": self.wallets
        }

class VyperWebsocketClient:
    def __init__(self, api_key: str):
        self.base_url = "wss://api.vyper.trade/api/v1/ws"
        self.api_key = api_key
        self.connection = None
        self.message_handler = None

    async def connect(self, feed_type: FeedType):
        url = f"{self.base_url}/{feed_type.value}?apiKey={self.api_key}"
        try:
            self.connection = await websockets.connect(url)
        except Exception as e:
            raise VyperWebsocketException(f"Failed to connect: {e}", connection_info=url)

    async def subscribe(self, feed_type: FeedType, subscription_message: Dict):
        if feed_type in [FeedType.TOKEN_EVENTS, FeedType.WALLET_EVENTS]:
            subscribe_message = json.dumps(subscription_message)
            try:
                await self.connection.send(subscribe_message)
            except Exception as e:
                raise VyperWebsocketException(f"Failed to subscribe: {e}")

    async def unsubscribe(self, feed_type: FeedType, subscription_message: Dict):
        if feed_type in [FeedType.TOKEN_EVENTS, FeedType.WALLET_EVENTS]:
            unsubscribe_message = json.dumps(subscription_message)
            try:
                await self.connection.send(unsubscribe_message)
            except Exception as e:
                raise VyperWebsocketException(f"Failed to unsubscribe: {e}")

    async def listen(self):
        try:
            max_iterations = 10
            for _ in range(max_iterations):
                message = await self.connection.recv()
                await self.handle_message(message)
        except websockets.ConnectionClosed as e:
            raise VyperWebsocketException("Connection closed unexpectedly", connection_info=str(e))
        except Exception as e:
            raise VyperWebsocketException(f"Error while listening to messages: {e}")

    async def handle_message(self, message: str):
        data = json.loads(message)
        if self.message_handler:
            await self.message_handler(data) 

    async def disconnect(self):
        try:
            await self.connection.close()
        except Exception as e:
            raise VyperWebsocketException(f"Failed to disconnect: {e}")

    async def cleanup(self):
        if self.connection:
            await self.disconnect()

    async def ping(self):
        try:
            await self.connection.ping()
        except Exception as e:
            raise VyperWebsocketException(f"Failed to send ping: {e}")

    async def pong(self):
        try:
            await self.connection.pong()
        except Exception as e:
            raise VyperWebsocketException(f"Failed to send pong: {e}")

    def set_message_handler(self, handler: Callable[[Dict], None]):
        self.message_handler = handler