# ruff: noqa: D200
# ruff: noqa: D204
# ruff: noqa: D205
# ruff: noqa: D404
# ruff: noqa: W291
# ruff: noqa: D400
# ruff: noqa: E501
from dataclasses import dataclass
from enum import Enum


class CandlestickInterval(Enum):
    # 1 minute
    CI_1_M = "CI_1_M"
    # 3 minutes
    CI_3_M = "CI_3_M"
    # 5 minutes
    CI_5_M = "CI_5_M"
    # 15 minutes
    CI_15_M = "CI_15_M"
    # 30 minutes
    CI_30_M = "CI_30_M"
    # 1 hour
    CI_1_H = "CI_1_H"
    # 2 hour
    CI_2_H = "CI_2_H"
    # 4 hour
    CI_4_H = "CI_4_H"
    # 6 hour
    CI_6_H = "CI_6_H"
    # 8 hour
    CI_8_H = "CI_8_H"
    # 12 hour
    CI_12_H = "CI_12_H"
    # 1 day
    CI_1_D = "CI_1_D"
    # 3 days
    CI_3_D = "CI_3_D"
    # 5 days
    CI_5_D = "CI_5_D"
    # 1 week
    CI_1_W = "CI_1_W"
    # 2 weeks
    CI_2_W = "CI_2_W"
    # 3 weeks
    CI_3_W = "CI_3_W"
    # 4 weeks
    CI_4_W = "CI_4_W"


class CandlestickType(Enum):
    # Tracks traded prices
    TRADE = "TRADE"
    # Tracks mark prices
    MARK = "MARK"
    # Tracks index prices
    INDEX = "INDEX"
    # Tracks book mid prices
    MID = "MID"


class Currency(Enum):
    # the USDC token
    USDC = "USDC"
    # the USDT token
    USDT = "USDT"
    # the ETH token
    ETH = "ETH"
    # the BTC token
    BTC = "BTC"


class InstrumentSettlementPeriod(Enum):
    # Instrument settles through perpetual hourly funding cycles
    PERPETUAL = "PERPETUAL"
    # Instrument settles at an expiry date, marked as a daily instrument
    DAILY = "DAILY"
    # Instrument settles at an expiry date, marked as a weekly instrument
    WEEKLY = "WEEKLY"
    # Instrument settles at an expiry date, marked as a monthly instrument
    MONTHLY = "MONTHLY"
    # Instrument settles at an expiry date, marked as a quarterly instrument
    QUARTERLY = "QUARTERLY"


class Kind(Enum):
    # the perpetual asset kind
    PERPETUAL = "PERPETUAL"
    # the future asset kind
    FUTURE = "FUTURE"
    # the call option asset kind
    CALL = "CALL"
    # the put option asset kind
    PUT = "PUT"


class MarginType(Enum):
    # Simple Cross Margin Mode: all assets have a predictable margin impact, the whole subaccount shares a single margin
    SIMPLE_CROSS_MARGIN = "SIMPLE_CROSS_MARGIN"
    # Portfolio Cross Margin Mode: asset margin impact is analysed on portfolio level, the whole subaccount shares a single margin
    PORTFOLIO_CROSS_MARGIN = "PORTFOLIO_CROSS_MARGIN"


class OrderRejectReason(Enum):
    # client called a Cancel API
    CLIENT_CANCEL = "CLIENT_CANCEL"
    # client called a Bulk Cancel API
    CLIENT_BULK_CANCEL = "CLIENT_BULK_CANCEL"
    # client called a Session Cancel API, or set the WebSocket connection to 'cancelOrdersOnTerminate'
    CLIENT_SESSION_END = "CLIENT_SESSION_END"
    # the market order was cancelled after no/partial fill. Takes precedence over other TimeInForce cancel reasons
    MARKET_CANCEL = "MARKET_CANCEL"
    # the IOC order was cancelled after no/partial fill
    IOC_CANCEL = "IOC_CANCEL"
    # the AON order was cancelled as it could not be fully matched
    AON_CANCEL = "AON_CANCEL"
    # the FOK order was cancelled as it could not be fully matched
    FOK_CANCEL = "FOK_CANCEL"
    # the order was cancelled as it has expired
    EXPIRED = "EXPIRED"
    # the post-only order could not be posted into the orderbook
    FAIL_POST_ONLY = "FAIL_POST_ONLY"
    # the reduce-only order would have caused position size to increase
    FAIL_REDUCE_ONLY = "FAIL_REDUCE_ONLY"
    # the order was cancelled due to market maker protection trigger
    MM_PROTECTION = "MM_PROTECTION"
    # the order was cancelled due to self-trade protection trigger
    SELF_TRADE_PROTECTION = "SELF_TRADE_PROTECTION"
    # the order matched with another order from the same sub account
    SELF_MATCHED_SUBACCOUNT = "SELF_MATCHED_SUBACCOUNT"
    # an active order on your sub account shares the same clientOrderId
    OVERLAPPING_CLIENT_ORDER_ID = "OVERLAPPING_CLIENT_ORDER_ID"
    # the order will bring the sub account below initial margin requirement
    BELOW_MARGIN = "BELOW_MARGIN"
    # the sub account is liquidated (and all open orders are cancelled by Gravity)
    LIQUIDATION = "LIQUIDATION"
    # instrument is invalid or not found on Gravity
    INSTRUMENT_INVALID = "INSTRUMENT_INVALID"
    # instrument is no longer tradable on Gravity. (typically due to a market halt, or instrument expiry)
    INSTRUMENT_DEACTIVATED = "INSTRUMENT_DEACTIVATED"
    # system failover resulting in loss of order state
    SYSTEM_FAILOVER = "SYSTEM_FAILOVER"
    # the credentials used (userSession/apiKeySession/walletSignature) is not authorised to perform the action
    UNAUTHORISED = "UNAUTHORISED"
    # the session key used to sign the order expired
    SESSION_KEY_EXPIRED = "SESSION_KEY_EXPIRED"
    # the subaccount does not exist
    SUB_ACCOUNT_NOT_FOUND = "SUB_ACCOUNT_NOT_FOUND"
    # the signature used to sign the order has no trade permission
    NO_TRADE_PERMISSION = "NO_TRADE_PERMISSION"
    # the order payload does not contain a supported TimeInForce value
    UNSUPPORTED_TIME_IN_FORCE = "UNSUPPORTED_TIME_IN_FORCE"
    # the order has multiple legs, but multiple legs are not supported by this venue
    MULTI_LEGGED_ORDER = "MULTI_LEGGED_ORDER"


class OrderStateFilter(Enum):
    # create only filter
    C = "C"
    # update only filter
    U = "U"
    # create and update filter
    A = "A"


class OrderStatus(Enum):
    # Order is waiting for Trigger Condition to be hit
    PENDING = "PENDING"
    # Order is actively matching on the orderbook, could be unfilled or partially filled
    OPEN = "OPEN"
    # Order is fully filled and hence closed
    FILLED = "FILLED"
    # Order is rejected by GRVT Backend since if fails a particular check (See OrderRejectReason)
    REJECTED = "REJECTED"
    # Order is cancelled by the user using one of the supported APIs (See OrderRejectReason)
    CANCELLED = "CANCELLED"


class SubAccountTradeInterval(Enum):
    # 1 month
    SAT_1_MO = "SAT_1_MO"
    # 1 day
    SAT_1_D = "SAT_1_D"


class TimeInForce(Enum):
    """
    |                       | Must Fill All | Can Fill Partial |
    | -                     | -             | -                |
    | Must Fill Immediately | FOK           | IOC              |
    | Can Fill Till Time    | AON           | GTC              |

    """

    # GTT - Remains open until it is cancelled, or expired
    GOOD_TILL_TIME = "GOOD_TILL_TIME"
    # AON - Either fill the whole order or none of it (Block Trades Only)
    ALL_OR_NONE = "ALL_OR_NONE"
    # IOC - Fill the order as much as possible, when hitting the orderbook. Then cancel it
    IMMEDIATE_OR_CANCEL = "IMMEDIATE_OR_CANCEL"
    # FOK - Both AoN and IoC. Either fill the full order when hitting the orderbook, or cancel it
    FILL_OR_KILL = "FILL_OR_KILL"


class Venue(Enum):
    # the trade is cleared on the orderbook venue
    ORDERBOOK = "ORDERBOOK"


@dataclass
class ApiPositionsRequest:
    # The sub account ID to request for
    sub_account_id: str
    # The kind filter to apply. If nil, this defaults to all kinds. Otherwise, only entries matching the filter will be returned
    kind: list[Kind]
    # The underlying filter to apply. If nil, this defaults to all underlyings. Otherwise, only entries matching the filter will be returned
    underlying: list[Currency]
    # The quote filter to apply. If nil, this defaults to all quotes. Otherwise, only entries matching the filter will be returned
    quote: list[Currency]


