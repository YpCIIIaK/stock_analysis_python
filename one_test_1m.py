from binance.client import Client as BinanceClient
import pandas as pd
import numpy as np
from datetime import datetime, timezone, timedelta
from telegram import Bot
import asyncio
import ta

binance_api_key = 'no see'
binance_api_secret = 'no see'
telegram_token = 'no see'
telegram_chat_id = 'no see'

binance_client = BinanceClient(api_key=binance_api_key, api_secret=binance_api_secret)
bot = Bot(token=telegram_token)

pair = 'BTCUSDT'

async def send_telegram_message(text):
    try:
        await bot.send_message(chat_id=telegram_chat_id, text=text)
    except Exception as e:
        print(f"Ошибка отправки сообщения: {e}")

def fetch_historical_klines(pair, interval='1m', lookback_minutes=60):
    try:
        now = datetime.now(timezone.utc)
        start_time = int((now - timedelta(minutes=lookback_minutes)).timestamp() * 1000)
        klines = binance_client.get_historical_klines(pair, interval, start_time)
        data = pd.DataFrame(klines, columns=[
            "timestamp", "open", "high", "low", "close", "volume", "close_time",
            "quote_asset_volume", "number_of_trades", "taker_buy_base", "taker_buy_quote", "ignore"
        ])
        data["close"] = data["close"].astype(float)
        data["volume"] = data["volume"].astype(float)
        data["high"] = data["high"].astype(float)
        data["low"] = data["low"].astype(float)
        data["timestamp"] = pd.to_datetime(data["timestamp"], unit='ms')
        return data
    except Exception as e:
        print(f"Ошибка загрузки данных для {pair}: {e}")
        return None

def calculate_rsi(prices, period=14):
    return ta.momentum.RSIIndicator(close=prices, window=period).rsi().iloc[-1]

def calculate_macd(prices):
    macd = ta.trend.MACD(close=prices)
    return macd.macd().iloc[-1], macd.macd_signal().iloc[-1]

def calculate_bollinger_bands(prices, window=20, num_std_dev=2):
    bb = ta.volatility.BollingerBands(close=prices, window=window, window_dev=num_std_dev)
    return bb.bollinger_hband().iloc[-1], bb.bollinger_lband().iloc[-1]

def calculate_adx(data, period=14):
    adx = ta.trend.ADXIndicator(high=data['high'], low=data['low'], close=data['close'], window=period)
    return adx.adx().iloc[-1]

def calculate_cci(data, period=20):
    cci = ta.trend.CCIIndicator(high=data['high'], low=data['low'], close=data['close'], window=period)
    return cci.cci().iloc[-1]

def calculate_williams_r(data, period=14):
    williams_r = ta.momentum.WilliamsRIndicator(high=data['high'], low=data['low'], close=data['close'])
    return williams_r.williams_r().iloc[-1]

def calculate_stochastic(data, k_window=14, d_window=3):
    stoch = ta.momentum.StochasticOscillator(high=data['high'], low=data['low'], close=data['close'], window=k_window, smooth_window=d_window)
    return stoch.stoch().iloc[-1], stoch.stoch_signal().iloc[-1]

def calculate_ema(prices, period=14):
    return ta.trend.EMAIndicator(close=prices, window=period).ema_indicator().iloc[-1]

def calculate_atr(data, period=14):
    atr = ta.volatility.AverageTrueRange(high=data['high'], low=data['low'], close=data['close'], window=period)
    return atr.average_true_range().iloc[-1]

def calculate_parabolic_sar(data):
    psar = ta.trend.PSARIndicator(high=data['high'], low=data['low'], close=data['close'])
    return psar.psar().iloc[-1]

def calculate_obv(data):
    obv = ta.volume.OnBalanceVolumeIndicator(close=data['close'], volume=data['volume'])
    return obv.on_balance_volume().iloc[-1]

def calculate_mfi(data, period=14):
    mfi = ta.volume.MFIIndicator(high=data['high'], low=data['low'], close=data['close'], volume=data['volume'], window=period)
    return mfi.money_flow_index().iloc[-1]

