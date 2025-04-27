def scrape_gold_prices(usd_to_toman):
    try:
        url = "https://alanchand.com/gold-price/"
        headers = {"User-Agent": "Mozilla/5.0"}
        response = requests.get(url, headers=headers)
        response.raise_for_status()
        soup = BeautifulSoup(response.text, 'html.parser')

        gold_data = {"scraped_at": datetime.now().strftime("%Y-%m-%d %H:%M:%S"), "gold_prices": []}

        # همه آیتم‌های طلا
        all_items = soup.find_all('div', class_='body')

        for item in all_items:
            title_tag = item.find('div', class_='title')
            if not title_tag:
                continue

            title_text = title_tag.get_text(strip=True)
            if title_text not in gold_titles:
                continue  # اگر جزو gold_titles نبود، بیخیالش شو

            translated_title = gold_titles[title_text]

            price_tag = item.find('div', class_='cell')
            if not price_tag:
                continue

            price_text = price_tag.get_text(strip=True).replace(',', '')

            # حالت خاص انس جهانی (دلار قیمتشه، بقیه تومان)
            if title_text == "انس جهانی طلا":
                if price_text.replace('.', '', 1).isdigit():
                    price_usd = float(price_text)
                    price_toman = int(price_usd * usd_to_toman)
                    gold_data["gold_prices"].append({
                        "title": translated_title,
                        "price_usd": price_usd,
                        "price_toman": price_toman
                    })
            else:
                if price_text.isdigit():
                    price_toman = int(price_text)
                    gold_data["gold_prices"].append({
                        "title": translated_title,
                        "price_toman": price_toman
                    })

        return gold_data

    except Exception as e:
        print(f"❌ خطا در دریافت قیمت طلا: {e}")
        return None