@dataclass
class Positions:
    # Time at which the event was emitted in unix nanoseconds
    event_time: str
    # The sub account ID that participated in the trade
    sub_account_id: str
    # The instrument being represented
    instrument: str
    # The balance of the position, expressed in underlying asset decimal units. Negative for short positions
    balance: str
    # The value of the position, negative for short assets, expressed in quote asset decimal units
    value: str
    """
    The entry price of the position, expressed in `9` decimals
    Whenever increasing the balance of a position, the entry price is updated to the new average entry price
    newEntryPrice = (oldEntryPrice * oldBalance + tradePrice * tradeBalance) / (oldBalance + tradeBalance)
    """
    entry_price: str
    """
    The exit price of the position, expressed in `9` decimals
    Whenever decreasing the balance of a position, the exit price is updated to the new average exit price
    newExitPrice = (oldExitPrice * oldExitBalance + tradePrice * tradeBalance) / (oldExitBalance + tradeBalance)
    """
    exit_price: str
    # The mark price of the position, expressed in `9` decimals
    mark_price: str
    """
    The unrealized PnL of the position, expressed in quote asset decimal units
    unrealizedPnl = (markPrice - entryPrice) * balance
    """
    unrealized_pnl: str
    """
    The realized PnL of the position, expressed in quote asset decimal units
    realizedPnl = (exitPrice - entryPrice) * exitBalance
    """
    realized_pnl: str
    """
    The total PnL of the position, expressed in quote asset decimal units
    totalPnl = realizedPnl + unrealizedPnl
    """
    pnl: str
    """
    The ROI of the position, expressed as a percentage
    roi = (pnl / (entryPrice * balance)) * 100
    """
    roi: str


@dataclass
class ApiPositionsResponse:
    # The positions matching the request filter
    results: list[Positions]


@dataclass
class ApiPrivateTradeHistoryRequest:
    # The sub account ID to request for
    sub_account_id: str
    # The kind filter to apply. If nil, this defaults to all kinds. Otherwise, only entries matching the filter will be returned
    kind: list[Kind]
    # The underlying filter to apply. If nil, this defaults to all underlyings. Otherwise, only entries matching the filter will be returned
    underlying: list[Currency]
    # The quote filter to apply. If nil, this defaults to all quotes. Otherwise, only entries matching the filter will be returned
    quote: list[Currency]
    # The expiration time to apply in unix nanoseconds. If nil, this defaults to all expirations. Otherwise, only entries matching the filter will be returned
    expiration: str
    # The strike price to apply. If nil, this defaults to all strike prices. Otherwise, only entries matching the filter will be returned
    strike_price: str
    # The limit to query for. Defaults to 500; Max 1000
    limit: int
    # The cursor to indicate when to start the query from
    cursor: str


@dataclass
class PrivateTrade:
    # Time at which the event was emitted in unix nanoseconds
    event_time: str
    # The sub account ID that participated in the trade
    sub_account_id: str
    # The instrument being represented
    instrument: str
    # The side that the subaccount took on the trade
    is_buyer: bool
    # The role that the subaccount took on the trade
    is_taker: bool
    # The number of assets being traded, expressed in underlying asset decimal units
    size: str
    # The traded price, expressed in `9` decimals
    price: str
    # The mark price of the instrument at point of trade, expressed in `9` decimals
    mark_price: str
    # The index price of the instrument at point of trade, expressed in `9` decimals
    index_price: str
    # The interest rate of the underlying at point of trade, expressed in centibeeps (1/100th of a basis point)
    interest_rate: str
    # [Options] The forward price of the option at point of trade, expressed in `9` decimals
    forward_price: str
    # The realized PnL of the trade, expressed in quote asset decimal units (0 if increasing position size)
    realized_pnl: str
    # The fees paid on the trade, expressed in quote asset decimal unit (negative if maker rebate applied)
    fee: str
    # The fee rate paid on the trade
    fee_rate: str
    # A trade identifier
    trade_id: str
    # An order identifier
    order_id: str
    # The venue where the trade occurred
    venue: Venue
    """
    A unique identifier for the active order within a subaccount, specified by the client
    This is used to identify the order in the client's system
    This field can be used for order amendment/cancellation, but has no bearing on the smart contract layer
    This field will not be propagated to the smart contract, and should not be signed by the client
    This value must be unique for all active orders in a subaccount, or amendment/cancellation will not work as expected
    Gravity UI will generate a random clientOrderID for each order in the range [0, 2^63 - 1]
    To prevent any conflicts, client machines should generate a random clientOrderID in the range [2^63, 2^64 - 1]

    When GRVT Backend receives an order with an overlapping clientOrderID, we will reject the order with rejectReason set to overlappingClientOrderId
    """
    client_order_id: str


@dataclass
class ApiPrivateTradeHistoryResponse:
    # The total number of private trades matching the request filter
    total: int
    # The cursor to indicate when to start the query from
    next: str
    # The private trades matching the request asset
    results: list[PrivateTrade]


@dataclass
class ApiSubAccountSummaryRequest:
    # The subaccount ID to filter by
    sub_account_id: str


@dataclass
class SpotBalance:
    # The currency you hold a spot balance in
    currency: Currency
    """
    The balance of the asset, expressed in underlying asset decimal units
    Must take into account the value of all positions with this quote asset
    ie. for USDT denominated subaccounts, this is is identical to total balance
    """
    balance: str


@dataclass
class SubAccount:
    # Time at which the event was emitted in unix nanoseconds
    event_time: str
    # The sub account ID this entry refers to
    sub_account_id: str
    # The type of margin algorithm this subaccount uses
    margin_type: MarginType
    """
    The Quote Currency that this Sub Account is denominated in
    This subaccount can only open derivative positions denominated in this quote currency
    All other assets are converted to this quote currency for the purpose of calculating margin
    In the future, when users select a Multi-Currency Margin Type, this will be USD
    """
    quote_currency: Currency
    # The total unrealized PnL of all positions owned by this subaccount, denominated in quote currency decimal units
    unrealized_pnl: str
    # The total value across all spot assets, or in other words, the current margin
    total_value: str
    # The initial margin requirement of all positions owned by this vault, denominated in quote currency decimal units
    initial_margin: str
    # The maintanence margin requirement of all positions owned by this vault, denominated in quote currency decimal units
    maintanence_margin: str
    # The margin available for withdrawal, denominated in quote currency decimal units
    available_margin: str
    # The list of spot assets owned by this sub account, and their balances
    spot_balances: list[SpotBalance]
    # The list of positions owned by this sub account
    positions: list[Positions]


@dataclass
class ApiSubAccountSummaryResponse:
    # The sub account matching the request sub account
    results: SubAccount


@dataclass
class ApiSubAccountHistoryRequest:
    """
    The request to get the history of a sub account
    SubAccount Summary values are snapshotted once every hour
    No snapshots are taken if the sub account has no activity in the hourly window
    The history is returned in reverse chronological order
    History is preserved only for the last 30 days
    """

    # The sub account ID to request for
    sub_account_id: str
    # Start time of sub account history in unix nanoseconds
    start_time: str
    # End time of sub account history in unix nanoseconds
    end_time: str
    # The cursor to indicate when to start the next query from
    cursor: str


@dataclass
class ApiSubAccountHistoryResponse:
    # The total number of sub account snapshots matching the request filter
    total: int
    # The cursor to indicate when to start the next query from
    next: str
    # The sub account history matching the request sub account
    results: list[SubAccount]


@dataclass
class ApiLatestSnapSubAccountsRequest:
    """
    The request to get the latest snapshot of list sub account

    """

    # The list of sub account ids to query
    sub_account_i_ds: list[str]


@dataclass
class ApiLatestSnapSubAccountsResponse:
    # The sub account history matching the request sub account
    results: list[SubAccount]


@dataclass
class MarkPrice:
    # The currency you hold a spot balance in
    currency: Currency
    # The mark price of the asset, expressed in `9` decimals
    mark_price: str


@dataclass
class ApiAggregatedAccountSummaryResponse:
    # The main account ID of the account to which the summary belongs
    main_account_id: str
    # Total equity of the account, denominated in USD
    total_equity: str
    # The list of spot assets owned by this sub account, and their balances
    spot_balances: list[SpotBalance]
    # The list of mark prices for the assets owned by this account
    mark_prices: list[MarkPrice]


@dataclass
class ApiFundingAccountSummaryResponse:
    # The main account ID of the account to which the summary belongs
    main_account_id: str
    # Total equity of the account, denominated in USD
    total_equity: str
    # The list of spot assets owned by this account, and their balances
    spot_balances: list[SpotBalance]
    # The list of mark prices for the assets owned by this account
    mark_prices: list[MarkPrice]


@dataclass
class ApiOrderbookLevelsRequest:
    """
    The readable name of the instrument. For Perpetual: ETH_USDT_Perp [Underlying Quote Perp]
    For Future: BTC_USDT_Fut_20Oct23 [Underlying Quote Fut DateFormat]
    For Call: ETH_USDT_Call_20Oct23_4123 [Underlying Quote Call DateFormat StrikePrice]
    For Put: ETH_USDT_Put_20Oct23_4123 [Underlying Quote Put DateFormat StrikePrice]
    """

    instrument: str
    # Depth of the order book to be retrieved (API/Snapshot max is 100, Delta max is 1000)
    depth: int
    # The number of levels to aggregate into one level (1 = no aggregation, 10/100/1000 = aggregate 10/100/1000 levels into 1)
    aggregate: int


@dataclass
class OrderbookLevel:
    # The price of the level, expressed in `9` decimals
    price: str
    # The number of assets offered, expressed in underlying asset decimal units
    size: str
    # The number of open orders at this level
    num_orders: int


