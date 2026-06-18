import requests
from bs4 import BeautifulSoup
import os

PRODUCT_URL = "https://www.freepeople.com/shop/we-the-free-baby-emerson-tote-bag/"

COLOR_NAME = "Peony"

NTFY_TOPIC = os.getenv("NTFY_TOPIC")

headers = {
    "User-Agent": "Mozilla/5.0"
}

response = requests.get(PRODUCT_URL, headers=headers, timeout=30)
response.raise_for_status()

soup = BeautifulSoup(response.text, "html.parser")

found = False

for img in soup.find_all("img"):
    alt = img.get("alt", "").strip()

    if alt.lower() == COLOR_NAME.lower():
        stock = img.get("isoutofstock", "").lower()

        if stock == "false":
            found = True
            break

if found:
    print(f"{COLOR_NAME} is available!")

    if NTFY_TOPIC:
        requests.post(
            f"https://ntfy.sh/{NTFY_TOPIC}",
            data=f"🌸 {COLOR_NAME} is now available!\n{PRODUCT_URL}".encode("utf-8"),
            headers={
                "Title": "Free People Restock!",
                "Priority": "5"
            },
            timeout=30
        )
else:
    print(f"{COLOR_NAME} not found or out of stock.")
