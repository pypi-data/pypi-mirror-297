import unittest
import requests
from unittest.mock import patch, Mock
from src.client import VyperClient
from src.exceptions import AuthenticationError, RateLimitError, ServerError, VyperApiException
from src.classes import TokenHolder, TokenATH, TokenPair, MigrationState, TokenMarket, TokenMetadata, TokenSymbol, TokenSearchResult, TopTrader, WalletAggregatedPnL, WalletHolding, WalletPnL, TokenPairs

class TestVyperClient(unittest.TestCase):
    def setUp(self):
        self.client = VyperClient(api_key="test_key")

    @patch("src.client.requests.Session.request")
    def test_get_chain_ids_success(self, mock_request):
        mock_response = {
            "status": "success",
            "message": "Chain IDs retrieved successfully",
            "data": {
                "solana": 900,
                "tron": 1000,
                "ethereum": 1,
                "base": 8453,
                "arbitrum": 42161,
                "bsc": 56,
                "blast": 81457
            }
        }
        mock_request.return_value.json.return_value = mock_response
        mock_request.return_value.raise_for_status.return_value = None

        response = self.client.get_chain_ids()

        self.assertEqual(response, mock_response['data'])
        mock_request.assert_called_once_with(
            "GET",
            "https://api.vyper.trade/api/v1/chain/ids",
            params=None
        )

    @patch("src.client.requests.Session.request")
    def test_rate_limit_error(self, mock_request):
        mock_response = Mock()
        mock_response.status_code = 429
        mock_response.headers = {'Retry-After': '3.00'}
        mock_response.json.return_value = {"error": "Rate limit exceeded"}
        mock_request.return_value = mock_response
        mock_request.return_value.raise_for_status.side_effect = requests.exceptions.HTTPError(response=mock_response)

        with self.assertRaises(RateLimitError) as context:
            self.client.get_chain_ids()

        self.assertEqual(context.exception.retry_after, 3.00)
        self.assertIn("Rate limit exceeded", str(context.exception))

    @patch("src.client.requests.Session.request")
    def test_authentication_error(self, mock_request):
        mock_response = Mock()
        mock_response.status_code = 401
        mock_response.json.return_value = {"error": "Invalid or expired API key"}
        mock_request.return_value = mock_response
        mock_request.return_value.raise_for_status.side_effect = requests.exceptions.HTTPError(response=mock_response)

        with self.assertRaises(AuthenticationError) as context:
            self.client.get_chain_ids()

        self.assertIn("Invalid or expired API key", str(context.exception))

    @patch("src.client.requests.Session.request")
    def test_server_error(self, mock_request):
        mock_response = Mock()
        mock_response.status_code = 500
        mock_response.json.return_value = {"error": "Internal server error"}
        mock_request.return_value = mock_response
        mock_request.return_value.raise_for_status.side_effect = requests.exceptions.HTTPError(response=mock_response)

        with self.assertRaises(ServerError) as context:
            self.client.get_chain_ids()

        self.assertIn("Server error: 500", str(context.exception))

    @patch("src.client.requests.Session.request")
    def test_other_http_error(self, mock_request):
        mock_response = Mock()
        mock_response.status_code = 403
        mock_response.json.return_value = {"error": "Forbidden"}
        mock_request.return_value = mock_response
        mock_request.return_value.raise_for_status.side_effect = requests.exceptions.HTTPError(response=mock_response)

        with self.assertRaises(VyperApiException) as context:
            self.client.get_chain_ids()

        self.assertIn("HTTP error occurred", str(context.exception))

    @patch("src.client.requests.Session.request")
    def test_network_error(self, mock_request):
        mock_request.side_effect = requests.exceptions.ConnectionError("Network error")

        with self.assertRaises(VyperApiException) as context:
            self.client.get_chain_ids()

        self.assertIn("An error occurred", str(context.exception))

    @patch("src.client.requests.Session.request")
    def test_get_token_ath_success(self, mock_request):
        mock_response = {
            "status": "success",
            "message": "Token ATH data retrieved successfully",
            "data": {
                "marketCapUsd": 1000000000,
                "timestamp": 1632825600,
                "tokenLiquidityUsd": 50000000
            }
        }
        mock_request.return_value.json.return_value = mock_response
        mock_request.return_value.raise_for_status.return_value = None

        response = self.client.get_token_ath(chain_id=1, market_id="BTC")

        self.assertIsInstance(response, TokenATH)
        self.assertEqual(response.market_cap_usd, 1000000000)
        self.assertEqual(response.timestamp, 1632825600)
        self.assertEqual(response.token_liquidity_usd, 50000000)
        mock_request.assert_called_once_with(
            "GET",
            "https://api.vyper.trade/api/v1/token/ath",
            params={"chainID": 1, "marketID": "BTC"}
        )

    @patch("src.client.requests.Session.request")
    def test_get_token_market_success(self, mock_request):
        mock_response = {
            "status": "success",
            "message": "Token market data retrieved successfully",
            "data": {
                "abused": False,
                "bondingCurvePercentage": 0.5,
                "buyTxnCount": 100,
                "chainId": 900,
                "contractCreator": "0x1234567890abcdef",
                "createdTimestamp": 1632825600,
                "description": "Test Token",
                "freezeAuthority": False,
                "image": "https://example.com/token.png",
                "initialAssetLiquidity": 1000000,
                "initialUsdLiquidity": 100000,
                "isMigrated": False,
                "lpBurned": False,
                "lpCreator": "0xabcdef1234567890",
                "marketId": "TEST-SOL",
                "metadataUri": "https://example.com/metadata.json",
                "migratedMarketId": "",
                "migrationState": {
                    "durationMinutes": 0,
                    "makers": 0,
                    "migrationTimestamp": 0,
                    "volume": 0
                },
                "mintAuthority": True,
                "name": "Test Token",
                "pooledAsset": 1000000,
                "pooledToken": 1000000,
                "priceChangePercent": 0.1,
                "sellTxnCount": 50,
                "symbol": "TEST",
                "telegram": "https://t.me/testtoken",
                "tokenLiquidityAsset": 500000,
                "tokenLiquidityUsd": 500000,
                "tokenMarketCapAsset": 10000000,
                "tokenMarketCapUsd": 10000000,
                "tokenMint": "0x0987654321fedcba",
                "tokenPriceAsset": 1,
                "tokenPriceUsd": 1.5,
                "tokenType": "SPL",
                "top10HoldingPercent": 30,
                "totalSupply": 1000000000,
                "transactionCount": 1000,
                "twitter": "https://twitter.com/testtoken",
                "volumeAsset": 500000,
                "volumeUsd": 750000,
                "website": "https://testtoken.com"
            }
        }
        mock_request.return_value.json.return_value = mock_response
        mock_request.return_value.raise_for_status.return_value = None

        response = self.client.get_token_market(market_id="TEST-SOL")

        self.assertIsInstance(response, TokenPair)
        self.assertEqual(response.market_id, "TEST-SOL")
        self.assertEqual(response.chain_id, 900)
        self.assertIsInstance(response.migration_state, MigrationState)
        self.assertEqual(response.migration_state.duration_minutes, 0)
        mock_request.assert_called_once_with(
            "GET",
            "https://api.vyper.trade/api/v1/token/market/TEST-SOL",
            params={"chainID": 900, "interval": "24h"}
        )

    @patch("src.client.requests.Session.request")
    def test_get_token_holders_success(self, mock_request):
        mock_response = {
            "status": "success",
            "message": "Token holders retrieved successfully",
            "data": {
                "holders": [
                    {
                        "percentOwned": 10.5,
                        "tokenHoldings": 105000,
                        "usdHoldings": 157500,
                        "walletAddress": "0x1111111111111111",
                        "walletTag": "Whale 1"
                    },
                    {
                        "percentOwned": 5.2,
                        "tokenHoldings": 52000,
                        "usdHoldings": 78000,
                        "walletAddress": "0x2222222222222222",
                        "walletTag": "Whale 2"
                    }
                ],
                "total_holders": 1000
            }
        }
        mock_request.return_value.json.return_value = mock_response
        mock_request.return_value.raise_for_status.return_value = None

        response = self.client.get_token_holders(market_id="TEST-SOL", chain_id=900)

        self.assertEqual(len(response['holders']), 2)
        self.assertIsInstance(response['holders'][0], TokenHolder)
        self.assertEqual(response['total_holders'], 1000)
        mock_request.assert_called_once_with(
            "GET",
            "https://api.vyper.trade/api/v1/token/holders",
            params={"marketID": "TEST-SOL", "chainID": 900}
        )

    def test_get_token_ath_no_api_key(self):
        client = VyperClient()  
        with self.assertRaises(AuthenticationError):
            client.get_token_ath(chain_id=1, market_id="BTC")

    def test_get_token_market_no_api_key(self):
        client = VyperClient()  
        with self.assertRaises(AuthenticationError):
            client.get_token_market(market_id="TEST-SOL")

    def test_get_token_holders_no_api_key(self):
        client = VyperClient()  
        with self.assertRaises(AuthenticationError):
            client.get_token_holders(market_id="TEST-SOL", chain_id=900)

    @patch("src.client.requests.Session.request")
    def test_get_chain_ids_no_auth(self, mock_request):
        mock_response = {
            "status": "success",
            "message": "Chain IDs retrieved successfully",
            "data": {
                "solana": 900,
                "tron": 1000,
                "ethereum": 1,
                "base": 8453,
                "arbitrum": 42161,
                "bsc": 56,
                "blast": 81457
            }
        }
        mock_request.return_value.json.return_value = mock_response
        mock_request.return_value.raise_for_status.return_value = None

        response = self.client.get_chain_ids()

        self.assertEqual(response, mock_response['data'])
        
        called_kwargs = mock_request.call_args.kwargs
        if 'headers' in called_kwargs:
            self.assertNotIn("X-API-Key", called_kwargs['headers'])
        else:
            self.assertNotIn('headers', called_kwargs)
            
    
    @patch("src.client.requests.Session.request")
    def test_get_token_markets_success(self, mock_request):
        mock_response = {
            "status": "success",
            "message": "Token markets retrieved successfully",
            "data": [
                {
                    "marketCapUsd": 1000000,
                    "marketID": "BTC-USD",
                    "tokenLiquidityUsd": 500000,
                    "tokenType": "CRYPTO"
                }
            ]
        }
        mock_request.return_value.json.return_value = mock_response
        mock_request.return_value.raise_for_status.return_value = None

        response = self.client.get_token_markets(token_mint="0x1234...", chain_id=1)

        self.assertIsInstance(response[0], TokenMarket)
        self.assertEqual(response[0].market_cap_usd, 1000000)
        self.assertEqual(response[0].market_id, "BTC-USD")
        self.assertEqual(response[0].token_liquidity_usd, 500000)
        self.assertEqual(response[0].token_type, "CRYPTO")
        mock_request.assert_called_once_with(
            "GET",
            "https://api.vyper.trade/api/v1/token/markets",
            params={"tokenMint": "0x1234...", "chainID": 1}
        )

    @patch("src.client.requests.Session.request")
    def test_get_token_metadata_success(self, mock_request):
        mock_response = {
            "status": "success",
            "message": "Token metadata retrieved successfully",
            "data": {
                "image": "https://example.com/token.png",
                "name": "Example Token",
                "symbol": "EXT",
                "telegram": "https://t.me/exampletoken",
                "twitter": "https://twitter.com/exampletoken",
                "website": "https://exampletoken.com"
            }
        }
        mock_request.return_value.json.return_value = mock_response
        mock_request.return_value.raise_for_status.return_value = None

        response = self.client.get_token_metadata(chain_id=1, token_mint="0x1234...")

        self.assertIsInstance(response, TokenMetadata)
        self.assertEqual(response.image, "https://example.com/token.png")
        self.assertEqual(response.name, "Example Token")
        self.assertEqual(response.symbol, "EXT")
        self.assertEqual(response.telegram, "https://t.me/exampletoken")
        self.assertEqual(response.twitter, "https://twitter.com/exampletoken")
        self.assertEqual(response.website, "https://exampletoken.com")
        mock_request.assert_called_once_with(
            "GET",
            "https://api.vyper.trade/api/v1/token/metadata",
            params={"chainID": 1, "tokenMint": "0x1234..."}
        )

    @patch("src.client.requests.Session.request")
    def test_get_token_symbol_success(self, mock_request):
        mock_response = {
            "status": "success",
            "message": "Token symbol retrieved successfully",
            "data": {
                "symbol": "EXT"
            }
        }
        mock_request.return_value.json.return_value = mock_response
        mock_request.return_value.raise_for_status.return_value = None

        response = self.client.get_token_symbol(chain_id=1, token_mint="0x1234...")

        self.assertIsInstance(response, TokenSymbol)
        self.assertEqual(response.symbol, "EXT")
        mock_request.assert_called_once_with(
            "GET",
            "https://api.vyper.trade/api/v1/token/symbol",
            params={"chainID": 1, "tokenMint": "0x1234..."}
        )
    
    @patch("src.client.requests.Session.request")
    def test_get_top_traders_success(self, mock_request):
        mock_response = {
            "status": "success",
            "message": "Top traders retrieved successfully",
            "data": [
                {
                    "investedAmount_tokens": 1000,
                    "investedAmount_usd": 5000,
                    "investedTxns": 10,
                    "pnlUsd": 500,
                    "remainingTokens": 800,
                    "remainingUsd": 4000,
                    "soldAmountTokens": 200,
                    "soldAmountUsd": 1500,
                    "soldTxns": 2,
                    "walletAddress": "0x1234...",
                    "walletTag": "Whale 1"
                }
            ]
        }
        mock_request.return_value.json.return_value = mock_response
        mock_request.return_value.raise_for_status.return_value = None

        response = self.client.get_top_traders(market_id="BTC-USD", chain_id=1)

        self.assertIsInstance(response[0], TopTrader)
        self.assertEqual(response[0].invested_amount_tokens, 1000)
        self.assertEqual(response[0].wallet_address, "0x1234...")
        mock_request.assert_called_once_with(
            "GET",
            "https://api.vyper.trade/api/v1/token/top-traders",
            params={"marketID": "BTC-USD", "chainID": 1}
        )

    @patch("src.client.requests.Session.request")
    def test_search_tokens_success(self, mock_request):
        mock_response = {
            "status": "success",
            "message": "Token search completed successfully",
            "data": [
                {
                    "chainId": 1,
                    "createdTimestamp": 1632825600,
                    "image": "https://example.com/token.png",
                    "marketId": "BTC-USD",
                    "name": "Bitcoin",
                    "percentChange24h": 2.5,
                    "pooledAsset": 1000000,
                    "symbol": "BTC",
                    "telegram": "https://t.me/bitcoin",
                    "tokenLiquidityUsd": 5000000,
                    "tokenMarketCapUsd": 1000000000,
                    "tokenMint": "0x2345...",
                    "tokenPriceUsd": 50000,
                    "tokenType": "CRYPTO",
                    "twitter": "https://twitter.com/bitcoin",
                    "volumeUsd": 10000000,
                    "website": "https://bitcoin.org"
                }
            ]
        }
        mock_request.return_value.json.return_value = mock_response
        mock_request.return_value.raise_for_status.return_value = None

        response = self.client.search_tokens(criteria="Bitcoin", chain_id=1)

        self.assertIsInstance(response[0], TokenSearchResult)
        self.assertEqual(response[0].name, "Bitcoin")
        self.assertEqual(response[0].symbol, "BTC")
        mock_request.assert_called_once_with(
            "GET",
            "https://api.vyper.trade/api/v1/token/search",
            params={"criteria": "Bitcoin", "chainID": 1}
        )
    
    @patch("src.client.requests.Session.request")
    def test_get_wallet_aggregated_pnl_success(self, mock_request):
        mock_response = {
            "status": "success",
            "message": "Wallet aggregated PnL retrieved successfully",
            "data": {
                "investedAmount": 1000.0,
                "pnlPercent": 10.5,
                "pnlUsd": 105.0,
                "soldAmount": 500.0,
                "tokensTraded": 100.0,
                "totalPnlPercent": 15.0,
                "totalPnlUsd": 150.0,
                "unrealizedPnlPercent": 4.5,
                "unrealizedPnlUsd": 45.0
            }
        }
        mock_request.return_value.json.return_value = mock_response
        mock_request.return_value.raise_for_status.return_value = None

        response = self.client.get_wallet_aggregated_pnl(wallet_address="0x1234...", chain_id=1)

        self.assertIsInstance(response, WalletAggregatedPnL)
        self.assertEqual(response.invested_amount, 1000.0)
        self.assertEqual(response.pnl_percent, 10.5)
        self.assertEqual(response.pnl_usd, 105.0)
        mock_request.assert_called_once_with(
            "GET",
            "https://api.vyper.trade/wallet/aggregated-pnl",
            params={"walletAddress": "0x1234...", "chainID": 1}
        )

    @patch("src.client.requests.Session.request")
    def test_get_wallet_holdings_success(self, mock_request):
        mock_response = {
            "status": "success",
            "message": "Wallet holdings retrieved successfully",
            "data": [
                {
                    "marketId": "BTC-USD",
                    "tokenHoldings": 0.5,
                    "tokenSymbol": "BTC",
                    "usdValue": 15000.0
                },
                {
                    "marketId": "ETH-USD",
                    "tokenHoldings": 2.0,
                    "tokenSymbol": "ETH",
                    "usdValue": 4000.0
                }
            ]
        }
        mock_request.return_value.json.return_value = mock_response
        mock_request.return_value.raise_for_status.return_value = None

        response = self.client.get_wallet_holdings(wallet_address="0x1234...", chain_id=1)

        self.assertIsInstance(response, list)
        self.assertEqual(len(response), 2)
        self.assertIsInstance(response[0], WalletHolding)
        self.assertEqual(response[0].market_id, "BTC-USD")
        self.assertEqual(response[0].token_holdings, 0.5)
        self.assertEqual(response[0].token_symbol, "BTC")
        self.assertEqual(response[0].usd_value, 15000.0)
        mock_request.assert_called_once_with(
            "GET",
            "https://api.vyper.trade/wallet/holdings",
            params={"walletAddress": "0x1234...", "chainID": 1}
        )

    @patch("src.client.requests.Session.request")
    def test_get_wallet_pnl_success(self, mock_request):
        mock_response = {
            "status": "success",
            "message": "Wallet PnL retrieved successfully",
            "data": {
                "holderSince": 1632825600,
                "investedAmount": 1000.0,
                "investedTxns": 5,
                "pnlPercent": 10.5,
                "pnlUsd": 105.0,
                "remainingTokens": 0.75,
                "remainingUsd": 750.0,
                "soldAmount": 250.0,
                "soldTxns": 2
            }
        }
        mock_request.return_value.json.return_value = mock_response
        mock_request.return_value.raise_for_status.return_value = None

        response = self.client.get_wallet_pnl(wallet_address="0x1234...", market_id="BTC-USD", chain_id=1)

        self.assertIsInstance(response, WalletPnL)
        self.assertEqual(response.holder_since, 1632825600)
        self.assertEqual(response.invested_amount, 1000.0)
        self.assertEqual(response.invested_txns, 5)
        self.assertEqual(response.pnl_percent, 10.5)
        self.assertEqual(response.pnl_usd, 105.0)
        mock_request.assert_called_once_with(
            "GET",
            "https://api.vyper.trade/wallet/pnl",
            params={"walletAddress": "0x1234...", "marketID": "BTC-USD", "chainID": 1}
        )

    @patch("src.client.requests.Session.request")
    def test_wallet_functions_authentication_error(self, mock_request):
        mock_response = Mock()
        mock_response.status_code = 401
        mock_response.json.return_value = {"error": "Invalid or expired API key"}
        mock_request.return_value = mock_response
        mock_request.return_value.raise_for_status.side_effect = requests.exceptions.HTTPError(response=mock_response)

        with self.assertRaises(AuthenticationError):
            self.client.get_wallet_aggregated_pnl(wallet_address="0x1234...", chain_id=1)

        with self.assertRaises(AuthenticationError):
            self.client.get_wallet_holdings(wallet_address="0x1234...", chain_id=1)

        with self.assertRaises(AuthenticationError):
            self.client.get_wallet_pnl(wallet_address="0x1234...", market_id="BTC-USD", chain_id=1)

    @patch("src.client.requests.Session.request")
    def test_wallet_functions_rate_limit_error(self, mock_request):
        mock_response = Mock()
        mock_response.status_code = 429
        mock_response.json.return_value = {"error": "Rate limit exceeded"}
        mock_response.headers = {'Retry-After': '60'}
        mock_request.return_value = mock_response
        mock_request.return_value.raise_for_status.side_effect = requests.exceptions.HTTPError(response=mock_response)

        with self.assertRaises(RateLimitError) as context:
            self.client.get_wallet_aggregated_pnl(wallet_address="0x1234...", chain_id=1)
        self.assertEqual(context.exception.retry_after, 60.0)

        with self.assertRaises(RateLimitError) as context:
            self.client.get_wallet_holdings(wallet_address="0x1234...", chain_id=1)
        self.assertEqual(context.exception.retry_after, 60.0)

        with self.assertRaises(RateLimitError) as context:
            self.client.get_wallet_pnl(wallet_address="0x1234...", market_id="BTC-USD", chain_id=1)
        self.assertEqual(context.exception.retry_after, 60.0)
    
    @patch("src.client.requests.Session.request")
    def test_get_token_pairs_success(self, mock_request):
        mock_response = {
            "status": "success",
            "message": "Token pairs retrieved successfully",
            "data": {
                "hasNext": True,
                "pairs": [
                    {
                        "abused": False,
                        "bondingCurvePercentage": 0.5,
                        "buyTxnCount": 100,
                        "chainId": 1,
                        "contractCreator": "0x1234...",
                        "createdTimestamp": 1632825600,
                        "description": "Test Token",
                        "freezeAuthority": False,
                        "image": "https://example.com/token.png",
                        "initialAssetLiquidity": 1000,
                        "initialUsdLiquidity": 1000,
                        "isMigrated": False,
                        "lpBurned": True,
                        "lpCreator": "0x5678...",
                        "marketId": "TEST-USD",
                        "metadataUri": "https://example.com/metadata.json",
                        "migratedMarketId": "",
                        "migrationState": {
                            "durationMinutes": 0,
                            "makers": 0,
                            "migrationTimestamp": 0,
                            "volume": 0
                        },
                        "mintAuthority": True,
                        "name": "Test Token",
                        "pooledAsset": 1000,
                        "pooledToken": 1000,
                        "priceChangePercent": 5.0,
                        "sellTxnCount": 50,
                        "symbol": "TEST",
                        "telegram": "https://t.me/testtoken",
                        "tokenLiquidityAsset": 900,
                        "tokenLiquidityUsd": 900,
                        "tokenMarketCapAsset": 10000,
                        "tokenMarketCapUsd": 10000,
                        "tokenMint": "0x9876...",
                        "tokenPriceAsset": 1,
                        "tokenPriceUsd": 1,
                        "tokenType": "ERC20",
                        "top10HoldingPercent": 30,
                        "totalSupply": 1000000,
                        "transactionCount": 150,
                        "twitter": "https://twitter.com/testtoken",
                        "volumeAsset": 5000,
                        "volumeUsd": 5000,
                        "website": "https://testtoken.com"
                    }
                ]
            }
        }
        mock_request.return_value.json.return_value = mock_response
        mock_request.return_value.raise_for_status.return_value = None

        response = self.client.get_token_pairs(chain_ids="1", liquidity_min=100, page=1)

        self.assertIsInstance(response, TokenPairs)
        self.assertTrue(response.has_next)
        self.assertEqual(len(response.pairs), 1)
        self.assertIsInstance(response.pairs[0], TokenPair)
        self.assertEqual(response.pairs[0].market_id, "TEST-USD")
        self.assertEqual(response.pairs[0].symbol, "TEST")
        self.assertIsInstance(response.pairs[0].migration_state, MigrationState)
        
        mock_request.assert_called_once_with(
        "GET",
        "https://api.vyper.trade/token/pairs",
        params={'chain_ids': '1', 'liquidity_min': 100, 'page': 1}
    )

if __name__ == "__main__":
    unittest.main()