@dataclass
class OrderbookLevels:
    # Time at which the event was emitted in unix nanoseconds
    event_time: str
    """
    The readable name of the instrument. For Perpetual: ETH_USDT_Perp [Underlying Quote Perp]
    For Future: BTC_USDT_Fut_20Oct23 [Underlying Quote Fut DateFormat]
    For Call: ETH_USDT_Call_20Oct23_4123 [Underlying Quote Call DateFormat StrikePrice]
    For Put: ETH_USDT_Put_20Oct23_4123 [Underlying Quote Put DateFormat StrikePrice]
    """
    instrument: str
    # The list of best bids up till query depth
    bids: list[OrderbookLevel]
    # The list of best asks up till query depth
    asks: list[OrderbookLevel]


@dataclass
class ApiOrderbookLevelsResponse:
    # The orderbook levels objects matching the request asset
    results: OrderbookLevels


@dataclass
class ApiMiniTickerRequest:
    """
    The readable name of the instrument. For Perpetual: ETH_USDT_Perp [Underlying Quote Perp]
    For Future: BTC_USDT_Fut_20Oct23 [Underlying Quote Fut DateFormat]
    For Call: ETH_USDT_Call_20Oct23_4123 [Underlying Quote Call DateFormat StrikePrice]
    For Put: ETH_USDT_Put_20Oct23_4123 [Underlying Quote Put DateFormat StrikePrice]
    """

    instrument: str


@dataclass
class MiniTicker:
    # Time at which the event was emitted in unix nanoseconds
    event_time: str | None
    """
    The readable name of the instrument. For Perpetual: ETH_USDT_Perp [Underlying Quote Perp]
    For Future: BTC_USDT_Fut_20Oct23 [Underlying Quote Fut DateFormat]
    For Call: ETH_USDT_Call_20Oct23_4123 [Underlying Quote Call DateFormat StrikePrice]
    For Put: ETH_USDT_Put_20Oct23_4123 [Underlying Quote Put DateFormat StrikePrice]
    """
    instrument: str | None
    # The mark price of the instrument, expressed in `9` decimals
    mark_price: str | None
    # The index price of the instrument, expressed in `9` decimals
    index_price: str | None
    # The last traded price of the instrument (also close price), expressed in `9` decimals
    last_price: str | None
    # The number of assets traded in the last trade, expressed in underlying asset decimal units
    last_size: str | None
    # The mid price of the instrument, expressed in `9` decimals
    mid_price: str | None
    # The best bid price of the instrument, expressed in `9` decimals
    best_bid_price: str | None
    # The number of assets offered on the best bid price of the instrument, expressed in underlying asset decimal units
    best_bid_size: str | None
    # The best ask price of the instrument, expressed in `9` decimals
    best_ask_price: str | None
    # The number of assets offered on the best ask price of the instrument, expressed in underlying asset decimal units
    best_ask_size: str | None


@dataclass
class ApiMiniTickerResponse:
    # The mini ticker matching the request asset
    results: MiniTicker


@dataclass
class ApiTickerRequest:
    """
    The readable name of the instrument. For Perpetual: ETH_USDT_Perp [Underlying Quote Perp]
    For Future: BTC_USDT_Fut_20Oct23 [Underlying Quote Fut DateFormat]
    For Call: ETH_USDT_Call_20Oct23_4123 [Underlying Quote Call DateFormat StrikePrice]
    For Put: ETH_USDT_Put_20Oct23_4123 [Underlying Quote Put DateFormat StrikePrice]
    """

    instrument: str


@dataclass
class Ticker:
    """
    Derived data such as the below, will not be included by default:
      - 24 hour volume (`buyVolume + sellVolume`)
      - 24 hour taker buy/sell ratio (`buyVolume / sellVolume`)
      - 24 hour average trade price (`volumeQ / volumeU`)
      - 24 hour average trade volume (`volume / trades`)
      - 24 hour percentage change (`24hStatChange / 24hStat`)
      - 48 hour statistics (`2 * 24hStat - 24hStatChange`)

    To query for an extended ticker payload, leverage the `greeks` and the `derived` flags.
    Ticker extensions are currently under design to offer you more convenience.
    These flags are only supported on the `Ticker Snapshot` WS endpoint, and on the `Ticker` API endpoint.

    """

    # Time at which the event was emitted in unix nanoseconds
    event_time: str | None
    """
    The readable name of the instrument. For Perpetual: ETH_USDT_Perp [Underlying Quote Perp]
    For Future: BTC_USDT_Fut_20Oct23 [Underlying Quote Fut DateFormat]
    For Call: ETH_USDT_Call_20Oct23_4123 [Underlying Quote Call DateFormat StrikePrice]
    For Put: ETH_USDT_Put_20Oct23_4123 [Underlying Quote Put DateFormat StrikePrice]
    """
    instrument: str | None
    # The mark price of the instrument, expressed in `9` decimals
    mark_price: str | None
    # The index price of the instrument, expressed in `9` decimals
    index_price: str | None
    # The last traded price of the instrument (also close price), expressed in `9` decimals
    last_price: str | None
    # The number of assets traded in the last trade, expressed in underlying asset decimal units
    last_size: str | None
    # The mid price of the instrument, expressed in `9` decimals
    mid_price: str | None
    # The best bid price of the instrument, expressed in `9` decimals
    best_bid_price: str | None
    # The number of assets offered on the best bid price of the instrument, expressed in underlying asset decimal units
    best_bid_size: str | None
    # The best ask price of the instrument, expressed in `9` decimals
    best_ask_price: str | None
    # The number of assets offered on the best ask price of the instrument, expressed in underlying asset decimal units
    best_ask_size: str | None
    # The current funding rate of the instrument, expressed in centibeeps (1/100th of a basis point)
    funding_rate_8_h_curr: str | None
    # The average funding rate of the instrument (over last 8h), expressed in centibeeps (1/100th of a basis point)
    funding_rate_8_h_avg: str | None
    # The interest rate of the underlying, expressed in centibeeps (1/100th of a basis point)
    interest_rate: str | None
    # [Options] The forward price of the option, expressed in `9` decimals
    forward_price: str | None
    # The 24 hour taker buy volume of the instrument, expressed in underlying asset decimal units
    buy_volume_24_h_u: str | None
    # The 24 hour taker sell volume of the instrument, expressed in underlying asset decimal units
    sell_volume_24_h_u: str | None
    # The 24 hour taker buy volume of the instrument, expressed in quote asset decimal units
    buy_volume_24_h_q: str | None
    # The 24 hour taker sell volume of the instrument, expressed in quote asset decimal units
    sell_volume_24_h_q: str | None
    # The 24 hour highest traded price of the instrument, expressed in `9` decimals
    high_price: str | None
    # The 24 hour lowest traded price of the instrument, expressed in `9` decimals
    low_price: str | None
    # The 24 hour first traded price of the instrument, expressed in `9` decimals
    open_price: str | None
    # The open interest in the instrument, expressed in underlying asset decimal units
    open_interest: str | None
    # The ratio of accounts that are net long vs net short on this instrument
    long_short_ratio: str | None


@dataclass
class ApiTickerResponse:
    # The mini ticker matching the request asset
    results: Ticker


@dataclass
class ApiPublicTradesRequest:
    """
    Retrieves up to 1000 of the most recent public trades in any given instrument. Do not use this to poll for data -- a websocket subscription is much more performant, and useful.
    This endpoint offers public trading data, use the Trading APIs instead to query for your personalized trade tape.
    """

    """
    The readable name of the instrument. For Perpetual: ETH_USDT_Perp [Underlying Quote Perp]
    For Future: BTC_USDT_Fut_20Oct23 [Underlying Quote Fut DateFormat]
    For Call: ETH_USDT_Call_20Oct23_4123 [Underlying Quote Call DateFormat StrikePrice]
    For Put: ETH_USDT_Put_20Oct23_4123 [Underlying Quote Put DateFormat StrikePrice]
    """
    instrument: str
    # The limit to query for. Defaults to 500; Max 1000
    limit: int


@dataclass
class PublicTrade:
    # Time at which the event was emitted in unix nanoseconds
    event_time: str
    """
    The readable name of the instrument. For Perpetual: ETH_USDT_Perp [Underlying Quote Perp]
    For Future: BTC_USDT_Fut_20Oct23 [Underlying Quote Fut DateFormat]
    For Call: ETH_USDT_Call_20Oct23_4123 [Underlying Quote Call DateFormat StrikePrice]
    For Put: ETH_USDT_Put_20Oct23_4123 [Underlying Quote Put DateFormat StrikePrice]
    """
    instrument: str
    # If taker was the buyer on the trade
    is_taker_buyer: bool
    # The number of assets being traded, expressed in underlying asset decimal units
    size: str
    # The traded price, expressed in `9` decimals
    price: str
    # The mark price of the instrument at point of trade, expressed in `9` decimals
    mark_price: str
    # The index price of the instrument at point of trade, expressed in `9` decimals
    index_price: str
    # The interest rate of the underlying at point of trade, expressed in centibeeps (1/100th of a basis point)
    interest_rate: str
    # [Options] The forward price of the option at point of trade, expressed in `9` decimals
    forward_price: str
    # A trade identifier
    trade_id: str
    # The venue where the trade occurred
    venue: Venue
    # If the trade was a liquidation
    is_liquidation: bool


