from dataclasses import dataclass
from typing import Any, Optional, List
from .utils import field_alias

@dataclass
class APIResponse:
    status: str
    message: str
    data: Any

@dataclass
class WalletAggregatedPnL:
    invested_amount: float = field_alias('investedAmount')
    pnl_percent: float = field_alias('pnlPercent')
    pnl_usd: float = field_alias('pnlUsd')
    sold_amount: float = field_alias('soldAmount')
    tokens_traded: int = field_alias('tokensTraded')  # Changed to int
    total_pnl_percent: float = field_alias('totalPnlPercent')
    total_pnl_usd: float = field_alias('totalPnlUsd')
    unrealized_pnl_percent: float = field_alias('unrealizedPnlPercent')
    unrealized_pnl_usd: float = field_alias('unrealizedPnlUsd')

@dataclass
class WalletHolding:
    market_id: str = field_alias('marketId')
    token_holdings: float = field_alias('tokenHoldings')
    token_symbol: str = field_alias('tokenSymbol')
    usd_value: float = field_alias('usdValue')

@dataclass
class WalletPnL:
    holder_since: int = field_alias('holderSince')
    invested_amount: float = field_alias('investedAmount')
    invested_txns: int = field_alias('investedTxns')
    pnl_percent: float = field_alias('pnlPercent')
    pnl_usd: float = field_alias('pnlUsd')
    remaining_tokens: float = field_alias('remainingTokens')
    remaining_usd: float = field_alias('remainingUsd')
    sold_amount: float = field_alias('soldAmount')
    sold_txns: int = field_alias('soldTxns')

@dataclass
class TopTrader:
    invested_amount_tokens: float = field_alias('investedAmount_tokens')
    invested_amount_usd: float = field_alias('investedAmount_usd')
    invested_txns: int = field_alias('investedTxns')
    pnl_usd: float = field_alias('pnlUsd')
    remaining_tokens: float = field_alias('remainingTokens')
    remaining_usd: float = field_alias('remainingUsd')
    sold_amount_tokens: float = field_alias('soldAmountTokens')
    sold_amount_usd: float = field_alias('soldAmountUsd')
    sold_txns: int = field_alias('soldTxns')
    wallet_address: str = field_alias('walletAddress')
    wallet_tag: Optional[str] = field_alias('walletTag')

@dataclass
class TokenSearchResult:
    chain_id: int = field_alias('chainId')
    market_id: str = field_alias('marketId')
    created_timestamp: int = field_alias('createdTimestamp')
    name: str
    symbol: str
    token_mint: str = field_alias('tokenMint')
    token_type: str = field_alias('tokenType')
    percent_change_24h: float = field_alias('percentChange24h')
    pooled_asset: float = field_alias('pooledAsset')
    token_liquidity_usd: float = field_alias('tokenLiquidityUsd')
    token_market_cap_usd: float = field_alias('tokenMarketCapUsd')
    token_price_usd: float = field_alias('tokenPriceUsd')
    volume_usd: float = field_alias('volumeUsd')
    image: Optional[str] = None
    telegram: Optional[str] = None
    twitter: Optional[str] = None
    website: Optional[str] = None

@dataclass
class TokenMarket:
    market_cap_usd: float = field_alias('marketCapUsd')
    market_id: str = field_alias('marketID')
    token_liquidity_usd: float = field_alias('tokenLiquidityUsd')
    token_type: str = field_alias('tokenType')

@dataclass
class TokenMetadata:
    image: Optional[str]
    name: str
    symbol: str
    telegram: Optional[str]
    twitter: Optional[str]
    website: Optional[str]

@dataclass
class TokenSymbol:
    symbol: str

@dataclass
class TokenHolder:
    percent_owned: float = field_alias('percentOwned')
    token_holdings: float = field_alias('tokenHoldings')
    usd_holdings: float = field_alias('usdHoldings')
    wallet_address: str = field_alias('walletAddress')
    wallet_tag: Optional[str] = field_alias('walletTag')

@dataclass
class TokenATH:
    market_cap_usd: float = field_alias('marketCapUsd')
    timestamp: int
    token_liquidity_usd: float = field_alias('tokenLiquidityUsd')

@dataclass
class MigrationState:
    duration_minutes: int = field_alias('durationMinutes')
    makers: int
    migration_timestamp: int = field_alias('migrationTimestamp')
    volume: float

@dataclass
class TokenPair:
    abused: Optional[bool]
    bonding_curve_percentage: Optional[float] = field_alias('bondingCurvePercentage')
    buy_txn_count: int = field_alias('buyTxnCount')
    chain_id: int = field_alias('chainId')
    contract_creator: str = field_alias('contractCreator')
    created_timestamp: int = field_alias('createdTimestamp')
    description: Optional[str]
    freeze_authority: Optional[bool] = field_alias('freezeAuthority')
    image: Optional[str]
    initial_asset_liquidity: float = field_alias('initialAssetLiquidity')
    initial_usd_liquidity: float = field_alias('initialUsdLiquidity')
    is_migrated: Optional[bool] = field_alias('isMigrated')
    lp_burned: bool = field_alias('lpBurned')
    lp_creator: str = field_alias('lpCreator')
    market_id: str = field_alias('marketId')
    metadata_uri: Optional[str] = field_alias('metadataUri')
    migrated_market_id: Optional[str] = field_alias('migratedMarketId')
    migration_state: Optional[MigrationState] = field_alias('migrationState')
    mint_authority: Optional[bool] = field_alias('mintAuthority')
    name: str
    pooled_asset: float = field_alias('pooledAsset')
    pooled_token: float = field_alias('pooledToken')
    price_change_percent: float = field_alias('priceChangePercent')
    sell_txn_count: int = field_alias('sellTxnCount')
    symbol: str
    telegram: Optional[str]
    token_liquidity_asset: float = field_alias('tokenLiquidityAsset')
    token_liquidity_usd: float = field_alias('tokenLiquidityUsd')
    token_market_cap_asset: float = field_alias('tokenMarketCapAsset')
    token_market_cap_usd: float = field_alias('tokenMarketCapUsd')
    token_mint: str = field_alias('tokenMint')
    token_price_asset: float = field_alias('tokenPriceAsset')
    token_price_usd: float = field_alias('tokenPriceUsd')
    token_type: str = field_alias('tokenType')
    top10_holding_percent: float = field_alias('top10HoldingPercent')
    total_supply: float = field_alias('totalSupply')
    transaction_count: int = field_alias('transactionCount')
    twitter: Optional[str]
    volume_asset: float = field_alias('volumeAsset')
    volume_usd: float = field_alias('volumeUsd')
    website: Optional[str]

@dataclass
class ChainAction:
    signer: str
    transaction_id: str
    market_id: str
    action_type: str
    token_amount: float
    asset_amount: float
    token_price_usd: float
    token_price_asset: float
    token_market_cap_asset: float
    token_market_cap_usd: float
    token_liquidity_asset: float
    token_liquidity_usd: float
    pooled_token: float
    pooled_asset: float
    action_timestamp: int
    token_account: Optional[str] = None
    token_mint: Optional[str] = None
    swap_total_usd: Optional[float] = None
    swap_total_asset: Optional[float] = None
    bonding_curve_percentage: Optional[float] = None
    bot_used: Optional[str] = None


@dataclass
class TokenPairs:
    has_next: bool = field_alias('hasNext')
    pairs: List[TokenPair]