import pandas as pd
from datetime import datetime, timedelta, timezone
from binance.client import Client
import os

# Initialize Binance client
binance_client = Client(os.getenv("BINANCE_API_KEY"), os.getenv("BINANCE_API_SECRET"))

kline_columns = {
    "open_time": "int",
    "open_price": "float",
    "high_price": "float",
    "low_price": "float",
    "close_price": "float",
    "volume": "float",
    "close_time": "int",
    "quote_asset_volume": "float",
    "number_of_trades": "int",
    "taker_buy_base_asset_volume": "float",
    "taker_buy_quote_asset_volume": "float",
    "ignore": "str",
}


def get_klines(
    symbol: str, interval: str, start_time: datetime, end_time: datetime
) -> pd.DataFrame:
    """Fetch klines (candlestick) data from Binance."""
    start_time = int(start_time.timestamp() * 1000)
    end_time = int(end_time.timestamp() * 1000)
    klines = binance_client.get_klines(
        symbol=symbol, interval=interval, startTime=start_time, endTime=end_time
    )
    if not klines:
        print(f"No data found for {symbol} from {start_time} to {end_time}")
        return pd.DataFrame()

    df = pd.DataFrame(klines, columns=kline_columns.keys()).astype(kline_columns)
    df["open_time"] = pd.to_datetime(df["open_time"], unit="ms")
    df["close_time"] = pd.to_datetime(df["close_time"], unit="ms")
    return df


def get_klines_by_date(symbol: str, date: str, interval: str = "1m") -> pd.DataFrame:
    start_time = datetime.strptime(date, "%Y-%m-%d").astimezone(timezone.utc)
    start_time = start_time.replace(
        hour=0, minute=0, second=0, microsecond=0
    )
    end_time = start_time + timedelta(days=1) - timedelta(minutes=1)

    all_klines = []
    current_start = start_time
    while current_start < end_time:
        klines_chunk = get_klines(
            symbol=symbol,
            interval=interval,
            start_time=current_start,
            end_time=end_time,
        )
        if klines_chunk is not None and not klines_chunk.empty:
            all_klines.append(klines_chunk)
            last_time = pd.to_datetime(
                klines_chunk.iloc[-1]["open_time"], unit="ms", utc=True
            )
            current_start = last_time + timedelta(minutes=1)
        else:
            break
    klines = pd.concat(all_klines, ignore_index=True) if all_klines else pd.DataFrame()
    klines["open_time"] = klines["open_time"].dt.strftime("%Y-%m-%d %H:%M:%S")
    klines["close_time"] = klines["close_time"].dt.strftime("%Y-%m-%d %H:%M:%S")
    return klines