@dataclass
class ApiPublicTradesResponse:
    # The public trades matching the request asset
    results: list[PublicTrade]


@dataclass
class ApiPublicTradeHistoryRequest:
    """
    Perform historical lookup of public trades in any given instrument.
    This endpoint offers public trading data, use the Trading APIs instead to query for your personalized trade tape.
    Only data from the last three months will be retained.
    """

    """
    The readable name of the instrument. For Perpetual: ETH_USDT_Perp [Underlying Quote Perp]
    For Future: BTC_USDT_Fut_20Oct23 [Underlying Quote Fut DateFormat]
    For Call: ETH_USDT_Call_20Oct23_4123 [Underlying Quote Call DateFormat StrikePrice]
    For Put: ETH_USDT_Put_20Oct23_4123 [Underlying Quote Put DateFormat StrikePrice]
    """
    instrument: str
    # The limit to query for. Defaults to 500; Max 1000
    limit: int
    # The cursor to indicate when to start the query from
    cursor: str


@dataclass
class ApiPublicTradeHistoryResponse:
    # The public trades matching the request asset
    results: list[PublicTrade]


@dataclass
class ApiGetInstrumentRequest:
    """
    The readable name of the instrument. For Perpetual: ETH_USDT_Perp [Underlying Quote Perp]
    For Future: BTC_USDT_Fut_20Oct23 [Underlying Quote Fut DateFormat]
    For Call: ETH_USDT_Call_20Oct23_4123 [Underlying Quote Call DateFormat StrikePrice]
    For Put: ETH_USDT_Put_20Oct23_4123 [Underlying Quote Put DateFormat StrikePrice]
    """

    instrument: str


@dataclass
class Instrument:
    """
    The readable name of the instrument. For Perpetual: ETH_USDT_Perp [Underlying Quote Perp]
    For Future: BTC_USDT_Fut_20Oct23 [Underlying Quote Fut DateFormat]
    For Call: ETH_USDT_Call_20Oct23_4123 [Underlying Quote Call DateFormat StrikePrice]
    For Put: ETH_USDT_Put_20Oct23_4123 [Underlying Quote Put DateFormat StrikePrice]
    """

    instrument: str
    # The underlying currency
    underlying: Currency
    # The quote currency
    quote: Currency
    # The kind of instrument
    kind: Kind
    # The expiry time of the instrument in unix nanoseconds
    expiry: str
    # The strike price of the instrument, expressed in `9` decimals
    strike_price: str
    # Venues that this instrument can be traded at
    venues: list[Venue]
    # The settlement period of the instrument
    settlement_period: InstrumentSettlementPeriod
    # The smallest denomination of the underlying asset supported by GRVT (+3 represents 0.001, -3 represents 1000, 0 represents 1)
    underlying_decimals: int
    # The smallest denomination of the quote asset supported by GRVT (+3 represents 0.001, -3 represents 1000, 0 represents 1)
    quote_decimals: int
    # The size of a single tick, expressed in quote asset decimal units
    tick_size: str
    # The minimum contract size, expressed in underlying asset decimal units
    min_size: str
    # The minimum block trade size, expressed in underlying asset decimal units
    min_block_trade_size: str
    # Creation time in unix nanoseconds
    create_time: str


@dataclass
class ApiGetInstrumentResponse:
    # The instrument matching the request asset
    results: Instrument


@dataclass
class ApiGetFilteredInstrumentsRequest:
    # The kind filter to apply. If nil, this defaults to all kinds. Otherwise, only entries matching the filter will be returned
    kind: list[Kind]
    # The underlying filter to apply. If nil, this defaults to all underlyings. Otherwise, only entries matching the filter will be returned
    underlying: list[Currency]
    # The quote filter to apply. If nil, this defaults to all quotes. Otherwise, only entries matching the filter will be returned
    quote: list[Currency]
    # Request for active instruments only
    is_active: bool
    # The limit to query for. Defaults to 500; Max 100000
    limit: int


@dataclass
class ApiGetFilteredInstrumentsResponse:
    # The instruments matching the request filter
    results: list[Instrument]


@dataclass
class ApiCandlestickRequest:
    """
    Kline/Candlestick bars for an instrument. Klines are uniquely identified by their instrument, type, interval, and open time.
    startTime and endTime are optional parameters. The semantics of these parameters are as follows:<ul><li>If both `startTime` and `endTime` are not set, the most recent candlesticks are returned up to `limit`.</li><li>If `startTime` is set and `endTime` is not set, the candlesticks starting from `startTime` are returned up to `limit`.</li><li>If `startTime` is not set and `endTime` is set, the candlesticks ending at `endTime` are returned up to `limit`.</li><li>If both `startTime` and `endTime` are set, the candlesticks between `startTime` and `endTime` are returned up to `limit`.</li></ul>
    """

    """
    The readable name of the instrument. For Perpetual: ETH_USDT_Perp [Underlying Quote Perp]
    For Future: BTC_USDT_Fut_20Oct23 [Underlying Quote Fut DateFormat]
    For Call: ETH_USDT_Call_20Oct23_4123 [Underlying Quote Call DateFormat StrikePrice]
    For Put: ETH_USDT_Put_20Oct23_4123 [Underlying Quote Put DateFormat StrikePrice]
    """
    instrument: str
    # The interval of each candlestick
    interval: CandlestickInterval
    # The type of candlestick data to retrieve
    type: CandlestickType
    # Start time of kline data in unix nanoseconds
    start_time: str
    # End time of kline data in unix nanoseconds
    end_time: str
    # The limit to query for. Defaults to 500; Max 1500
    limit: int


@dataclass
class Candlestick:
    # Open time of kline bar in unix nanoseconds
    open_time: str
    # Close time of kline bar in unix nanosecond
    close_time: str
    # The open price, expressed in underlying currency resolution units
    open: str
    # The close price, expressed in underlying currency resolution units
    close: str
    # The high price, expressed in underlying currency resolution units
    high: str
    # The low price, expressed in underlying currency resolution units
    low: str
    # The underlying volume transacted, expressed in underlying asset decimal units
    volume_u: str
    # The quote volume transacted, expressed in quote asset decimal units
    volume_q: str
    # The number of trades transacted
    trades: int
    """
    The readable name of the instrument. For Perpetual: ETH_USDT_Perp [Underlying Quote Perp]
    For Future: BTC_USDT_Fut_20Oct23 [Underlying Quote Fut DateFormat]
    For Call: ETH_USDT_Call_20Oct23_4123 [Underlying Quote Call DateFormat StrikePrice]
    For Put: ETH_USDT_Put_20Oct23_4123 [Underlying Quote Put DateFormat StrikePrice]
    """
    instrument: str


@dataclass
class ApiCandlestickResponse:
    # The candlestick result set for given interval
    results: list[Candlestick]


@dataclass
class ApiFundingRateRequest:
    """
    Lookup the historical funding rate of various pairs.
    startTime and endTime are optional parameters. The semantics of these parameters are as follows:<ul><li>If both `startTime` and `endTime` are not set, the most recent funding rates are returned up to `limit`.</li><li>If `startTime` is set and `endTime` is not set, the funding rates starting from `startTime` are returned up to `limit`.</li><li>If `startTime` is not set and `endTime` is set, the funding rates ending at `endTime` are returned up to `limit`.</li><li>If both `startTime` and `endTime` are set, the funding rates between `startTime` and `endTime` are returned up to `limit`.</li></ul>

    The instrument is also optional. When left empty, all perpetual instruments are returned.
    """

    """
    The readable name of the instrument. For Perpetual: ETH_USDT_Perp [Underlying Quote Perp]
    For Future: BTC_USDT_Fut_20Oct23 [Underlying Quote Fut DateFormat]
    For Call: ETH_USDT_Call_20Oct23_4123 [Underlying Quote Call DateFormat StrikePrice]
    For Put: ETH_USDT_Put_20Oct23_4123 [Underlying Quote Put DateFormat StrikePrice]
    """
    instrument: str
    # Start time of funding rate in unix nanoseconds
    start_time: str
    # End time of funding rate in unix nanoseconds
    end_time: str
    # The limit to query for. Defaults to 90; Max 300
    limit: int


@dataclass
class FundingRate:
    """
    The readable name of the instrument. For Perpetual: ETH_USDT_Perp [Underlying Quote Perp]
    For Future: BTC_USDT_Fut_20Oct23 [Underlying Quote Fut DateFormat]
    For Call: ETH_USDT_Call_20Oct23_4123 [Underlying Quote Call DateFormat StrikePrice]
    For Put: ETH_USDT_Put_20Oct23_4123 [Underlying Quote Put DateFormat StrikePrice]
    """

    instrument: str
    # The funding rate of the instrument, expressed in centibeeps
    funding_rate: int
    # The funding timestamp of the funding rate, expressed in unix nanoseconds
    funding_time: str
    # The mark price of the instrument at funding timestamp, expressed in `9` decimals
    mark_price: str


@dataclass
class ApiFundingRateResponse:
    # The funding rate result set for given interval
    results: list[FundingRate]


