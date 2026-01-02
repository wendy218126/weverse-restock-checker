import requests
import os

URL = "https://shop.weverse.io/en/shop/USD/artists/3/sales/52282"
WEBHOOK = os.environ["DISCORD_WEBHOOK"]

headers = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64)"
}

html = requests.get(URL, headers=headers, timeout=15).text.lower()

# 常見售罄關鍵字（保守寫法）
sold_out_keywords = [
    "sold out",
    "out of stock",
    "품절"
]

is_sold_out = any(keyword in html for keyword in sold_out_keywords)

if not is_sold_out:
    requests.post(
        WEBHOOK,
        json={
            "content": f"🚨 **Weverse 補貨偵測到有庫存！**\n{URL}"
        },
        timeout=10
    )
    print("RESTOCK DETECTED → Discord notified")
else:
    print("Still sold out")
