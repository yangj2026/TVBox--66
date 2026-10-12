#!/usr/bin/env python3
"""
scripts/fetch_tvbox.py

Fetches the TVBOX VOD list from the provided API and writes it to data/tvbox_list.json.

Usage:
  python scripts/fetch_tvbox.py

Requirements:
  pip install requests

This script attempts to parse the response as JSON. If parsing fails, it will save the
raw response text under the "raw" field in the output JSON so you can inspect and
convert it later.

Output path: data/tvbox_list.json
"""

import json
import os
import sys
from datetime import datetime

import requests

URL = "https://ckzy.me/api.php/provide/vod/?ac=list"
OUT_DIR = "data"
OUT_PATH = os.path.join(OUT_DIR, "tvbox_list.json")


def fetch_and_save(url=URL, out_path=OUT_PATH, timeout=15):
    os.makedirs(os.path.dirname(out_path), exist_ok=True)

    try:
        resp = requests.get(url, timeout=timeout)
        resp.raise_for_status()
    except Exception as e:
        print(f"Request failed: {e}")
        sys.exit(1)

    content_type = resp.headers.get("Content-Type", "")
    text = resp.text

    result = {
        "source": url,
        "fetched_at": datetime.utcnow().isoformat() + "Z",
        "content_type": content_type,
    }

    try:
        result["data"] = resp.json()
        result["format"] = "json"
    except ValueError:
        # Not JSON — save raw text
        result["raw"] = text
        result["format"] = "text_or_other"

    with open(out_path, "w", encoding="utf-8") as f:
        json.dump(result, f, ensure_ascii=False, indent=2)

    print(f"Saved API response to {out_path} (format={result.get('format')})")


if __name__ == "__main__":
    fetch_and_save()