@dataclass
class ApiSettlementPriceRequest:
    """
    Lookup the historical settlement price of various pairs.
    startTime and endTime are optional parameters. The semantics of these parameters are as follows:<ul><li>If both `startTime` and `endTime` are not set, the most recent settlement prices are returned up to `limit`.</li><li>If `startTime` is set and `endTime` is not set, the settlement prices starting from `startTime` are returned up to `limit`.</li><li>If `startTime` is not set and `endTime` is set, the settlement prices ending at `endTime` are returned up to `limit`.</li><li>If both `startTime` and `endTime` are set, the settlement prices between `startTime` and `endTime` are returned up to `limit`.</li></ul>

    The instrument is also optional. When left empty, all perpetual instruments are returned.
    """

    # The underlying currency to select
    underlying: Currency
    # The quote currency to select
    quote: Currency
    # Start time of kline data in unix nanoseconds
    start_time: str
    # End time of kline data in unix nanoseconds
    end_time: str
    # The expiration time to select in unix nanoseconds
    expiration: str
    # The strike price to select
    strike_price: str
    # The limit to query for. Defaults to 30; Max 100
    limit: int


@dataclass
class APISettlementPrice:
    # The underlying currency of the settlement price
    underlying: Currency
    # The quote currency of the settlement price
    quote: Currency
    # The settlement timestamp of the settlement price, expressed in unix nanoseconds
    settlement_time: str
    # The settlement price, expressed in `9` decimals
    settlement_price: str


@dataclass
class ApiSettlementPriceResponse:
    # The funding rate result set for given interval
    results: list[APISettlementPrice]


@dataclass
class WSRequestV1:
    # The channel to subscribe to (eg: ticker.s / ticker.d
    stream: str
    # The list of feeds to subscribe to (eg:
    feed: list[str]
    # The method to use for the request (eg: subscribe / unsubscribe)
    method: str
    # Whether the request is for full data or lite data
    is_full: bool


@dataclass
class WSOrderbookLevelsFeedSelectorV1:
    """
    Subscribes to aggregated orderbook updates for a single instrument. The `book.s` channel offers simpler integration. To experience higher publishing rates, please use the `book.d` channel.
    Unlike the `book.d` channel which publishes an initial snapshot, then only streams deltas after, the `book.s` channel publishes full snapshots at each feed.

    The Delta feed will work as follows:<ul><li>On subscription, the server will send a full snapshot of all levels of the Orderbook.</li><li>After the snapshot, the server will only send levels that have changed in value.</li></ul>

    Field Semantics:<ul><li>[DeltaOnly] If a level is not updated, level not published</li><li>If a level is updated, {size: '123'}</li><li>If a level is set to zero, {size: '0'}</li><li>Incoming levels will be published as soon as price moves</li><li>Outgoing levels will be published with `size = 0`</li></ul>
    """

    """
    The readable name of the instrument. For Perpetual: ETH_USDT_Perp [Underlying Quote Perp]
    For Future: BTC_USDT_Fut_20Oct23 [Underlying Quote Fut DateFormat]
    For Call: ETH_USDT_Call_20Oct23_4123 [Underlying Quote Call DateFormat StrikePrice]
    For Put: ETH_USDT_Put_20Oct23_4123 [Underlying Quote Put DateFormat StrikePrice]
    """
    instrument: str
    """
    The minimal rate at which we publish feeds (in milliseconds)
    Delta (100, 200, 500, 1000, 5000)
    Snapshot (500, 1000, 5000)
    """
    rate: int
    # Depth of the order book to be retrieved (API/Snapshot max is 100, Delta max is 1000)
    depth: int
    # The number of levels to aggregate into one level (1 = no aggregation, 10/100/1000 = aggregate 10/100/1000 levels into 1)
    aggregate: int


@dataclass
class WSOrderbookLevelsFeedDataV1:
    # Stream name
    stream: str
    # A running sequence number that determines global message order within the specific stream
    sequence_number: str
    # An orderbook levels object matching the request filter
    feed: OrderbookLevels


@dataclass
class WSMiniTickerFeedSelectorV1:
    """
    Subscribes to a mini ticker feed for a single instrument. The `mini.s` channel offers simpler integration. To experience higher publishing rates, please use the `mini.d` channel.
    Unlike the `mini.d` channel which publishes an initial snapshot, then only streams deltas after, the `mini.s` channel publishes full snapshots at each feed.

    The Delta feed will work as follows:<ul><li>On subscription, the server will send a full snapshot of the mini ticker.</li><li>After the snapshot, the server will only send deltas of the mini ticker.</li><li>The server will send a delta if any of the fields in the mini ticker have changed.</li></ul>

    Field Semantics:<ul><li>[DeltaOnly] If a field is not updated, {}</li><li>If a field is updated, {field: '123'}</li><li>If a field is set to zero, {field: '0'}</li><li>If a field is set to null, {field: ''}</li></ul>
    """

    """
    The readable name of the instrument. For Perpetual: ETH_USDT_Perp [Underlying Quote Perp]
    For Future: BTC_USDT_Fut_20Oct23 [Underlying Quote Fut DateFormat]
    For Call: ETH_USDT_Call_20Oct23_4123 [Underlying Quote Call DateFormat StrikePrice]
    For Put: ETH_USDT_Put_20Oct23_4123 [Underlying Quote Put DateFormat StrikePrice]
    """
    instrument: str
    """
    The minimal rate at which we publish feeds (in milliseconds)
    Delta (raw, 50, 100, 200, 500, 1000, 5000)
    Snapshot (200, 500, 1000, 5000)
    """
    rate: int


@dataclass
class WSMiniTickerFeedDataV1:
    # Stream name
    stream: str
    # A running sequence number that determines global message order within the specific stream
    sequence_number: str
    # A mini ticker matching the request filter
    feed: MiniTicker


@dataclass
class WSTickerFeedSelectorV1:
    """
    Subscribes to a ticker feed for a single instrument. The `ticker.s` channel offers simpler integration. To experience higher publishing rates, please use the `ticker.d` channel.
    Unlike the `ticker.d` channel which publishes an initial snapshot, then only streams deltas after, the `ticker.s` channel publishes full snapshots at each feed.

    The Delta feed will work as follows:<ul><li>On subscription, the server will send a full snapshot of the ticker.</li><li>After the snapshot, the server will only send deltas of the ticker.</li><li>The server will send a delta if any of the fields in the ticker have changed.</li></ul>

    Field Semantics:<ul><li>[DeltaOnly] If a field is not updated, {}</li><li>If a field is updated, {field: '123'}</li><li>If a field is set to zero, {field: '0'}</li><li>If a field is set to null, {field: ''}</li></ul>
    """

    """
    The readable name of the instrument. For Perpetual: ETH_USDT_Perp [Underlying Quote Perp]
    For Future: BTC_USDT_Fut_20Oct23 [Underlying Quote Fut DateFormat]
    For Call: ETH_USDT_Call_20Oct23_4123 [Underlying Quote Call DateFormat StrikePrice]
    For Put: ETH_USDT_Put_20Oct23_4123 [Underlying Quote Put DateFormat StrikePrice]
    """
    instrument: str
    """
    The minimal rate at which we publish feeds (in milliseconds)
    Delta (100, 200, 500, 1000, 5000)
    Snapshot (500, 1000, 5000)
    """
    rate: int


@dataclass
class WSTickerFeedDataV1:
    # Stream name
    stream: str
    # A running sequence number that determines global message order within the specific stream
    sequence_number: str
    # A ticker matching the request filter
    feed: Ticker


@dataclass
class ApiTickerFeedDataV1:
    # The mini ticker matching the request asset
    results: Ticker


@dataclass
class WSPublicTradesFeedSelectorV1:
    """
    The readable name of the instrument. For Perpetual: ETH_USDT_Perp [Underlying Quote Perp]
    For Future: BTC_USDT_Fut_20Oct23 [Underlying Quote Fut DateFormat]
    For Call: ETH_USDT_Call_20Oct23_4123 [Underlying Quote Call DateFormat StrikePrice]
    For Put: ETH_USDT_Put_20Oct23_4123 [Underlying Quote Put DateFormat StrikePrice]
    """

    instrument: str
    # The limit to query for. Defaults to 500; Max 1000
    limit: int


@dataclass
class WSPublicTradesFeedDataV1:
    # Stream name
    stream: str
    # A running sequence number that determines global message order within the specific stream
    sequence_number: str
    # A public trade matching the request filter
    feed: PublicTrade


@dataclass
class WSCandlestickFeedSelectorV1:
    """
    Subscribes to a stream of Kline/Candlestick updates for an instrument. A Kline is uniquely identified by its open time.
    A new Kline is published every interval (if it exists). Upon subscription, the server will send the 5 most recent Kline for the requested interval.
    """

    """
    The readable name of the instrument. For Perpetual: ETH_USDT_Perp [Underlying Quote Perp]
    For Future: BTC_USDT_Fut_20Oct23 [Underlying Quote Fut DateFormat]
    For Call: ETH_USDT_Call_20Oct23_4123 [Underlying Quote Call DateFormat StrikePrice]
    For Put: ETH_USDT_Put_20Oct23_4123 [Underlying Quote Put DateFormat StrikePrice]
    """
    instrument: str
    # The interval of each candlestick
    interval: CandlestickInterval
    # The type of candlestick data to retrieve
    type: CandlestickType


