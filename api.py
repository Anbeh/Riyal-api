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
        return usd_to_irr // 10  # Convert IRR to Toman
    return None

def get_selected_rates_in_toman():
    response = requests.get("https://open.er-api.com/v6/latest/USD")
    data = response.json()
    usd_to_toman = get_usd_price_toman()
    if not usd_to_toman:
        print("❌ Failed to fetch USD to Toman rate.")
        return

    rates = data.get("rates", {})
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    result = {
        "checked_at": timestamp,
        "usd_to_toman": usd_to_toman,
        "selected_rates": []
    }

    for code, info in selected_currencies.items():
        rate = rates.get(code)
        if rate and rate != 0:
            price_toman = int(round((1 / rate) * usd_to_toman))
            result["selected_rates"].append({
                "name": info["name"],
                "code": code,
                "flag": info["flag"],
                "price": price_toman
            })

    with open("data.json", "w", encoding="utf-8") as f:
        json.dump(result, f, indent=2, ensure_ascii=False)

    print("✅ Saved formatted exchange rates to data.json")

if __name__ == "__main__":
    get_selected_rates_in_toman()