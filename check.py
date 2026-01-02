import requests
import os
from datetime import datetime

# =========================
# ① 要監控的商品網址（只改這裡）
# =========================
URL = "https://shop.weverse.io/en/shop/USD/artists/3/sales/43782"
# 測試時你可以暫時改成：
# URL = "https://shop.weverse.io/en/shop/USD/artists/3/sales/52282"

WEBHOOK = os.environ["DISCORD_WEBHOOK"]

headers = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64)"
}

print("SCRIPT STARTED")
print("Checking URL:", URL)
print("Checked at UTC:", datetime.utcnow())

response = requests.get(URL, headers=headers, timeout=20)
html = response.text.lower()

# =========================
# ② 「手機穩定版」購買訊號判斷
# （寧願多叫，也不要漏）
# =========================
buy_signals = [
    "add to cart",
    "buy now",
    "purchase",
    "checkout",
    "cart",
    "order",
]

has_buy_signal = any(signal in html for signal in buy_signals)

if has_buy_signal:
    print("BUY SIGNAL DETECTED")
    requests.post(
        WEBHOOK,
        json={
            "content": f"🚨 **Weverse 可能補貨了！快查看**\n{URL}"
        },
        timeout=10
    )
else:
    print("No buy signal yet (probably sold out)")

print("SCRIPT FINISHED")
