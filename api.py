import requests
from bs4 import BeautifulSoup
import json
from datetime import datetime
from zoneinfo import ZoneInfo

currency_icons = {
    'USD': 'https://www.emoji.co.uk/files/apple-emojis/flags-ios/1236-flag-of-united-states.png',
    'EUR': 'https://www.emoji.co.uk/files/apple-emojis/flags-ios/1084-flag-of-european-union.png',
    'GBP': 'https://www.emoji.co.uk/files/apple-emojis/flags-ios/1235-flag-of-great-britain.png',
    'AED': 'https://www.emoji.co.uk/files/apple-emojis/flags-ios/1234-flag-of-the-united-arab-emirates.png',
    'TRY': 'https://www.emoji.co.uk/files/apple-emojis/flags-ios/1228-flag-of-turkey.png',
    'CNY': 'https://www.emoji.co.uk/files/apple-emojis/flags-ios/1060-flag-of-china.png',
    'CAD': 'https://www.emoji.co.uk/files/apple-emojis/flags-ios/7164-flag-of-canada.png',
    'CHF': 'https://www.emoji.co.uk/files/apple-emojis/flags-ios/1217-flag-of-switzerland.png',
    'RUB': 'https://www.emoji.co.uk/files/apple-emojis/flags-ios/1187-flag-of-russia.png',
    'IQD': 'https://www.emoji.co.uk/files/apple-emojis/flags-ios/1115-flag-of-iraq.png',
}

crypto_icons = {
    'bitcoin': 'https://assets.coingecko.com/coins/images/1/large/bitcoin.png',
    'ethereum': 'https://assets.coingecko.com/coins/images/279/large/ethereum.png',
    'tether': 'https://assets.coingecko.com/coins/images/325/large/Tether.png',
    'ripple': 'https://assets.coingecko.com/coins/images/44/large/xrp-symbol-white-128.png',
    'binancecoin': 'https://assets.coingecko.com/coins/images/825/large/bnb-icon2_2x.png',
    'solana': 'https://assets.coingecko.com/coins/images/4128/large/solana.png',
    'usd-coin': 'https://assets.coingecko.com/coins/images/6319/large/USD_Coin_icon.png',
    'dogecoin': 'https://assets.coingecko.com/coins/images/5/large/dogecoin.png',
    'cardano': 'https://assets.coingecko.com/coins/images/975/large/cardano.png',
    'tron': 'https://assets.coingecko.com/coins/images/1094/large/tron-logo.png'
}

selected_currencies = {
    "USD": {"name": "دلار آمریکا"},
    "EUR": {"name": "یورو"},
    "GBP": {"name": "پوند انگلیس"},
    "CHF": {"name": "فرانک سوئیس"},
    "CAD": {"name": "دلار کانادا"},
    "TRY": {"name": "لیر ترکیه"},
    "RUB": {"name": "روبل روسیه"},
    "CNY": {"name": "یوآن چین"},
    "IQD": {"name": "دینار عراق"},
    "AED": {"name": "درهم امارات"},
}

crypto_names = {
    'bitcoin': 'بیت‌کوین',
    'ethereum': 'اتریوم',
    'tether': 'تتر',
    'ripple': 'ریپل',
    'binancecoin': 'بایننس کوین',
    'solana': 'سولانا',
    'usd-coin': 'یو‌اس‌دی کوین',
    'dogecoin': 'دوج‌کوین',
    'cardano': 'کاردانو',
    'tron': 'ترون'
}

def get_usd_price_toman():
    url = "https://www.tgju.org/profile/price_dollar_rl"
    res = requests.get(url)
    soup = BeautifulSoup(res.text, "html.parser")
    price_tag = soup.select_one("div.block-last-change-percentage span.price[data-col='info.last_trade.PDrCotVal']")
    return int(price_tag.text.replace(",", "")) if price_tag else None

