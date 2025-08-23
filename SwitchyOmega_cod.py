import os
import requests
from datetime import datetime
from zoneinfo import ZoneInfo  # для Python 3.9+

# URLs для загрузки списков
URLS = {
    "community": "https://raw.githubusercontent.com/1andrevich/Re-filter-lists/main/community.lst",
    "domains_all": "https://raw.githubusercontent.com/1andrevich/Re-filter-lists/main/domains_all.lst",
    "ooni": "https://raw.githubusercontent.com/1andrevich/Re-filter-lists/main/ooni_domains.lst",
}

# Папка для итоговых файлов
OUTPUT_DIR = "SwitchyOmega"
if not os.path.exists(OUTPUT_DIR):
    os.makedirs(OUTPUT_DIR)

OUTPUT_FILES = {
    "community": os.path.join(OUTPUT_DIR, "community_so.txt"),
    "domains_all": os.path.join(OUTPUT_DIR, "domains_all_so.txt"),
    "ooni": os.path.join(OUTPUT_DIR, "ooni_so.txt"),
}

def download_list(url):
    response = requests.get(url)
    response.raise_for_status()
    return response.text.splitlines()

def convert_to_switchy(lines):
    switchy_lines = []
    for line in lines:
        domain = line.strip()
        if domain and not domain.startswith("#"):
            if domain.startswith("*://"):
                domain = domain.replace("*://", "").split("/", 1)[0]  # Убираем префикс и путь
            switchy_lines.append(f"*://*.{domain}/*")
    return switchy_lines

def main():
    for name, url in URLS.items():
        print(f"Загружаем список {name}...")
        lines = download_list(url)
        print(f"Преобразуем список {name} в формат Switchy Omega...")
        switchy_lines = convert_to_switchy(lines)
        domain_count = len(switchy_lines)
        filename = OUTPUT_FILES[name]
        print(f"Сохраняем список {name} в файл {filename}...")
        with open(filename, "w", encoding="utf-8") as outfile:
            outfile.write("#BEGIN\n")
            outfile.write("[Wildcard]\n")
            outfile.write("\n".join(switchy_lines))
            outfile.write("\n#END\n")
            outfile.write(f"# Domain count: {domain_count}\n\n")
            current_time = datetime.now(ZoneInfo("Europe/Moscow")).strftime('%Y-%m-%d %H:%M:%S')
            outfile.write(f"# Generated on {current_time} (MSK)\n")
        print(f"Список {name} успешно сохранён в {filename}\n")

if __name__ == "__main__":
    main()
