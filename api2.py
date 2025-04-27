import requests
import json
from bs4 import BeautifulSoup
from datetime import datetime

# لیست ارزهای انتخاب‌شده
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

# معادل‌های فارسی طلا
gold_titles = {
    "انس جهانی طلا": "انس طلا",
    "مثقال طلای ۱۸ عیار": "مثقال طلا",
    "یک گرم طلای ۱۸ عیار": "طلای 18 عیار",
    "سکه امامی جدید": "سکه امامی",
    "سکه بهار آزادی": "سکه بهار آزادی",
    "نیم سکه بانکی": "نیم سکه",
    "ربع سکه بانکی": "ربع سکه",
    "سکه گرمی بانک ملی": "سکه گرمی"
}

# آیکون ارزها
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
    'JPY': 'https://www.emoji.co.uk/files/apple-emojis/flags-ios/1121-flag-of-japan.png'
}

# اطلاعات کریپتو
CRYPTO_API = 'https://api.cryptorank.io/v0/coins/prices?keys=bitcoin,ethereum,tether,ripple,bnb,solana,usdcoin,dogecoin,cardano,tron&currency=USD'

crypto_abbreviations = {
    'bitcoin': 'BTC',
    'ethereum': 'ETH',
    'tether': 'USDT',
    'ripple': 'XRP',
    'bnb': 'BNB',
    'solana': 'SOL',
    'usdcoin': 'USDC',
    'dogecoin': 'DOGE',
    'cardano': 'ADA',
    'tron': 'TRX'
}

crypto_icons = {
    'bitcoin': 'https://img.cryptorank.io/coins/60x60.bitcoin1524754012028.png',
    'ethereum': 'https://img.cryptorank.io/coins/60x60.ethereum1524754015525.png',
    'tether': 'https://img.cryptorank.io/coins/60x60.tether1645007690922.png',
    'ripple': 'https://img.cryptorank.io/coins/60x60.xrp1634717634479.png',
    'bnb': 'https://img.cryptorank.io/coins/60x60.bnb1732530324407.png',
    'solana': 'https://img.cryptorank.io/coins/60x60.solana1606979093056.png',
    'usdcoin': 'https://img.cryptorank.io/coins/60x60.usd coin1634317395959.png',
    'dogecoin': 'https://img.cryptorank.io/coins/60x60.dogecoin1524754995294.png',
    'cardano': 'https://img.cryptorank.io/coins/60x60.cardano1524754132195.png',
    'tron': 'https://img.cryptorank.io/coins/60x60.tron1608810047161.png'
}

# دریافت قیمت دلار به تومان
def get_usd_price_toman():
    try:
        url = "https://alanchand.com/en/currencies-price/usd-hav"
        headers = {"User-Agent": "Mozilla/5.0"}
        response = requests.get(url, headers=headers)
        soup = BeautifulSoup(response.text, "html.parser")
        td_tags = soup.find_all("td", {"data-v-c1354816": True})
        if len(td_tags) >= 2:
            text = td_tags[1].text.strip().replace(",", "").replace(" IRR", "")
            usd_to_irr = int(text)
            return usd_to_irr // 10
    except Exception as e:
        print(f"❌ خطا در دریافت قیمت دلار: {e}")
    return None

# دریافت قیمت طلا
def scrape_gold_prices(usd_to_toman):
    try:
        url = "https://alanchand.com/gold-price/"
        headers = {"User-Agent": "Mozilla/5.0"}
        response = requests.get(url, headers=headers)
        response.raise_for_status()
        soup = BeautifulSoup(response.text, 'html.parser')
        
        gold_items = soup.find_all('div', {'data-v-37c0fcfd': True, 'class': 'body cpt'})
        gold_data = {"scraped_at": datetime.now().strftime("%Y-%m-%d %H:%M:%S"), "gold_prices": []}
        
        for item in gold_items:
            title_element = item.find('div', {'class': 'title'}).find('strong')
            if not title_element:
                continue

            original_title = title_element.text.strip()
            if original_title not in gold_titles:
                continue

            translated_title = gold_titles[original_title]
            price_cell = item.find('div', {'class': 'cell'})
            if not price_cell:
                continue

            price_text = price_cell.text.strip().replace(',', '').replace('.', '')

            if original_title == "انس جهانی طلا" and price_text.replace('.', '', 1).isdigit():
                price_usd = float(price_text)
                price_toman = int(price_usd * usd_to_toman)
                gold_data["gold_prices"].append({
                    "title": translated_title,
                    "price_usd": price_usd,
                    "price_toman": price_toman
                })
            elif price_text.isdigit():
                price_toman = int(price_text)
                gold_data["gold_prices"].append({
                    "title": translated_title,
                    "price_toman": price_toman
                })

        return gold_data

    except Exception as e:
        print(f"❌ خطا در دریافت قیمت طلا: {e}")
        return None

# دریافت قیمت کریپتو
def get_crypto_prices():
    try:
        response = requests.get(CRYPTO_API)
        response.raise_for_status()
        data = response.json()
        crypto_data = {"cryptos": []}

        for crypto in data['data']:
            symbol = crypto_abbreviations.get(crypto['key'], crypto['key'].upper())
            price = crypto['price']
            icon = crypto_icons.get(crypto['key'])
            crypto_data["cryptos"].append({
                "name": symbol,
                "price": price,
                "icon": icon
            })
        return crypto_data

    except Exception as e:
        print(f"❌ خطا در دریافت قیمت کریپتو: {e}")
        return None

# جمع آوری تمام داده‌ها
def get_all_data():
    usd_to_toman = get_usd_price_toman()
    if not usd_to_toman:
        print("❌ دریافت قیمت دلار با شکست مواجه شد")
        return None

    response = requests.get("https://open.er-api.com/v6/latest/USD")
    data = response.json()
    rates = data.get("rates", {})
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    currency_rates = []
    for code, info in selected_currencies.items():
        rate = rates.get(code)
        if rate and rate != 0:
            price_toman = int(round((1 / rate) * usd_to_toman))
            icon = currency_icons.get(code)
            currency_rates.append({
                "name": info["name"],
                "code": code,
                "price": price_toman,
                "icon": icon
            })

    gold_data = scrape_gold_prices(usd_to_toman)
    if not gold_data:
        print("❌ دریافت قیمت طلا با شکست مواجه شد")
        return None

    crypto_data = get_crypto_prices()
    if not crypto_data:
        print("❌ دریافت قیمت کریپتو با شکست مواجه شد")
        return None

    combined_data = {
        "checked_at": timestamp,
        "usd_to_toman": usd_to_toman,
        "currency_rates": currency_rates,
        "gold_prices": gold_data["gold_prices"],
        "cryptos": crypto_data["cryptos"]
    }

    # ذخیره فایل
    with open("data2.json", "w", encoding="utf-8") as f:
        json.dump(combined_data, f, indent=2, ensure_ascii=False)

    print("✅ تمام داده‌ها با موفقیت استخراج و در فایل data2.json ذخیره شد")
    return combined_data

if __name__ == "__main__":
    get_all_data()
