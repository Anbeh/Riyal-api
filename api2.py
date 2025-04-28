import requests
import json
from bs4 import BeautifulSoup
from datetime import datetime

# تنظیم داده‌های اولیه
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

gold_titles = {
    "مثقال طلا": "مثقال طلا",
    "یک گرم طلای 18 عیار": "طلای 18 عیار",
    "سکه امامی": "سکه امامی",
    "سکه بهار آزادی": "سکه بهار آزادی",
    "نیم سکه": "نیم سکه",
    "ربع سکه": "ربع سکه",
    "سکه گرمی": "سکه گرمی",
    "انس طلا": "انس طلا"
}

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

# گرفتن قیمت دلار به تومان
def get_usd_price_toman():
    url = "https://alanchand.com/en/currencies-price/usd-hav"
    headers = {"User-Agent": "Mozilla/5.0"}
    response = requests.get(url, headers=headers)
    soup = BeautifulSoup(response.text, "html.parser")
    td_tags = soup.find_all("td", {"data-v-c1354816": True})
    if len(td_tags) >= 2:
        text = td_tags[1].text.strip().replace(",", "").replace(" IRR", "")
        usd_to_irr = int(text)
        return usd_to_irr // 10
    return None

# گرفتن قیمت طلا
def scrape_gold_prices(usd_to_toman):
    url = "https://alanchand.com/gold-price/"
    headers = {
        "User-Agent": "Mozilla/5.0"
    }
    
    try:
        response = requests.get(url, headers=headers)
        response.raise_for_status()
        soup = BeautifulSoup(response.text, 'html.parser')
        
        gold_items = soup.find_all('div', {'data-v-37c0fcfd': True, 'class': 'body cpt'})
        
        gold_data = {
            "scraped_at": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
            "gold_prices": []
        }
        
        for item in gold_items:
            try:
                title_element = item.find('div', {'class': 'title'}).find('strong')
                title = title_element.text.strip() if title_element else "N/A"
                translated_title = gold_titles.get(title, None)
                if not translated_title:
                    continue  # اگر عنوان در لیست نبود، رد کن
                
                price_cell = item.find('div', {'class': 'cell'})
                if price_cell:
                    price_text = price_cell.text.strip().replace(',', '')
                    
                    if title == "انس طلا":
                        if price_text.replace('.', '', 1).isdigit():
                            price_usd = float(price_text)
                            price_toman = int(price_usd * usd_to_toman)
                            gold_data["gold_prices"].append({
                                "title": translated_title,
                                "price_toman": price_toman
                            })
                    else:
                        price_text = price_text.replace('.', '')
                        if price_text.isdigit():
                            price_toman = int(price_text)
                            gold_data["gold_prices"].append({
                                "title": translated_title,
                                "price_toman": price_toman
                            })
                
            except Exception as item_error:
                print(f"⚠️ خطا در پردازش آیتم طلا: {str(item_error)}")
                continue
        
        return gold_data
    
    except Exception as e:
        print(f"❌ خطا در استخراج داده‌های طلا: {str(e)}")
        return None

# گرفتن قیمت کریپتو
def get_crypto_prices():
    try:
        response = requests.get(CRYPTO_API)
        response.raise_for_status()
        data = response.json()
        
        crypto_data = {
            "cryptos": []
        }

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
        print(f"❌ خطا در استخراج داده‌های کریپتو: {str(e)}")
        return None

# گرفتن همه داده‌ها
def get_all_data():
    usd_to_toman = get_usd_price_toman()
    if not usd_to_toman:
        print("❌ Failed to fetch USD to Toman rate.")
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
        print("❌ Failed to fetch gold prices.")
        return None

    crypto_data = get_crypto_prices()
    if not crypto_data:
        print("❌ Failed to fetch crypto prices.")
        return None

    combined_data = {
        "checked_at": timestamp,
        "usd_to_toman": usd_to_toman,
        "currency_rates": currency_rates,
        "gold_prices": gold_data["gold_prices"],
        "cryptos": crypto_data["cryptos"]
    }

    with open("data2.json", "w", encoding="utf-8") as f:
        json.dump(combined_data, f, indent=2, ensure_ascii=False)

    print("✅ تمام داده‌ها با موفقیت استخراج و در data2.json ذخیره شدند")
    return combined_data

# اجرای اصلی
if __name__ == "__main__":
    get_all_data()
