import requests
from typing import Dict, Any, List, Optional
from dataclasses import fields
from .utils import camel_to_snake
from .exceptions import AuthenticationError, RateLimitError, ServerError, VyperApiException
from .classes import APIResponse, TokenHolder, TokenATH, MigrationState, TokenPair, TokenMarket, TokenMetadata, TokenSymbol, TopTrader, TokenSearchResult, WalletAggregatedPnL, WalletHolding, WalletPnL, TokenPairs

class VyperClient:
    def __init__(self, api_key=None):
        self.base_url = "https://api.vyper.trade"
        self.api_key = api_key
        self.session = requests.Session()
        if api_key:
            self.session.headers.update({"X-API-Key": self.api_key})

    def _request(self, method, endpoint, **kwargs) -> APIResponse:
        url = f"{self.base_url}{endpoint}"
        try:
            response = self.session.request(method, url, **kwargs)
            response.raise_for_status()
            json_response = response.json()
            return APIResponse(
                status=json_response.get('status'),
                message=json_response.get('message'),
                data=json_response.get('data')
            )
        except requests.exceptions.HTTPError as e:
            if e.response.status_code == 401:
                raise AuthenticationError("Invalid or expired API key", status_code=401, response=e.response)
            elif e.response.status_code == 429:
                retry_after = e.response.headers.get('Retry-After', '3.00')
                raise RateLimitError(f"Rate limit exceeded. Please wait {retry_after} seconds before making another request.", retry_after=float(retry_after))
            elif 500 <= e.response.status_code < 600:
                raise ServerError(f"Server error: {e.response.status_code}", status_code=e.response.status_code, response=e.response)
            else:
                raise VyperApiException(f"HTTP error occurred: {e}", status_code=e.response.status_code, response=e.response)
        except requests.exceptions.RequestException as e:
            raise VyperApiException(f"An error occurred: {e}")

    def get(self, endpoint, params=None) -> APIResponse:
        return self._request("GET", endpoint, params=params)

    def post(self, endpoint, data=None, json=None) -> APIResponse:
        return self._request("POST", endpoint, data=data, json=json)

    def put(self, endpoint, data=None, json=None) -> APIResponse:
        return self._request("PUT", endpoint, data=data, json=json)

    def delete(self, endpoint) -> APIResponse:
        return self._request("DELETE", endpoint)

    def get_chain_ids(self) -> Dict[str, int]:
        """
        Retrieve the chain IDs supported by the API.
        
        Returns:
            Dict[str, int]: A dictionary containing the chain IDs and their corresponding values.
        
        Note:
            This endpoint does not require an API key.
        """
        original_headers = self.session.headers.copy()
        self.session.headers.pop("X-API-Key", None)
        try:
            response = self.get("/api/v1/chain/ids")
            return response.data
        finally:
            self.session.headers = original_headers

    def get_token_ath(self, chain_id: int, market_id: str) -> TokenATH:
        """
        Retrieve all-time high market cap, liquidity, and timestamp for a token based on chain ID and market ID.

        Args:
            chain_id (int): The chain ID.
            market_id (str): The market ID.

        Returns:
            TokenATH: An object containing the all-time high data for the specified token.

        Raises:
            AuthenticationError: If the API key is invalid or expired.
            RateLimitError: If the rate limit is exceeded.
            ServerError: If a server error occurs.
            VyperApiException: For other API-related errors.

        Note:
            This endpoint requires an API key.
        """
        if not self.api_key:
            raise AuthenticationError("API key is required for this endpoint")

        params = {
            "chainID": chain_id,
            "marketID": market_id
        }
        response = self.get("/api/v1/token/ath", params=params)
        return TokenATH(**{camel_to_snake(k): v for k, v in response.data.items()})

    def get_token_market(self, market_id: str, chain_id: int = 900, interval: str = "24h") -> TokenPair:
        """
        Retrieve detailed information about a token using its market ID.

        Args:
            market_id (str): Market ID of the token.
            chain_id (int, optional): Chain ID. Defaults to 900.
            interval (str, optional): Time interval. Available values: 5m, 1h, 6h, 24h. Defaults to "24h".

        Returns:
            Market: An object containing detailed information about the token.

        Raises:
            AuthenticationError: If the API key is invalid or expired.
            RateLimitError: If the rate limit is exceeded.
            ServerError: If a server error occurs.
            VyperApiException: For other API-related errors.
        """
        if not self.api_key:
            raise AuthenticationError("API key is required for this endpoint")

        params = {
            "chainID": chain_id,
            "interval": interval
        }
        response = self.get(f"/api/v1/token/market/{market_id}", params=params)
        data = response.data
        data['migration_state'] = MigrationState(**{camel_to_snake(k): v for k, v in data['migrationState'].items()})
        return TokenPair(**{camel_to_snake(k): v for k, v in data.items()})

    def get_token_holders(self, market_id: str, chain_id: int) -> Dict[str, Any]:
        """
        Retrieve token holders information.

        Args:
            market_id (str): Market ID of the token.
            chain_id (int): Chain ID.

        Returns:
            Dict[str, Any]: A dictionary containing token holders information and total holders count.

        Raises:
            AuthenticationError: If the API key is invalid or expired.
            RateLimitError: If the rate limit is exceeded.
            ServerError: If a server error occurs.
            VyperApiException: For other API-related errors.
        """
        if not self.api_key:
            raise AuthenticationError("API key is required for this endpoint")

        params = {
            "marketID": market_id,
            "chainID": chain_id
        }
        response = self.get("/api/v1/token/holders", params=params)
        data = response.data
        holders = [TokenHolder(**{camel_to_snake(k): v for k, v in holder.items()}) for holder in data['holders']]
        return {
            'holders': holders,
            'total_holders': data['total_holders']
        }
        
    def get_token_markets(self, token_mint: str, chain_id: int) -> List[TokenMarket]:
        """
        Retrieve market IDs and token types for a token based on token mint and chain ID.

        Args:
            token_mint (str): Token mint address
            chain_id (int): Chain ID

        Returns:
            List[TokenMarket]: A list of TokenMarket objects containing market information for the token

        Raises:
            AuthenticationError: If the API key is invalid or expired
            RateLimitError: If the rate limit is exceeded
            ServerError: If a server error occurs
            VyperApiException: For other API-related errors
        """
        if not self.api_key:
            raise AuthenticationError("API key is required for this endpoint")

        params = {
            "tokenMint": token_mint,
            "chainID": chain_id
        }
        response = self.get("/api/v1/token/markets", params=params)
        return [TokenMarket(**{camel_to_snake(k): v for k, v in market.items()}) for market in response.data]

    def get_token_metadata(self, chain_id: int, token_mint: str) -> TokenMetadata:
        """
        Retrieve metadata for a token based on chain ID and token mint.

        Args:
            chain_id (int): Chain ID
            token_mint (str): Token mint address

        Returns:
            TokenMetadata: An object containing token metadata

        Raises:
            AuthenticationError: If the API key is invalid or expired
            RateLimitError: If the rate limit is exceeded
            ServerError: If a server error occurs
            VyperApiException: For other API-related errors
        """
        if not self.api_key:
            raise AuthenticationError("API key is required for this endpoint")

        params = {
            "chainID": chain_id,
            "tokenMint": token_mint
        }
        response = self.get("/api/v1/token/metadata", params=params)
        return TokenMetadata(**response.data)

    def get_token_symbol(self, chain_id: int, token_mint: str) -> TokenSymbol:
        """
        Retrieve the symbol for a token based on chain ID and token mint.

        Args:
            chain_id (int): Chain ID
            token_mint (str): Token mint address

        Returns:
            TokenSymbol: An object containing the token symbol

        Raises:
            AuthenticationError: If the API key is invalid or expired
            RateLimitError: If the rate limit is exceeded
            ServerError: If a server error occurs
            VyperApiException: For other API-related errors
        """
        if not self.api_key:
            raise AuthenticationError("API key is required for this endpoint")

        params = {
            "chainID": chain_id,
            "tokenMint": token_mint
        }
        response = self.get("/api/v1/token/symbol", params=params)
        return TokenSymbol(**response.data)

    def get_top_traders(self, market_id: str, chain_id: int) -> List[TopTrader]:
        """
        Retrieve the top traders for a specific token.

        Args:
            market_id (str): Market ID of the token
            chain_id (int): Chain ID

        Returns:
            List[TopTrader]: A list of TopTrader objects containing top trader information

        Raises:
            AuthenticationError: If the API key is invalid or expired
            RateLimitError: If the rate limit is exceeded
            ServerError: If a server error occurs
            VyperApiException: For other API-related errors
        """
        if not self.api_key:
            raise AuthenticationError("API key is required for this endpoint")

        params = {
            "marketID": market_id,
            "chainID": chain_id
        }
        response = self.get("/api/v1/token/top-traders", params=params)
        return [TopTrader(**{
            field.name: trader[field.metadata['alias']]
            for field in fields(TopTrader)
            if field.metadata.get('alias') in trader
        }) for trader in response.data]

    def search_tokens(self, criteria: str, chain_id: int = None) -> List[TokenSearchResult]:
        """
        Search for tokens by name, symbol, or address.

        Args:
            criteria (str): Search criteria (name, symbol, or address)
            chain_id (int, optional): Chain ID to filter results

        Returns:
            List[TokenSearchResult]: A list of TokenSearchResult objects containing search results

        Raises:
            AuthenticationError: If the API key is invalid or expired
            RateLimitError: If the rate limit is exceeded
            ServerError: If a server error occurs
            VyperApiException: For other API-related errors
        """
        if not self.api_key:
            raise AuthenticationError("API key is required for this endpoint")

        params = {
            "criteria": criteria
        }
        if chain_id is not None:
            params["chainID"] = chain_id

        response = self.get("/api/v1/token/search", params=params)
        return [TokenSearchResult(**{
            field.name: token.get(field.metadata.get('alias', field.name), None)
            for field in fields(TokenSearchResult)
        }) for token in response.data]

    def get_wallet_holdings(self, wallet_address: str, chain_id: int) -> List[WalletHolding]:
        """
        Retrieve the token holdings for a specific wallet.

        Args:
            wallet_address (str): Wallet address to query.
            chain_id (int): Chain ID of the network.

        Returns:
            List[WalletHolding]: List of token holdings for the specified wallet.
        
        Raises:
            AuthenticationError: If the API key is invalid or expired
            RateLimitError: If the rate limit is exceeded
            ServerError: If a server error occurs
            VyperApiException: For other API-related errors
        """
        params = {
            "walletAddress": wallet_address,
            "chainID": chain_id
        }
        response = self.get("/api/v1/wallet/holdings", params=params)
        return [WalletHolding(**{
            field.name: holding[field.metadata['alias']]
            for field in fields(WalletHolding)
            if field.metadata.get('alias') in holding
        }) for holding in response.data]

    def get_wallet_aggregated_pnl(self, wallet_address: str, chain_id: int) -> WalletAggregatedPnL:
        """
        Retrieve aggregated Profit and Loss data for a wallet across all its transactions.

        Args:
            wallet_address (str): Wallet address to query.
            chain_id (int): Chain ID of the network.

        Returns:
            WalletAggregatedPnL: Aggregated Profit and Loss data for the wallet.
        
        Raises:
            AuthenticationError: If the API key is invalid or expired
            RateLimitError: If the rate limit is exceeded
            ServerError: If a server error occurs
            VyperApiException: For other API-related errors
        """
        params = {
            "walletAddress": wallet_address,
            "chainID": chain_id
        }
        response = self.get("/api/v1/wallet/aggregated-pnl", params=params)
        return WalletAggregatedPnL(**{
            field.name: response.data[field.metadata['alias']]
            for field in fields(WalletAggregatedPnL)
            if field.metadata.get('alias') in response.data
        })

    def get_wallet_pnl(self, wallet_address: str, market_id: str, chain_id: int) -> WalletPnL:
        """
        Retrieve Profit and Loss data for a trader based on wallet address, market ID, and chain ID.

        Args:
            wallet_address (str): Wallet address of the trader.
            market_id (str): Market ID for the query.
            chain_id (int): Chain ID of the network.

        Returns:
            WalletPnL: Profit and Loss data for the specified wallet and market.
        
        Raises:
            AuthenticationError: If the API key is invalid or expired
            RateLimitError: If the rate limit is exceeded
            ServerError: If a server error occurs
            VyperApiException: For other API-related errors
        """
        params = {
            "walletAddress": wallet_address,
            "marketID": market_id,
            "chainID": chain_id
        }
        response = self.get("/api/v1/wallet/pnl", params=params)
        return WalletPnL(**{
            field.name: response.data[field.metadata['alias']]
            for field in fields(WalletPnL)
            if field.metadata.get('alias') in response.data
        })
    
    def get_token_pairs(self, 
                        at_least_one_social: Optional[bool] = None,
                        buys_max: Optional[int] = None,
                        buys_min: Optional[int] = None,
                        chain_ids: Optional[str] = None,
                        freeze_auth_disabled: Optional[bool] = None,
                        initial_liquidity_max: Optional[float] = None,
                        initial_liquidity_min: Optional[float] = None,
                        interval: Optional[str] = None,
                        liquidity_max: Optional[float] = None,
                        liquidity_min: Optional[float] = None,
                        lp_burned: Optional[bool] = None,
                        market_cap_max: Optional[float] = None,
                        market_cap_min: Optional[float] = None,
                        mint_auth_disabled: Optional[bool] = None,
                        page: Optional[int] = None,
                        sells_max: Optional[int] = None,
                        sells_min: Optional[int] = None,
                        sorting: Optional[str] = None,
                        swaps_max: Optional[int] = None,
                        swaps_min: Optional[int] = None,
                        token_types: Optional[str] = None,
                        top10_holders: Optional[bool] = None,
                        volume_max: Optional[float] = None,
                        volume_min: Optional[float] = None) -> TokenPairs:
        """
        Retrieve a list of token pairs based on specified criteria.

        Args:
            at_least_one_social (Optional[bool]): Filter for tokens with at least one social media link.
            buys_max (Optional[int]): Maximum number of buy transactions.
            buys_min (Optional[int]): Minimum number of buy transactions.
            chain_ids (Optional[str]): Comma-separated list of chain IDs.
            freeze_auth_disabled (Optional[bool]): Filter for tokens with freeze authority disabled.
            initial_liquidity_max (Optional[float]): Maximum initial liquidity in USD.
            initial_liquidity_min (Optional[float]): Minimum initial liquidity in USD.
            interval (Optional[str]): Time interval for data.
            liquidity_max (Optional[float]): Maximum current liquidity in USD.
            liquidity_min (Optional[float]): Minimum current liquidity in USD.
            lp_burned (Optional[bool]): Filter for tokens with LP tokens burned.
            market_cap_max (Optional[float]): Maximum market cap in USD.
            market_cap_min (Optional[float]): Minimum market cap in USD.
            mint_auth_disabled (Optional[bool]): Filter for tokens with mint authority disabled.
            page (Optional[int]): Page number for pagination.
            sells_max (Optional[int]): Maximum number of sell transactions.
            sells_min (Optional[int]): Minimum number of sell transactions.
            sorting (Optional[str]): Sorting criteria.
            swaps_max (Optional[int]): Maximum number of swap transactions.
            swaps_min (Optional[int]): Minimum number of swap transactions.
            token_types (Optional[str]): Comma-separated list of token types.
            top10_holders (Optional[bool]): Filter for tokens where top 10 holders own more than 50%.
            volume_max (Optional[float]): Maximum trading volume in USD.
            volume_min (Optional[float]): Minimum trading volume in USD.

        Returns:
            TokenPairs: An object containing the list of token pairs and pagination info.

        Raises:
            AuthenticationError: If the API key is invalid or expired.
            RateLimitError: If the rate limit is exceeded.
            ServerError: If a server error occurs.
            VyperApiException: For other API-related errors.
        """
        params: Dict[str, Any] = {
            k: v for k, v in locals().items() 
            if k != 'self' and v is not None
        }
        
        response = self.get("/api/v1/token/pairs", params=params)
        
        pairs = [TokenPair(**{
        field.name: pair.get(field.metadata.get('alias', field.name))
        for field in fields(TokenPair)
        }) for pair in response.data['pairs']]
        
        for pair in pairs:
            if pair.migration_state:
                pair.migration_state = MigrationState(**{
                    camel_to_snake(k): v for k, v in pair.migration_state.items()
                })
        
        return TokenPairs(has_next=response.data['hasNext'], pairs=pairs)