@dataclass
class WSCandlestickFeedDataV1:
    # Stream name
    stream: str
    # A running sequence number that determines global message order within the specific stream
    sequence_number: str
    # A candlestick entry matching the request filters
    feed: Candlestick


@dataclass
class WSResponseV1:
    # The channel to subscribe to (eg: ticker.s / ticker.d
    stream: str
    # The list of feeds subscribed to
    subs: list[str]
    # The list of feeds unsubscribed to
    unsubs: list[str]


@dataclass
class ApiGetAllInstrumentsRequest:
    # Fetch only active instruments
    is_active: bool | None


@dataclass
class ApiGetAllInstrumentsResponse:
    # List of instruments
    results: list[Instrument]


@dataclass
class OrderLeg:
    # The instrument to trade in this leg
    instrument: str
    # The total number of assets to trade in this leg, expressed in underlying asset decimal units.
    size: str
    """
    The limit price of the order leg, expressed in `9` decimals.
    This is the total amount of base currency to pay/receive for all legs.
    """
    limit_price: str
    """
    If a OCO order is specified, this must contain the other limit price
    User must sign both limit prices. Depending on which trigger condition is activated, a different limit price is used
    The smart contract will always validate both limit prices, by arranging them in ascending order
    """
    oco_limit_price: str
    # Specifies if the order leg is a buy or sell
    is_buying_asset: bool


@dataclass
class Signature:
    # The address (public key) of the wallet signing the payload
    signer: str
    # Signature R
    r: str
    # Signature S
    s: str
    # Signature V
    v: int
    # Timestamp after which this signature expires, expressed in unix nanoseconds. Must be capped at 30 days
    expiration: str
    """
    Users can randomly generate this value, used as a signature deconflicting key.
    ie. You can send the same exact instruction twice with different nonces.
    When the same nonce is used, the same payload will generate the same signature.
    Our system will consider the payload a duplicate, and ignore it.
    """
    nonce: int


@dataclass
class OrderMetadata:
    """
    Metadata fields are used to support Backend only operations. These operations are not trustless by nature.
    Hence, fields in here are never signed, and is never transmitted to the smart contract.
    """

    """
    A unique identifier for the active order within a subaccount, specified by the client
    This is used to identify the order in the client's system
    This field can be used for order amendment/cancellation, but has no bearing on the smart contract layer
    This field will not be propagated to the smart contract, and should not be signed by the client
    This value must be unique for all active orders in a subaccount, or amendment/cancellation will not work as expected
    Gravity UI will generate a random clientOrderID for each order in the range [0, 2^63 - 1]
    To prevent any conflicts, client machines should generate a random clientOrderID in the range [2^63, 2^64 - 1]

    When GRVT Backend receives an order with an overlapping clientOrderID, we will reject the order with rejectReason set to overlappingClientOrderId
    """
    client_order_id: str
    # [Filled by GRVT Backend] Time at which the order was received by GRVT in unix nanoseconds
    create_time: str


@dataclass
class OrderState:
    # The status of the order
    status: OrderStatus
    # The reason for rejection or cancellation
    reject_reason: OrderRejectReason
    # The number of assets available for orderbook/RFQ matching. Sorted in same order as Order.Legs
    book_size: list[str]
    # The total number of assets traded. Sorted in same order as Order.Legs
    traded_size: list[str]
    # Time at which the order was updated by GRVT, expressed in unix nanoseconds
    update_time: str


@dataclass
class Order:
    """
    Order is a typed payload used throughout the GRVT platform to express all orderbook, RFQ, and liquidation orders.
    GRVT orders are capable of expressing both single-legged, and multi-legged orders by default.
    This increases the learning curve slightly but reduces overall integration load, since the order payload is used across all GRVT trading venues.
    Given GRVT's trustless settlement model, the Order payload also carries the signature, required to trade the order on our ZKSync Hyperchain.

    All fields in the Order payload (except `id`, `metadata`, and `state`) are trustlessly enforced on our Hyperchain.
    This minimizes the amount of trust users have to offer to GRVT
    """

    # [Filled by GRVT Backend] A unique 128-bit identifier for the order, deterministically generated within the GRVT backend
    order_id: str
    # The subaccount initiating the order
    sub_account_id: str
    """
    If the order is a market order
    Market Orders do not have a limit price, and are always executed according to the maker order price.
    Market Orders must always be taker orders
    """
    is_market: bool
    """
    Four supported types of orders: GTT, IOC, AON, FOK:<ul>
    <li>PARTIAL EXECUTION = GTT / IOC - allows partial size execution on each leg</li>
    <li>FULL EXECUTION = AON / FOK - only allows full size execution on all legs</li>
    <li>TAKER ONLY = IOC / FOK - only allows taker orders</li>
    <li>MAKER OR TAKER = GTT / AON - allows maker or taker orders</li>
    </ul>Exchange only supports (GTT, IOC, FOK)
    RFQ Maker only supports (GTT, AON), RFQ Taker only supports (FOK)
    """
    time_in_force: TimeInForce
    """
    The taker fee percentage cap signed by the order.
    This is the maximum taker fee percentage the order sender is willing to pay for the order.
    Expressed in 1/100th of a basis point. Eg. 100 = 1bps, 10,000 = 1%

    """
    taker_fee_percentage_cap: int
    # Same as TakerFeePercentageCap, but for the maker fee. Negative for maker rebates
    maker_fee_percentage_cap: int
    """
    If True, Order must be a maker order. It has to fill the orderbook instead of match it.
    If False, Order can be either a maker or taker order.

    |               | Must Fill All | Can Fill Partial |
    | -             | -             | -                |
    | Must Be Taker | FOK + False   | IOC + False      |
    | Can Be Either | AON + False   | GTC + False      |
    | Must Be Maker | AON + True    | GTC + True       |

    """
    post_only: bool
    # If True, Order must reduce the position size, or be cancelled
    reduce_only: bool
    """
    The legs present in this order
    The legs must be sorted by Asset.Instrument/Underlying/Quote/Expiration/StrikePrice
    """
    legs: list[OrderLeg]
    # The signature approving this order
    signature: Signature
    # Order Metadata, ignored by the smart contract, and unsigned by the client
    metadata: OrderMetadata
    # [Filled by GRVT Backend] The current state of the order, ignored by the smart contract, and unsigned by the client
    state: OrderState


@dataclass
class ApiCreateOrderRequest:
    # The order to create
    order: Order


@dataclass
class ApiCreateOrderResponse:
    # The created order
    order: Order


@dataclass
class ApiCancelOrderRequest:
    # The subaccount ID cancelling the order
    sub_account_id: str
    # Cancel the order with this `order_id`
    order_id: str
    # Cancel the order with this `client_order_id`
    client_order_id: str


@dataclass
class ApiCancelOrderResponse:
    # The cancelled order
    order: Order


@dataclass
class ApiCancelAllOrdersRequest:
    # The subaccount ID cancelling all orders
    sub_account_id: str


@dataclass
class ApiCancelAllOrdersResponse:
    # The number of orders cancelled
    num_cancelled: int


@dataclass
class ApiOpenOrdersRequest:
    # The subaccount ID to filter by
    sub_account_id: str
    # The kind filter to apply. If nil, this defaults to all kinds. Otherwise, only entries matching the filter will be returned
    kind: list[Kind]
    # The underlying filter to apply. If nil, this defaults to all underlyings. Otherwise, only entries matching the filter will be returned
    underlying: list[Currency]
    # The quote filter to apply. If nil, this defaults to all quotes. Otherwise, only entries matching the filter will be returned
    quote: list[Currency]


@dataclass
class ApiOpenOrdersResponse:
    # The Open Orders matching the request filter
    orders: list[Order]


@dataclass
class ApiOrderHistoryRequest:
    # The subaccount ID to filter by
    sub_account_id: str
    # The kind filter to apply. If nil, this defaults to all kinds. Otherwise, only entries matching the filter will be returned
    kind: list[Kind]
    # The underlying filter to apply. If nil, this defaults to all underlyings. Otherwise, only entries matching the filter will be returned
    underlying: list[Currency]
    # The quote filter to apply. If nil, this defaults to all quotes. Otherwise, only entries matching the filter will be returned
    quote: list[Currency]
    # The expiration time to apply in nanoseconds. If nil, this defaults to all expirations. Otherwise, only entries matching the filter will be returned
    expiration: list[str]
    # The strike price to apply. If nil, this defaults to all strike prices. Otherwise, only entries matching the filter will be returned
    strike_price: list[str]
    # The limit to query for. Defaults to 500; Max 1000
    limit: int
    # The cursor to indicate when to start the query from
    cursor: str


@dataclass
class ApiOrderHistoryResponse:
    # The total number of orders matching the request filter
    total: int
    # The cursor to indicate when to start the query from
    next: str
    # The Open Orders matching the request filter
    orders: list[Order]


@dataclass
class EmptyRequest:
    pass


@dataclass
class AckResponse:
    # Gravity has acknowledged that the request has been successfully received and it will process it in the backend
    acknowledgement: bool


