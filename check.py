import requests
import os
from datetime import datetime

# ==================================================
# ① 要監控的商品網址（只改這一行即可）
# ==================================================
URL = "https://shop.weverse.io/en/shop/USD/artists/3/sales/43782"
# 測試用（目前有貨）：
# URL = "https://shop.weverse.io/en/shop/USD/artists/3/sales/52282"

# Discord Webhook（從 GitHub Secrets 讀）
WEBHOOK = os.environ["DISCORD_WEBHOOK"]

headers = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64)"
}

print("========== Weverse Restock Check ==========")
print("Time (UTC):", datetime.utcnow())
print("Checking URL:", URL)

try:
    response = requests.get(URL, headers=headers, timeout=20)
    html = response.text.lower()

    # ==================================================
    # ② 最穩定判斷條件：只看「purchase」
    # ==================================================
    if "purchase" in html:
        print("PURCHASE detected → sending Discord notification")
        requests.post(
            WEBHOOK,
            json={
                "content": f"🚨 **Weverse 可以購買了（Purchase 出現）！**\n{URL}"
            },
            timeout=10
        )
    else:
        print("No purchase button yet (still sold out)")

except Exception as e:
    print("Error occurred:", e)

print("========== Check Finished ==========")
