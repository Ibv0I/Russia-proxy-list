import os
import requests
from datetime import datetime
from zoneinfo import ZoneInfo # Python 3.9+

# URLs для загрузки списков
URLS = {
    "community": "https://raw.githubusercontent.com/1andrevich/Re-filter-lists/main/community.lst",
    "domains_all": "https://raw.githubusercontent.com/1andrevich/Re-filter-lists/main/domains_all.lst",
    "ooni": "https://raw.githubusercontent.com/1andrevich/Re-filter-lists/main/ooni_domains.lst",
}

# Папка для итоговых файлов
OUTPUT_DIR = "AutoProxy"
if not os.path.exists(OUTPUT_DIR):
    os.makedirs(OUTPUT_DIR)

OUTPUT_FILES = {
    "community": os.path.join(OUTPUT_DIR, "community_ap.txt"),
    "domains_all": os.path.join(OUTPUT_DIR, "domains_all_ap.txt"),
    "ooni": os.path.join(OUTPUT_DIR, "ooni_ap.txt"),
}

def download_list(url):
    resp = requests.get(url, timeout=20)
    resp.raise_for_status()
    return resp.text.splitlines()

def clean_and_format(lines):
    domains = set()
    for line in lines:
        domain = line.strip()
        if not domain or domain.startswith('#') or domain.startswith('!'):
            continue
        if not domain.startswith('||'):
            domain = '||' + domain
        domains.add(domain)
    return sorted(domains)

def main():
    for name, url in URLS.items():
        print(f"[{name}] Загрузка списка...")
        try:
            lines = download_list(url)
        except Exception as e:
            print(f"[{name}] Ошибка загрузки: {e}")
            continue
        print(f"[{name}] Обработка и форматирование в AutoProxy...")
        rules = clean_and_format(lines)
        domain_count = len(rules)
        # Московское время
        moscow_time = datetime.now(ZoneInfo("Europe/Moscow")).strftime('%Y-%m-%d %H:%M:%S')
        filename = OUTPUT_FILES[name]
        with open(filename, 'w', encoding='utf-8') as f:
            f.write("[AutoProxy 0.2.9]\n")
            f.write(f"! Domain count: {domain_count}\n")
            f.write(f"! Generated on {moscow_time} (MSK)\n\n")
            f.write('\n'.join(rules))
            f.write('\n')
        print(f"[{name}] Готово — сохранено в {filename}\n")

if __name__ == '__main__':
    main()
