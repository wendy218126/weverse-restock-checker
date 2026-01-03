import requests
import os
from datetime import datetime

URL = "https://shop.weverse.io/en/shop/USD/artists/3/sales/43782"

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

    if "purchase" in html:
        requests.post(
            WEBHOOK,
            json={
                "content": f"🚨 **Weverse 可以購買了（Purchase 出現）！**\n{URL}"
            },
            timeout=10
        )
        print("PURCHASE detected")
    else:
        print("No purchase button yet")

except Exception as e:
    print("Error occurred:", e)

print("========== Check Finished ==========")
