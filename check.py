import requests
import os
from datetime import datetime

# ==================================================
# ① 要監控的商品網址
# ==================================================
URL = "https://shop.weverse.io/en/shop/USD/artists/3/sales/52282"
# 測試用（目前有貨）：
# URL = "https://shop.weverse.io/en/shop/USD/artists/3/sales/52282"

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

    # =========================
    # 核心判斷（實戰版）
    # =========================
    has_purchase = "purchase" in html

    disabled_signals = [
        "disabled",
        "unavailable",
        "not available",
        "sold out",
        "out of stock",
        "품절"
    ]
    is_disabled = any(word in html for word in disabled_signals)

    if has_purchase and not is_disabled:
        print("VALID PURCHASE STATE DETECTED → notify Discord")
        requests.post(
            WEBHOOK,
            json={
                "content": f"🚨 **Weverse 可以購買了！**\n{URL}"
            },
            timeout=10
        )
    else:
        print(
            "Not purchasable yet | "
            f"purchase={has_purchase}, disabled={is_disabled}"
        )

except Exception as e:
    print("Error occurred:", e)

print("========== Check Finished ==========")