@dataclass
class ApiOrderStateRequest:
    # The subaccount ID to filter by
    sub_account_id: str
    # Filter for `order_id`
    order_id: str
    # Filter for `client_order_id`
    client_order_id: str


@dataclass
class ApiOrderStateResponse:
    # The order state for the requested filter
    state: OrderState


@dataclass
class ApiGetOrderRequest:
    # The subaccount ID to filter by
    sub_account_id: str
    # Filter for `order_id`
    order_id: str
    # Filter for `client_order_id`
    client_order_id: str


@dataclass
class ApiGetOrderResponse:
    # The order object for the requested filter
    order: Order


@dataclass
class ApiGetUserEcosystemPointRequest:
    # The off chain account id
    account_id: str
    # Start time of the epoch - phase
    calculate_from: str
    # Include user rank in the response
    include_user_rank: bool


@dataclass
class EcosystemPoint:
    # The off chain account id
    account_id: str
    # The main account id
    main_account_id: str
    # Total ecosystem point
    total_point: str
    # Direct invite count
    direct_invite_count: int
    # Indirect invite count
    indirect_invite_count: int
    # Direct invite trading volume
    direct_invite_trading_volume: str
    # Indirect invite trading volume
    indirect_invite_trading_volume: str
    # The time when the ecosystem point is calculated
    calculate_at: str
    # Start time of the epoch - phase
    calculate_from: str
    # End time of the epoch - phase
    calculate_to: str
    # The rank of the account in the ecosystem
    rank: int


@dataclass
class ApiGetUserEcosystemPointResponse:
    # The list of ecosystem points
    points: list[EcosystemPoint]


@dataclass
class ApiGetEcosystemLeaderboardRequest:
    # Start time of the epoch - phase
    calculate_from: str
    # The number of accounts to return
    limit: int


@dataclass
class ApiGetEcosystemLeaderboardResponse:
    # The list of ecosystem points
    points: list[EcosystemPoint]


@dataclass
class ApiGetEcosystemReferralStatResponse:
    # Direct invite count
    direct_invite_count: int
    # Indirect invite count
    indirect_invite_count: int
    # Total volume traded by direct invites multiple by 1e9
    direct_invite_trading_volume: str
    # Total volume traded by indirect invites multiple by 1e9
    indirect_invite_trading_volume: str


@dataclass
class ApiResolveEpochEcosystemMetricResponse:
    # The name of the epoch
    epoch_name: str
    # Ecosystem points up to the most recently calculated time within this epoch
    point: int
    # The time in unix nanoseconds when the ecosystem points were last calculated
    last_calculated_time: str


@dataclass
class EcosystemMetric:
    # Direct invite count
    direct_invite_count: int
    # Indirect invite count
    indirect_invite_count: int
    # Direct invite trading volume
    direct_invite_trading_volume: str
    # Indirect invite trading volume
    indirect_invite_trading_volume: str
    # Total ecosystem point of this epoch/phase
    total_point: str


@dataclass
class ApiFindFirstEpochMetricResponse:
    # Phase zero metric
    phase_zero_metric: EcosystemMetric
    # Phase one metric
    phase_one_metric: EcosystemMetric
    # The rank of the account in the ecosystem
    rank: int
    # The total number of accounts in the ecosystem
    total: int
    # Total ecosystem point of the first epoch
    total_point: str
    # The time when the ecosystem points were last calculated
    last_calculated_at: str


@dataclass
class EcosystemLeaderboardUser:
    # The off chain account id
    account_id: str
    # The rank of the account in the ecosystem
    rank: int
    # Total ecosystem point
    total_point: str
    # The twitter username of the account
    twitter_username: str


@dataclass
class ApiFindEcosystemLeaderboardResponse:
    # The list of ecosystem leaderboard users
    users: list[EcosystemLeaderboardUser]


@dataclass
class ApiGetListFlatReferralRequest:
    # The off chain referrer account id to get all flat referrals
    referral_id: str
    # Optional. Start time in unix nanoseconds
    start_time: str
    # Optional. End time in unix nanoseconds
    end_time: str
    # The off chain account id to get all user's referrers
    account_id: str


@dataclass
class FlatReferral:
    # The off chain account id
    account_id: str
    # The off chain referrer account id
    referrer_id: str
    # The referrer level; 1: direct referrer, 2: indirect referrer
    referrer_level: int
    # The account creation time
    account_create_time: str
    # The main account id
    main_account_id: str
    # The referrer main account id
    referrer_main_account_id: str


@dataclass
class ApiGetListFlatReferralResponse:
    # The list of flat referrals
    flat_referrals: list[FlatReferral]


@dataclass
class ApiSubAccountTradeRequest:
    """
    The readable name of the instrument. For Perpetual: ETH_USDT_Perp [Underlying Quote Perp]
    For Future: BTC_USDT_Fut_20Oct23 [Underlying Quote Fut DateFormat]
    For Call: ETH_USDT_Call_20Oct23_4123 [Underlying Quote Call DateFormat StrikePrice]
    For Put: ETH_USDT_Put_20Oct23_4123 [Underlying Quote Put DateFormat StrikePrice]
    """

    instrument: str
    # The interval of each sub account trade
    interval: SubAccountTradeInterval
    # The list of sub account ids to query
    sub_account_i_ds: list[str]
    # Optional. The starting time in unix nanoseconds of a specific interval to query
    start_interval: str
    # Optional. Start time in unix nanoseconds
    start_time: str
    # Optional. End time in unix nanoseconds
    end_time: str


@dataclass
class SubAccountTrade:
    # Start of calculation epoch
    start_interval: str
    # The sub account id
    sub_account_id: str
    # The instrument being represented
    instrument: str
    # Total fee paid
    total_fee: str
    # Total volume traded
    total_trade_volume: str


@dataclass
class ApiSubAccountTradeResponse:
    # The sub account trade result set for given interval
    results: list[SubAccountTrade]


@dataclass
class ApiSubAccountTradeAggregationRequest:
    # Optional. The limit of the number of results to return
    limit: int
    # The interval of each sub account trade
    interval: SubAccountTradeInterval
    # The list of sub account ids to query
    sub_account_i_ds: list[str]
    # The sub account id to query greater than
    sub_account_id_greater_than: str
    # Optional. The starting time in unix nanoseconds of a specific interval to query
    start_interval: str
    # Optional. Start time in unix nanoseconds
    start_time: str
    # Optional. End time in unix nanoseconds
    end_time: str


@dataclass
class SubAccountTradeAggregation:
    # The sub account id
    sub_account_id: str
    # Total fee paid
    total_fee: str
    # Total volume traded
    total_trade_volume: str


@dataclass
class ApiSubAccountTradeAggregationResponse:
    # The sub account trade aggregation result set for given interval
    results: list[SubAccountTradeAggregation]


@dataclass
class ApiGetTraderStatResponse:
    # Total fee paid
    total_fee: str


@dataclass
class TraderMetric:
    # Total fee paid
    total_fee: str
    # Total trader point of this epoch/phase
    total_point: str


@dataclass
class ApiFindTraderEpochMetricResponse:
    # Phase zero metric
    metric: TraderMetric
    # The rank of the account in the trader
    rank: int
    # The total number of accounts in the trader
    total: int
    # The time when the trader points were last calculated
    last_calculated_at: str


@dataclass
class TraderLeaderboardUser:
    # The off chain account id
    account_id: str
    # The rank of the account in the Trader
    rank: int
    # Total Trader point
    total_point: str
    # The twitter username of the account
    twitter_username: str


@dataclass
class ApiFindTraderLeaderboardResponse:
    # The list of trader leaderboard users
    users: list[TraderLeaderboardUser]


@dataclass
class WSOrderFeedSelectorV1:
    """
    Subscribes to a feed of order updates pertaining to orders made by your account.
    Each Order can be uniquely identified by its `order_id` or `client_order_id` (if client designs well).
    Use `stateFilter = c` to only receive create events, `stateFilter = u` to only receive update events, and `stateFilter = a` to receive both.
    """

    # The subaccount ID to filter by
    sub_account_id: str
    # The kind filter to apply.
    kind: Kind
    # The underlying filter to apply.
    underlying: Currency
    # The quote filter to apply.
    quote: Currency
    # create only, update only, all
    state_filter: OrderStateFilter


@dataclass
class WSOrderFeedDataV1:
    # Stream name
    stream: str
    # A running sequence number that determines global message order within the specific stream
    sequence_number: str
    # The order object being created or updated
    feed: Order


@dataclass
class WSOrderStateFeedSelectorV1:
    """
    Subscribes to a feed of order updates pertaining to orders made by your account.
    Unlike the Order Stream, this only streams state updates, drastically improving throughput, and latency.
    Each Order can be uniquely identified by its `order_id` or `client_order_id` (if client designs well).
    Use `stateFilter = c` to only receive create events, `stateFilter = u` to only receive update events, and `stateFilter = a` to receive both.
    """

    # The subaccount ID to filter by
    sub_account_id: str
    # The kind filter to apply.
    kind: Kind
    # The underlying filter to apply.
    underlying: Currency
    # The quote filter to apply.
    quote: Currency
    # create only, update only, all
    state_filter: OrderStateFilter


