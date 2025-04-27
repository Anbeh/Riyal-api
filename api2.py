import requests
import json
from bs4 import BeautifulSoup
from datetime import datetime

# لیست ارزهای منتخب
selected_currencies = {
    "USD": {"name": "US Dollar", "flag": "🇺🇸"},
    "EUR": {"name": "Euro", "flag": "🇪🇺"},
    "GBP": {"name": "British Pound", "flag": "🇬🇧"},
    "CHF": {"name": "Swiss Franc", "flag": "🇨🇭"},
    "CAD": {"name": "Canadian Dollar", "flag": "🇨🇦"},
    "TRY": {"name": "Turkish Lira", "flag": "🇹🇷"},
    "RUB": {"name": "Russian Ruble", "flag": "🇷🇺"},
    "CNY": {"name": "Chinese Yuan", "flag": "🇨🇳"},
    "IQD": {"name": "Iraqi Dinar", "flag": "🇮🇶"},
    "AED": {"name": "UAE Dirham", "flag": "🇦🇪"},
    "AFN": {"name": "Afghan Afghani", "flag": "🇦🇫"}
}

# اطلاعات API ارزهای دیجیتال
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

def get_usd_price_toman():
    url = "https://alanchand.com/en/currencies-price/usd-hav"
    headers = {
        "User-Agent": "Mozilla/5.0"
    }
    response = requests.get(url, headers=headers)
    soup = BeautifulSoup(response.text, "html.parser")
    td_tags = soup.find_all("td", {"data-v-c1354816": True})
    if len(td_tags) >= 2:
        text = td_tags[1].text.strip().replace(",", "").replace(" IRR", "")
        usd_to_irr = int(text)
        return usd_to_irr // 10  # تبدیل ریال به تومان
    return None

def scrape_gold_prices(usd_to_toman):
    url = "https://alanchand.com/gold-price/"
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36"
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
                
                price_cell = item.find('div', {'class': 'cell'})
                if price_cell:
                    price_text = price_cell.text.strip().replace(',', '').replace('.','')
                    
                    if title == "XAU":  # فقط برای انس طلا
                        if price_text.replace('.', '', 1).isdigit():
                            price_usd = float(price_text)
                            price_toman = int(price_usd * usd_to_toman)
                            
                            gold_data["gold_prices"].append({
                                "title": title,
                                "price_usd": price_usd,
                                "price_toman": price_toman
                            })
                    else:  # برای سایر انواع طلا
                        if price_text.isdigit():
                            price_irr = int(price_text)
                            price_toman = price_irr // 10
                            
                            gold_data["gold_prices"].append({
                                "title": title,
                                "price_toman": price_toman
                            })
                
            except Exception as item_error:
                print(f"⚠️ خطا در پردازش آیتم طلا: {str(item_error)}")
                continue
        
        return gold_data
    
    except Exception as e:
        print(f"❌ خطا در استخراج داده‌های طلا: {str(e)}")
        return None

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
            currency_rates.append({
                "name": info["name"],
                "code": code,
                "flag": info["flag"],
                "price": price_toman
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

    # ذخیره‌سازی داده‌ها
    with open("data.json", "w", encoding="utf-8") as f:
        json.dump(combined_data, f, indent=2, ensure_ascii=False)

    print("✅ تمام داده‌ها با موفقیت استخراج و در combined_data.json ذخیره شدند")
    return combined_data

if __name__ == "__main__":
    get_all_data()