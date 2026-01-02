import requests
import os
from datetime import datetime

# =========================
# ① 要監控的商品網址（只改這一行）
# =========================
URL = "https://shop.weverse.io/en/shop/USD/artists/3/sales/52282"
# 測試用（目前有貨）：
# URL = "https://shop.weverse.io/en/shop/USD/artists/3/sales/52282"

WEBHOOK = os.environ["DISCORD_WEBHOOK"]

headers = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64)"
}

print("SCRIPT STARTED")
print("Checking URL:", URL)
print("Checked at UTC:", datetime.utcnow())

response = requests.get(URL, headers=headers, timeout=20)

# 🔑 一定要轉小寫
html = response.text.lower()

# =========================
# ② 最穩定判斷：只看 purchase
# =========================
if "purchase" in html:
    print("PURCHASE BUTTON DETECTED")
    requests.post(
        WEBHOOK,
        json={
            "content": f"🚨 **Weverse 可以購買了（Purchase 出現）！**\n{URL}"
        },
        timeout=10
    )
else:
    print("No purchase button yet")

print("SCRIPT FINISHED")