@dataclass
class OrderStateFeed:
    # A unique 128-bit identifier for the order, deterministically generated within the GRVT backend
    order_id: str
    # The order state object being created or updated
    order_state: OrderState


@dataclass
class WSOrderStateFeedDataV1:
    # Stream name
    stream: str
    # A running sequence number that determines global message order within the specific stream
    sequence_number: str
    # The Order State Feed
    feed: OrderStateFeed


@dataclass
class WSPositionsFeedSelectorV1:
    # The subaccount ID to filter by
    sub_account_id: str
    # The kind filter to apply.
    kind: Kind
    # The underlying filter to apply.
    underlying: Currency
    # The quote filter to apply.
    quote: Currency


@dataclass
class WSPositionsFeedDataV1:
    # Stream name
    stream: str
    # A running sequence number that determines global message order within the specific stream
    sequence_number: str
    # A Position being created or updated matching the request filter
    feed: Positions


@dataclass
class WSPrivateTradeFeedSelectorV1:
    # The sub account ID to request for
    sub_account_id: str
    # The kind filter to apply.
    kind: Kind
    # The underlying filter to apply.
    underlying: Currency
    # The quote filter to apply.
    quote: Currency


@dataclass
class WSPrivateTradeFeedDataV1:
    # The websocket channel to which the response is sent
    stream: str
    # A running sequence number that determines global message order within the specific stream
    sequence_number: str
    # A private trade matching the request filter
    feed: PrivateTrade


@dataclass
class Transfer:
    # The account to transfer from
    from_account_id: str
    # The subaccount to transfer from (0 if transferring from main account)
    from_sub_account_id: str
    # The account to deposit into
    to_account_id: str
    # The subaccount to transfer to (0 if transferring to main account)
    to_sub_account_id: str
    # The token currency to transfer
    token_currency: Currency
    # The number of tokens to transfer
    num_tokens: str
    # The signature of the transfer
    signature: Signature


@dataclass
class WSTransferFeedDataV1:
    # The websocket channel to which the response is sent
    stream: str
    # A running sequence number that determines global message order within the specific stream
    sequence_number: str
    # The Transfer object
    feed: Transfer


@dataclass
class Deposit:
    # The hash of the bridgemint event producing the deposit
    tx_hash: str
    # The account to deposit into
    to_account_id: str
    # The token currency to deposit
    token_currency: Currency
    # The number of tokens to deposit
    num_tokens: str


@dataclass
class WSDepositFeedDataV1:
    # The websocket channel to which the response is sent
    stream: str
    # A running sequence number that determines global message order within the specific stream
    sequence_number: str
    # The Deposit object
    feed: Deposit


@dataclass
class Withdrawal:
    # The subaccount to withdraw from
    from_account_id: str
    # The ethereum address to withdraw to
    to_eth_address: str
    # The token currency to withdraw
    token_currency: Currency
    # The number of tokens to withdraw
    num_tokens: str
    # The signature of the withdrawal
    signature: Signature


@dataclass
class WSWithdrawalFeedDataV1:
    # The websocket channel to which the response is sent
    stream: str
    # A running sequence number that determines global message order within the specific stream
    sequence_number: str
    # The Withdrawal object
    feed: Withdrawal


@dataclass
class ApiDepositRequest:
    """
    GRVT runs on a ZKSync Hyperchain which settles directly onto Ethereum.
    To Deposit funds from your L1 wallet into a GRVT SubAccount, you will be required to submit a deposit transaction directly to Ethereum.
    GRVT's bridge verifier will scan Ethereum from time to time. Once it receives proof that your deposit has been confirmed on Ethereum, it will initiate the deposit process.

    This current payload is used for alpha testing only.
    """

    # The main account to deposit into
    to_account_id: str
    # The token currency to deposit
    token_currency: Currency
    # The number of tokens to deposit, quoted in token_currency decimals
    num_tokens: str


@dataclass
class ApiWithdrawalRequest:
    """
    Leverage this API to initialize a withdrawal from GRVT's Hyperchain onto Ethereum.
    Do take note that the bridging process does take time. The GRVT UI will help you keep track of bridging progress, and notify you once its complete.

    If not withdrawing the entirety of your balance, there is a minimum withdrawal amount. Currently that amount is ~25 USDT.
    Withdrawal fees also apply to cover the cost of the Ethereum transaction.
    Note that your funds will always remain in self-custory throughout the withdrawal process. At no stage does GRVT gain control over your funds.
    """

    # The main account to withdraw from
    from_account_id: str
    # The Ethereum wallet to withdraw into
    to_eth_address: str
    # The token currency to withdraw
    token_currency: Currency
    # The number of tokens to withdraw, quoted in tokenCurrency decimal units
    num_tokens: str
    # The signature of the withdrawal
    signature: Signature


@dataclass
class ApiTransferRequest:
    """
    This API allows you to transfer funds in multiple different ways<ul>
    <li>Between SubAccounts within your Main Account</li>
    <li>Between your MainAccount and your SubAccounts</li>
    <li>To other MainAccounts that you have previously allowlisted</li>
    </ul>
    """

    # The main account to transfer from
    from_account_id: str
    # The subaccount to transfer from (0 if transferring from main account)
    from_sub_account_id: str
    # The main account to deposit into
    to_account_id: str
    # The subaccount to transfer to (0 if transferring to main account)
    to_sub_account_id: str
    # The token currency to transfer
    token_currency: Currency
    # The number of tokens to transfer, quoted in tokenCurrency decimal units
    num_tokens: str
    # The signature of the transfer
    signature: Signature


@dataclass
class ApiDepositHistoryRequest:
    """
    The request to get the historical deposits of an account
    The history is returned in reverse chronological order
    """

    # The limit to query for. Defaults to 500; Max 1000
    limit: int
    # The cursor to indicate when to start the next query from
    cursor: str
    # The token currency to query for, if nil or empty, return all deposits. Otherwise, only entries matching the filter will be returned
    token_currency: list[Currency]
    # The start time to query for in unix nanoseconds
    start_time: str
    # The end time to query for in unix nanoseconds
    end_time: str


@dataclass
class DepositHistory:
    # The transaction ID of the deposit
    tx_id: str
    # The txHash of the bridgemint event
    tx_hash: str
    # The account to deposit into
    to_account_id: str
    # The token currency to deposit
    token_currency: Currency
    # The number of tokens to deposit
    num_tokens: str
    # The timestamp of the deposit in unix nanoseconds
    event_time: str


@dataclass
class ApiDepositHistoryResponse:
    # The total number of deposits matching the request account
    total: int
    # The cursor to indicate when to start the next query from
    next: str
    # The deposit history matching the request account
    results: list[DepositHistory]


@dataclass
class ApiTransferHistoryRequest:
    """
    The request to get the historical transfers of an account
    The history is returned in reverse chronological order
    """

    # The limit to query for. Defaults to 500; Max 1000
    limit: int
    # The cursor to indicate when to start the next query from
    cursor: str
    # The token currency to query for, if nil or empty, return all transfers. Otherwise, only entries matching the filter will be returned
    token_currency: list[Currency]
    # The start time to query for in unix nanoseconds
    start_time: str
    # The end time to query for in unix nanoseconds
    end_time: str


@dataclass
class TransferHistory:
    # The transaction ID of the transfer
    tx_id: str
    # The account to transfer from
    from_account_id: str
    # The subaccount to transfer from (0 if transferring from main account)
    from_sub_account_id: str
    # The account to deposit into
    to_account_id: str
    # The subaccount to transfer to (0 if transferring to main account)
    to_sub_account_id: str
    # The token currency to transfer
    token_currency: Currency
    # The number of tokens to transfer
    num_tokens: str
    # The signature of the transfer
    signature: Signature
    # The timestamp of the transfer in unix nanoseconds
    event_time: str


@dataclass
class ApiTransferHistoryResponse:
    # The total number of transfers matching the request account
    total: int
    # The cursor to indicate when to start the next query from
    next: str
    # The transfer history matching the request account
    results: list[TransferHistory]


@dataclass
class ApiWithdrawalHistoryRequest:
    """
    The request to get the historical withdrawals of an account
    The history is returned in reverse chronological order
    """

    # The limit to query for. Defaults to 500; Max 1000
    limit: int
    # The cursor to indicate when to start the next query from
    cursor: str
    # The token currency to query for, if nil or empty, return all withdrawals. Otherwise, only entries matching the filter will be returned
    token_currency: list[Currency]
    # The start time to query for in unix nanoseconds
    start_time: str
    # The end time to query for in unix nanoseconds
    end_time: str


@dataclass
class WithdrawalHistory:
    # The transaction ID of the withdrawal
    tx_id: str
    # The subaccount to withdraw from
    from_account_id: str
    # The ethereum address to withdraw to
    to_eth_address: str
    # The token currency to withdraw
    token_currency: Currency
    # The number of tokens to withdraw
    num_tokens: str
    # The signature of the withdrawal
    signature: Signature
    # The timestamp of the withdrawal in unix nanoseconds
    event_time: str


@dataclass
class ApiWithdrawalHistoryResponse:
    # The total number of withdrawals matching the request account
    total: int
    # The cursor to indicate when to start the next query from
    next: str
    # The withdrawals history matching the request account
    results: list[WithdrawalHistory]
