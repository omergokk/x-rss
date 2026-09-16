import json
import os
import requests

CONFIG_FILE = "config.json"
OUTPUT_DIR = "feeds"

os.makedirs(OUTPUT_DIR, exist_ok=True)

with open(CONFIG_FILE, "r", encoding="utf-8") as f:
    config = json.load(f)

for account in config["accounts"]:
    username = account["username"]
    name = account["name"]

    print(f"{name} kontrol ediliyor...")

    url = f"https://rsshub.app/twitter/user/{username}"

    try:
        response = requests.get(
            url,
            timeout=30,
            headers={
                "User-Agent": "Mozilla/5.0"
            }
        )

        print(f"HTTP durum kodu: {response.status_code}")

        response.raise_for_status()

        content = response.text

        if "<item" not in content and "<entry" not in content:
            print(f"{username}: RSS verisi bulunamadı.")
            print(content[:500])
            continue

        output_file = os.path.join(
            OUTPUT_DIR,
            f"{username}.xml"
        )

        with open(output_file, "w", encoding="utf-8") as f:
            f.write(content)

        print(f"{username}: RSS oluşturuldu.")

    except Exception as e:
        print(f"{username}: HATA -> {e}")
