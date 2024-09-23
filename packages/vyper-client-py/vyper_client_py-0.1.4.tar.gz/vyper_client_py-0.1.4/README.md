# Vyper API Python SDK

![Vyper](https://images.vyper.trade/0000/vyper-header)

A Python SDK for interacting with the [Vyper API](https://build.vyper.trade/). This library allows developers to integrate Vyper's http and websocket api into their Python applications with ease.

## Table of Contents

- [Vyper API Python SDK](#vyper-api-python-sdk)
  - [Table of Contents](#table-of-contents)
  - [Installation](#installation)
  - [Quick Start](#quick-start)
  - [Usage](#usage)
    - [Client Initialization](#client-initialization)
    - [REST API Example](#rest-api-example)
    - [WebSocket API Example](#websocket-api-example)
  - [API Documentation](#api-documentation)

## Installation

To install the Vyper API Python SDK, use pip:

```bash
pip install vyper-client-py
```

## Quick Start

Here's a simple example to get you started:

```py
from vyper_client import VyperClient

# Initialize the client with your API key
client = VyperClient(api_key="your_api_key_here")

# Get the list of chain IDs supported by Vyper
chain_ids = client.get_chain_ids()
print("Supported chain IDs:", chain_ids)
```

## Usage

### Client Initialization

The `VyperClient` class provides access to the RESTful API endpoints:

```python
from vyper_client import VyperClient

# Create a client instance
client = VyperClient(api_key="your_api_key_here")
```

### REST API Example

Retrieve the market data for a specific token:

```python
# Fetch the All-Time High (ATH) data for a token
token_ath = client.get_token_ath(chain_id=1, market_id="AVs9TA4nWDzfPJE9gGVNJMVhcQy3V9PGazuz33BfG2RA")

print(f"Market Cap USD: {token_ath.market_cap_usd}")
print(f"Timestamp: {token_ath.timestamp}")
```

### WebSocket API Example

```python
import asyncio
from vyper_client import VyperWebsocketClient, FeedType, SubscriptionType

async def main():
    # Create a websocket client instance
    ws_client = VyperWebsocketClient(api_key="your_api_key_here")

    # Define a message handler
    async def message_handler(message):
        print("Received message:", message)

    ws_client.set_message_handler(message_handler)

    # Connect to the WebSocket and subscribe to token events
    await ws_client.connect(FeedType.TOKEN_EVENTS)
    await ws_client.subscribe(
        FeedType.TOKEN_EVENTS,
        subscription_message={
            "action": "subscribe",
            "types": [SubscriptionType.PUMPFUN_TOKENS.value]
        }
    )

    # Listen for incoming messages
    await ws_client.listen()

# Run the asyncio event loop
asyncio.run(main())
```

## API Documentation

For detailed information on the Vyper API, refer to the official documentation:

- API Dashboard: [Vyper Dashboard](https://build.vyper.trade/)
- API Documentation: [Vyper API Docs](ttps://docs.vyper.trade/)