def get_gold_prices():
    url = "https://www.tgju.org/gold-chart"
    res = requests.get(url)
    soup = BeautifulSoup(res.text, "html.parser")

    markets = {
        "geram18": "طلای 18 عیار",
        "gold_740k": "طلای 18 عیار 740",
        "geram24": "طلای 24 عیار",
        "gold_mini_size": "طلای دست دوم"
    }

    gold_data = {}

    for slug, title in markets.items():
        row = soup.select_one(f'tr[data-market-nameslug="{slug}"]')
        if row:
            price_td = row.select_one("td.nf")
            if price_td:
                price = int(price_td.text.replace(",", ""))
                gold_data[title] = price//10

    return {"gold_prices": gold_data}

def get_crypto_prices():
    try:
        url = "https://api.coingecko.com/api/v3/coins/markets"
        params = {
            'vs_currency': 'usd',
            'ids': ','.join(crypto_icons.keys()),
            'order': 'market_cap_desc',
            'per_page': 10,
            'page': 1,
            'sparkline': 'false'
        }
        response = requests.get(url, params=params)
        data = response.json()

        return {
            "cryptos": [
                {
                    "name": coin["symbol"].upper(),
                    "fullname": crypto_names.get(coin["id"], ""),
                    "price": round(coin["current_price"], 2),
                    "icon": crypto_icons.get(coin["id"], "")
                }
                for coin in data
            ]
        }
    except Exception as e:
        print(f"❌ خطا در دریافت قیمت کریپتو: {e}")
        return {"cryptos": []}
    
def get_gold_coins_prices():
    try:
        url = "https://www.tgju.org/coin"
        headers = {
            "User-Agent": "Mozilla/5.0"
        }
        response = requests.get(url, headers=headers)
        soup = BeautifulSoup(response.text, 'html.parser')

        table = soup.find("table", class_="market-table")
        rows = table.find("tbody").find_all("tr")

        result = []

        for row in rows:
            cells = row.find_all("td")
            title = row.find("th").text.strip()

            if len(cells) >= 5:
                cash_price = cells[0].text.strip()

                result.append({
                    "title": title,
                    "price": int(cash_price.replace(",", "")) // 10,
                })

        return {"gold_coins": result}
    
    except Exception as e:
        print(f"❌ خطا در دریافت اطلاعات سکه‌ها: {e}")
        return {"gold_coins": []}

def get_currency_rates(usd_to_toman):
    try:
        url = "https://open.er-api.com/v6/latest/USD"
        response = requests.get(url)
        data = response.json()
        rates = data.get("rates", {})

        currency_rates = []
        for code, info in selected_currencies.items():
            rate = rates.get(code)
            if rate:
                price_toman = int(round((1 / rate) * usd_to_toman)) // 10
                currency_rates.append({
                    "name": info["name"],
                    "code": code,
                    "price": price_toman,
                    "icon": currency_icons.get(code)
                })
        return currency_rates
    except Exception as e:
        print(f"❌ خطا در دریافت نرخ ارز: {e}")
        return []

def get_all_data():
    usd_to_toman = get_usd_price_toman()
    if not usd_to_toman:
        print("❌ دریافت قیمت دلار با شکست مواجه شد")
        return

    currency_rates = get_currency_rates(usd_to_toman)
    gold_data = get_gold_prices()
    crypto_data = get_crypto_prices()
    gold_coins_data = get_gold_coins_prices()

    result = {
        "checked_at": datetime.now(ZoneInfo("Asia/Tehran")).strftime("%Y-%m-%d %H:%M:%S"),
        "usd_to_toman": usd_to_toman,
        "currency_rates": currency_rates,
        "gold_prices": gold_data["gold_prices"],
        "gold_coins": gold_coins_data["gold_coins"],
        "cryptos": crypto_data["cryptos"],
    }

    with open("data2.json", "w", encoding="utf-8") as f:
        json.dump(result, f, indent=2, ensure_ascii=False)

    print("✅ داده‌ها با موفقیت ذخیره شدند در فایل data2.json")

if __name__ == "__main__":
    get_all_data()
