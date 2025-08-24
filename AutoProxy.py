import os
import requests
from datetime import datetime
from zoneinfo import ZoneInfo   # для Python 3.9+

# URLs
url_1 = "https://raw.githubusercontent.com/1andrevich/Re-filter-lists/main/ooni_domains.lst"
url_2 = "https://raw.githubusercontent.com/1andrevich/Re-filter-lists/main/community.lst"
url_3 = "https://community.antifilter.download/list/domains.lst"
url_4 = "https://raw.githubusercontent.com/itdoginfo/allow-domains/main/Russia/inside-raw.lst"

# Папка для вывода
output_folder = "AutoProxy"
if not os.path.exists(output_folder):
    os.makedirs(output_folder)
output_file = os.path.join(output_folder, "autoproxy.txt")

def download_list(url):
    try:
        print(f"Скачивание списка: {url}")
        response = requests.get(url, timeout=15)
        response.raise_for_status()
        print("Список успешно скачан.")
        return response.text.splitlines()
    except requests.exceptions.RequestException as e:
        print(f"Ошибка при скачивании списка: {e}")
        return []

def extract_domains(lines):
    return {
        line.strip()
        for line in lines
        if line.strip()
        and not line.startswith("#")
        and not line.startswith("!")
    }

def save_to_file(filename, data):
    with open(filename, "w", encoding="utf-8") as file:
        for line in data:
            file.write(line + "\n")
    print(f"Итоговый список сохранён в {filename}")

def process_and_refilter(output_file):
    urls = [url_1, url_2, url_3, url_4]
    all_domains = set()
    for url in urls:
        lines = download_list(url)
        all_domains.update(extract_domains(lines))
    print(f"Объединено {len(all_domains)} уникальных доменов.")

    formatted_domains = [f"||{domain}" for domain in sorted(all_domains) if not domain.startswith("||")]
    domain_count = len(formatted_domains)

    # Точное время по Москве
    current_time = datetime.now(ZoneInfo("Europe/Moscow")).strftime("%Y-%m-%d %H:%M:%S")

    final_output = [
        "[AutoProxy 0.2.9]",
        f"! Generated on : {current_time} (MSK)",
        f"! Domain count: {domain_count}",
        ""
    ] + formatted_domains

    save_to_file(output_file, final_output)

if __name__ == "__main__":
    process_and_refilter(output_file)
