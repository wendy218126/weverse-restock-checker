import requests
import os

URL = "https://shop.weverse.io/en/shop/USD/artists/3/sales/43782"
WEBHOOK = os.environ["DISCORD_WEBHOOK"]

headers = {
    "User-Agent": "Mozilla/5.0"
}

html = requests.get(URL, headers=headers).text

if True:
    requests.post(
        WEBHOOK,
        json={
            "content": "🚨 **Weverse 補貨啦！**\n" + URL
        }
    )
else:
    print("Still sold out")
