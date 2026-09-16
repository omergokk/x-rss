import json
import os
import requests
from datetime import datetime
from xml.sax.saxutils import escape

CONFIG_FILE = "config.json"
OUTPUT_DIR = "feeds"

os.makedirs(OUTPUT_DIR, exist_ok=True)

with open(CONFIG_FILE, "r", encoding="utf-8") as f:
    config = json.load(f)

def get_tweets(username):
    url = f"https://rsshub.app/twitter/user/{username}"
    
    try:
        response = requests.get(
            url,
            timeout=30,
            headers={
                "User-Agent": "Mozilla/5.0"
            }
        )
        response.raise_for_status()
        return response.text
    except Exception as e:
        print(f"{username} alınamadı: {e}")
        return None

def save_feed(username, name, content):
    if not content:
        return

    path = os.path.join(OUTPUT_DIR, f"{username}.xml")

    with open(path, "w", encoding="utf-8") as f:
        f.write(content)

    print(f"{name}: {path} oluşturuldu")

for account in config["accounts"]:
    username = account["username"]
    name = account["name"]

    print(f"{name} kontrol ediliyor...")
    
    feed = get_tweets(username)
    save_feed(username, name, feed)
