import datetime
import os
import requests
from typing import Dict, Any

TELEGRAM_BOT_TOKEN = os.environ["BOT_TOKEN"]
TELEGRAM_CHAT_ID = os.environ["CHAT_ID"]

def fetch_weather_moscow() -> str:
    # Москва: 55.7558, 37.6176
    url = (
        "https://api.open-meteo.com/v1/forecast"
        "?latitude=55.7558&longitude=37.6176"
        "&hourly=temperature_2m,precipitation_probability,weathercode"
        "&daily=temperature_2m_max,temperature_2m_min,precipitation_sum,weathercode"
        "&timezone=Europe%2FMoscow"
    )
    r = requests.get(url, timeout=20)
    r.raise_for_status()
    data = r.json()
    today = data["daily"]
    t_min = today["temperature_2m_min"][0]
    t_max = today["temperature_2m_max"][0]
    precip = today.get("precipitation_sum", [0])[0]
    code = today["weathercode"][0]
    desc = weathercode_to_text(code)
    return f"Погода (Москва): {desc}, мин {t_min:.0f}°C, макс {t_max:.0f}°C, осадки {precip:.1f} мм"

def weathercode_to_text(code: int) -> str:
    mapping = {
        0: "ясно",
        1: "в осн. ясно",
        2: "переменная облачность",
        3: "облачно",
        45: "туман",
        48: "изморозь",
        51: "легкая морось",
        53: "морось",
        55: "сильная морось",
        61: "легкий дождь",
        63: "дождь",
        65: "ливень",
        66: "ледяной дождь",
        67: "сильный ледяной дождь",
        71: "легкий снег",
        73: "снег",
        75: "сильный снег",
        80: "кратковременные дожди",
        81: "сильные кратковременные дожди",
        82: "оч. сильные кратковременные дожди",
        85: "снегопад",
        86: "сильный снегопад",
        95: "гроза",
        96: "гроза с градом",
        99: "сильная гроза с градом",
    }
    return mapping.get(code, f"код {code}")

def fetch_fx() -> str:
    # ЦБ РФ: курсы на сегодня/последний рабочий день
    r = requests.get("https://www.cbr-xml-daily.ru/daily_json.js", timeout=20)
    r.raise_for_status()
    data = r.json()["Valute"]
    usd = data["USD"]["Value"]
    eur = data["EUR"]["Value"]
    return f"Курсы ЦБ: USD {usd:.2f} ₽, EUR {eur:.2f} ₽"

def fetch_crypto() -> str:
    # CoinGecko simple price (USD)
    ids = "bitcoin,ethereum,solana"
    url = f"https://api.coingecko.com/api/v3/simple/price?ids={ids}&vs_currencies=usd"
    r = requests.get(url, timeout=20, headers={"Accept": "application/json"})
    r.raise_for_status()
    d: Dict[str, Any] = r.json()
    btc = d["bitcoin"]["usd"]
    eth = d["ethereum"]["usd"]
    sol = d["solana"]["usd"]
    # format with thousands separators and no decimals; replace comma with thin space for readability
    btc_str = f"${btc:,.0f}".replace(",", " ")
    eth_str = f"${eth:,.0f}".replace(",", " ")
    sol_str = f"${sol:,.0f}".replace(",", " ")
    return f"₿ Крипто (USD): BTC {btc_str}, ETH {eth_str}, SOL {sol_str}"

def send_telegram_message(text: str) -> None:
    url = f"https://api.telegram.org/bot{TELEGRAM_BOT_TOKEN}/sendMessage"
    payload = {"chat_id": TELEGRAM_CHAT_ID, "text": text, "parse_mode": "HTML", "disable_web_page_preview": True}
    r = requests.post(url, json=payload, timeout=20)
    r.raise_for_status()

def build_message() -> str:
    today = datetime.datetime.now(datetime.timezone(datetime.timedelta(hours=3)))  # MSK
    date_str = today.strftime("%d.%m.%Y")
    parts = [
        f"🌅 Доброе утро! Сводка на {date_str}",
        "",
        f"☀️ {fetch_weather_moscow()}",
        f"💱 {fetch_fx()}",
        f"💹 {fetch_crypto()}",
    ]
    return "\n".join(parts)

def main() -> None:
    try:
        msg = build_message()
        send_telegram_message(msg)
    except Exception as e:
        try:
            send_telegram_message(f"Ошибка утренней сводки: {e}")
        except Exception:
            pass
        raise

if __name__ == "__main__":
    main()