def generate_recommendation(
    rsi, macd, signal, price, upper_band, lower_band, adx, cci, williams_r, stoch_k, stoch_d,
    ema, atr, psar, obv, mfi
):
    recommendations = {
        "RSI": "Нет рекомендации.",
        "MACD": "Нет рекомендации.",
        "Bollinger": "Нет рекомендации.",
        "ADX": "Нет рекомендации.",
        "CCI": "Нет рекомендации.",
        "Williams %R": "Нет рекомендации.",
        "Stochastic": "Нет рекомендации.",
        "EMA": "Нет рекомендации.",
        "ATR": "Нет рекомендации.",
        "Parabolic SAR": "Нет рекомендации.",
        "OBV": "Нет рекомендации.",
        "MFI": "Нет рекомендации."
    }
    buy_count = 0
    sell_count = 0

    if price > ema:
        recommendations["EMA"] = "Цена выше EMA, тренд восходящий."
        buy_count += 1
    else:
        recommendations["EMA"] = "Цена ниже EMA, тренд нисходящий."
        sell_count += 1

    if atr > 0.5:
        recommendations["ATR"] = "Высокая волатильность, будьте осторожны."
    else:
        recommendations["ATR"] = "Низкая волатильность, рынок спокоен."

    if price > psar:
        recommendations["Parabolic SAR"] = "Тренд восходящий."
        buy_count += 1
    else:
        recommendations["Parabolic SAR"] = "Тренд нисходящий."
        sell_count += 1

    if obv > 0:
        recommendations["OBV"] = "Объем подтверждает рост."
        buy_count += 1
    else:
        recommendations["OBV"] = "Объем подтверждает снижение."
        sell_count += 1

    if mfi > 80:
        recommendations["MFI"] = "Перекупленность, возможно, стоит продавать."
        sell_count += 1
    elif mfi < 20:
        recommendations["MFI"] = "Перепроданность, возможно, стоит покупать."
        buy_count += 1

    if buy_count > sell_count:
        recommendations["Общая рекомендация"] = "Рекомендуется покупать."
    elif sell_count > buy_count:
        recommendations["Общая рекомендация"] = "Рекомендуется продавать."
    else:
        recommendations["Общая рекомендация"] = "Нет четкой рекомендации."

    return recommendations

async def analyze_data():
    data = fetch_historical_klines(pair)
    if data is not None:
        prices = data['close']
        rsi = calculate_rsi(prices)
        macd, signal = calculate_macd(prices)
        upper_band, lower_band = calculate_bollinger_bands(prices)
        adx = calculate_adx(data)
        cci = calculate_cci(data)
        williams_r = calculate_williams_r(data)
        stoch_k, stoch_d = calculate_stochastic(data)
        ema = calculate_ema(prices)
        atr = calculate_atr(data)
        psar = calculate_parabolic_sar(data)
        obv = calculate_obv(data)
        mfi = calculate_mfi(data)

        recommendations = generate_recommendation(
            rsi, macd, signal, prices.iloc[-1], upper_band, lower_band, adx, cci, williams_r, stoch_k, stoch_d, ema, atr, psar, obv, mfi)

        print(f"Цена: {prices.iloc[-1]:.2f}")
        print(f"RSI: {rsi:.2f} - {recommendations['RSI']}")
        print(f"MACD: {macd:.2f}, Signal: {signal:.2f} - {recommendations['MACD']}")
        print(f"Upper Band: {upper_band:.2f}, Lower Band: {lower_band:.2f} - {recommendations['Bollinger']}")
        print(f"ADX: {adx:.2f} - {recommendations['ADX']}")
        print(f"CCI: {cci:.2f} - {recommendations['CCI']}")
        print(f"Williams %R: {williams_r:.2f} - {recommendations['Williams %R']}")
        print(f"Stochastic K: {stoch_k:.2f}, Stochastic D: {stoch_d:.2f} - {recommendations['Stochastic']}")
        print(f"EMA: {ema:.2f} - {recommendations['EMA']}")
        print(f"ATR: {atr:.2f} - {recommendations['ATR']}")
        print(f"Parabolic SAR: {psar:.2f} - {recommendations['Parabolic SAR']}")
        print(f"OBV: {obv:.2f} - {recommendations['OBV']}")
        print(f"MFI: {mfi:.2f} - {recommendations['MFI']}")
        print(f"Общая рекомендация: {recommendations['Общая рекомендация']}")

        message = "Рекомендации по BTC/USDT:\n"
        for indicator, recommendation in recommendations.items():
            message += f"{indicator}: {recommendation}\n"

        await send_telegram_message(message)

async def main():
    while True:
        await analyze_data()
        await asyncio.sleep(60)

if __name__ == "__main__":
    asyncio.run(main())