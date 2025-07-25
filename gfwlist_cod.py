import requests
from datetime import datetime

# URLs для загрузки списков
URLS = {
    "community": "https://raw.githubusercontent.com/1andrevich/Re-filter-lists/main/community.lst",
    "domains_all": "https://raw.githubusercontent.com/1andrevich/Re-filter-lists/main/domains_all.lst",
    "ooni": "https://raw.githubusercontent.com/1andrevich/Re-filter-lists/main/ooni_domains.lst",
}

# Выходные файлы
OUTPUT_FILES = {
    "community": "community_gfw.txt",
    "domains_all": "domains_all_gfw.txt",
    "ooni": "ooni_gfw.txt",
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

        print(f"[{name}] Обработка и форматирование в GFWList...")
        rules = clean_and_format(lines)

        filename = OUTPUT_FILES[name]
        with open(filename, 'w', encoding='utf-8') as f:
            f.write(f"! GFWList: {name}\n")
            f.write(f"! Generated on {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n\n")
            f.write('\n'.join(rules))
            f.write('\n')

        print(f"[{name}] Готово — сохранено в {filename}\n")

if __name__ == '__main__':
    main()
