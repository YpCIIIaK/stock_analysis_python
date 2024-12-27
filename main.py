from binance.client import Client as BinanceClient
import pandas as pd
import numpy as np
from datetime import datetime, timezone, timedelta
from telegram import Bot
import asyncio

binance_api_key = 'no see'
binance_api_secret = 'no see'
telegram_token = 'no see'
telegram_chat_id = 'no see'

binance_client = BinanceClient(api_key=binance_api_key, api_secret=binance_api_secret)

bot = Bot(token=telegram_token)

pairs = ['XRPUSDT', 'EOSUSDT', 'LTCUSDT', 'TRXUSDT', 'ETCUSDT', 'LINKUSDT', 'XLMUSDT',
         'ADAUSDT', 'DASHUSDT', 'ZECUSDT', 'XTZUSDT', 'BNBUSDT', 'ATOMUSDT', 'ONTUSDT', 'IOTAUSDT',
         'BATUSDT', 'VETUSDT', 'NEOUSDT', 'QTUMUSDT', 'IOSTUSDT', 'THETAUSDT', 'ALGOUSDT', 'ZILUSDT', 'KNCUSDT',
         'ZRXUSDT', 'COMPUSDT', 'DOGEUSDT', 'SXPUSDT', 'KAVAUSDT', 'BANDUSDT', 'RLCUSDT',
         'MKRUSDT', 'SNXUSDT', 'DOTUSDT', 'YFIUSDT', 'BALUSDT', 'CRVUSDT', 'TRBUSDT', 'RUNEUSDT',
         'SUSHIUSDT', 'EGLDUSDT', 'SOLUSDT', 'ICXUSDT', 'STORJUSDT', 'UNIUSDT', 'AVAXUSDT',
         'FTMUSDT', 'ENJUSDT', 'FLMUSDT',  'KSMUSDT', 'NEARUSDT', 'AAVEUSDT',
         'FILUSDT', 'RSRUSDT', 'LRCUSDT', 'BELUSDT', 'AXSUSDT',
         'ALPHAUSDT', 'ZENUSDT', 'SKLUSDT', 'GRTUSDT', '1INCHUSDT', 'CHZUSDT', 'SANDUSDT', 'ANKRUSDT',
         'LITUSDT', 'RVNUSDT', 'SFPUSDT', 'COTIUSDT', 'CHRUSDT', 'MANAUSDT',
         'ALICEUSDT', 'HBARUSDT', 'ONEUSDT', 'LINAUSDT', 'STMXUSDT', 'DENTUSDT', 'CELRUSDT', 'HOTUSDT', 'MTLUSDT',
         'OGNUSDT', 'NKNUSDT', 'BAKEUSDT', 'GTCUSDT', 'IOTXUSDT',
         'C98USDT', 'MASKUSDT', 'ATAUSDT', 'DYDXUSDT', 'GALAUSDT', 'CELOUSDT',
         'ARUSDT', 'ARPAUSDT', 'CTSIUSDT', 'LPTUSDT', 'ENSUSDT', 'PEOPLEUSDT', 'ROSEUSDT',
         'DUSKUSDT', 'FLOWUSDT', 'IMXUSDT', 'API3USDT', 'GMTUSDT', 'APEUSDT', 'WOOUSDT', 'JASMYUSDT',
         'DARUSDT', 'OPUSDT', 'INJUSDT', 'STGUSDT',  'SPELLUSDT',
         'LDOUSDT', 'CVXUSDT', 'ICPUSDT', 'APTUSDT', 'QNTUSDT', 'FETUSDT', 'FXSUSDT', 'HOOKUSDT',
         'MAGICUSDT', 'TUSDT', 'HIGHUSDT', 'MINAUSDT', 'ASTRUSDT', 'PHBUSDT', 'GMXUSDT',
         'CFXUSDT', 'STXUSDT', 'BNXUSDT', 'ACHUSDT', 'SSVUSDT', 'CKBUSDT', 'PERPUSDT', 'TRUUSDT',
         'LQTYUSDT', 'USDCUSDT', 'IDUSDT', 'ARBUSDT', 'JOEUSDT', 'TLMUSDT', 'AMBUSDT', 'LEVERUSDT', 'RDNTUSDT',
         'HFTUSDT', 'XVSUSDT', 'BLURUSDT', 'EDUUSDT', 'IDEXUSDT', 'SUIUSDT',
         'UMAUSDT', 'RADUSDT', 'COMBOUSDT', 'NMRUSDT', 'MAVUSDT', 'MDTUSDT', 'XVGUSDT', 'WLDUSDT',
         'PENDLEUSDT', 'ARKMUSDT', 'AGLDUSDT', 'YGGUSDT', 'BNTUSDT', 'OXTUSDT', 'SEIUSDT', 'CYBERUSDT',
         'HIFIUSDT', 'ARKUSDT', 'GLMRUSDT', 'BICOUSDT',
         'STPTUSDT', 'WAXPUSDT', 'RIFUSDT', 'POLYXUSDT', 'GASUSDT', 'POWRUSDT', 'SLPUSDT',
         'TIAUSDT', 'SNTUSDT', 'CAKEUSDT', 'MEMEUSDT', 'TWTUSDT', 'ORDIUSDT', 'STEEMUSDT', 'BADGERUSDT',
         'ILVUSDT', 'NTRNUSDT', 'BEAMXUSDT', 'PYTHUSDT', 'SUPERUSDT', 'USTCUSDT',
         'ONGUSDT', 'JTOUSDT', '1000SATSUSDT', 'AUCTIONUSDT', 'ACEUSDT', 'MOVRUSDT',
         'NFPUSDT', 'AIUSDT', 'XAIUSDT', 'WIFUSDT',
         'MANTAUSDT', 'LSKUSDT', 'ALTUSDT', 'JUPUSDT', 'RONINUSDT', 'DYMUSDT',
         'OMUSDT', 'LINKUSDC', 'PIXELUSDT', 'STRKUSDT', 'ORDIUSDC', 'GLMUSDT', 'PORTALUSDT',
         'AXLUSDT', 'METISUSDT', 'AEVOUSDT', 'VANRYUSDT', 'BOMEUSDT',
         'ETHFIUSDT', 'ENAUSDT', 'WUSDT']


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
        return data
    except Exception as e:
        print(f"Ошибка загрузки данных для {pair}: {e}")
        return None


