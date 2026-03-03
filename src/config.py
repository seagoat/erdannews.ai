import json
import os

CONFIG_PATH = os.path.join(os.path.dirname(os.path.dirname(__file__)), 'config.json')

DEFAULT_CONFIG = {
  "feeds": [
    {"name": "V2EX", "url": "https://www.v2ex.com/index.xml"},
    {"name": "Hacker News", "url": "https://hnrss.org/newest"}
  ],
  "keywords": [
    "AI", "大模型", "Python", "开源", "自动化", "前端"
  ]
}

def load_config():
    if not os.path.exists(CONFIG_PATH):
        save_config(DEFAULT_CONFIG)
        return DEFAULT_CONFIG
    try:
        with open(CONFIG_PATH, 'r', encoding='utf-8') as f:
            return json.load(f)
    except Exception:
        return DEFAULT_CONFIG

def save_config(config):
    with open(CONFIG_PATH, 'w', encoding='utf-8') as f:
        json.dump(config, f, indent=4, ensure_ascii=False)
