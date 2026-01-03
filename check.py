import requests
import os
from datetime import datetime

# ==================================================
# ① 要監控的商品網址（只改這一行）
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
    # ② 判斷邏輯（重點）
    # 有 purchase「且」沒有 sold out 類訊號才通知
    # ==================================================
    has_purchase = "purchase" in html

    sold_out_signals = [
        "sold out",
        "out of stock",
        "품절"
    ]
    is_sold_out = any(word in html for word in sold_out_signals)

    if has_purchase and not is_sold_out:
        print("VALID PURCHASE STATE DETECTED → notify Discord")
        requests.post(
            WEBHOOK,
            json={
                "content": f"🚨 **Weverse 真的可以購買了！**\n{URL}"
            },
            timeout=10
        )
    else:
        print(
            "No valid purchase yet | "
            f"purchase={has_purchase}, sold_out={is_sold_out}"
        )

except Exception as e:
    print("Error occurred:", e)

print("========== Check Finished ==========")