def calculate_rsi(prices, period=14):
    try:
        diff = np.diff(prices)
        gain = np.maximum(diff, 0)
        loss = -np.minimum(diff, 0)
        avg_gain = pd.Series(gain).rolling(window=period).mean()
        avg_loss = pd.Series(loss).rolling(window=period).mean()
        rs = avg_gain / avg_loss
        rsi = 100 - (100 / (1 + rs))
        return rsi.iloc[-1] if not rsi.empty else None
    except Exception as e:
        print(f"Ошибка расчёта RSI: {e}")
        return None


def get_trade_volume_last_interval(data):
    try:
        if data is not None and not data.empty:
            return data["volume"].iloc[-1]
        return None
    except Exception as e:
        print(f"Ошибка получения объёма торгов: {e}")
        return None


async def analyze_pairs():
    for pair in pairs:
        print(f"Анализ пары {pair}...")
        data = fetch_historical_klines(pair)
        if data is not None and len(data) > 1:

            rsi = calculate_rsi(data["close"])
            volume = get_trade_volume_last_interval(data)

            price_change_percent = ((data["close"].iloc[-1] - data["close"].iloc[-2]) / data["close"].iloc[-2]) * 100

            if rsi is not None and volume is not None:
                print(f"Пара: {pair}, RSI: {rsi:.2f}, Объём торгов: {volume}, Изменение цены: {price_change_percent:.2f}%")

                if abs(price_change_percent) > 0.5 or rsi > 89 or rsi < 19:
                    await send_telegram_message(
                        f"Пара: {pair}\nRSI: {rsi:.2f}\nОбъём торгов: {volume}\nИзменение цены: {price_change_percent:.2f}%"
                        f"Ссылка: https://www.binance.com/en-KZ/futures/{pair}"
                    )
            else:
                print(f"Не удалось рассчитать показатели для {pair}.")


async def main():
    while True:
        try:
            await analyze_pairs()
            await asyncio .sleep(1)
        except KeyboardInterrupt:
            print("Программа остановлена пользователем.")
            break
        except Exception as e:
            print(f"Ошибка в основном цикле: {e}")
            await asyncio.sleep(60)


if __name__ == "__main__":
    asyncio.run(main())