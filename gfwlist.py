import requests
import base64
from datetime import datetime

# URLs для скачивания списков
url_1 = "https://raw.githubusercontent.com/1andrevich/Re-filter-lists/main/ooni_domains.lst"
url_2 = "https://raw.githubusercontent.com/1andrevich/Re-filter-lists/main/community.lst"
url_3 = "https://community.antifilter.download/list/domains.lst"
url_4 = "https://raw.githubusercontent.com/itdoginfo/allow-domains/main/Russia/inside-raw.lst"

# Имя итогового base64-файла
output_file_b64 = "gfwlist.txt"

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
        file.write(data)
    print(f"Итоговый список сохранён в {filename}")

def process_and_refilter(output_file_b64):
    urls = [url_1, url_2, url_3, url_4]
    all_domains = set()
    
    for url in urls:
        lines = download_list(url)
        all_domains.update(extract_domains(lines))

    print(f"Объединено {len(all_domains)} уникальных доменов.")

    # Форматируем для GFWList
    formatted_domains = [f"||{domain}" for domain in sorted(all_domains) if not domain.startswith("||")]

    current_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    # Формируем полный текст
    header = f"! GFWList merged\n! Generated on: {current_time}\n\n"
    body = "\n".join(formatted_domains) + "\n"
    full_text = header + body

    # Кодируем весь текст в base64
    encoded = base64.b64encode(full_text.encode("utf-8")).decode("utf-8")

    # Разбиваем на строки по 76 символов (по желанию)
    chunk_size = 76
    encoded_chunks = [encoded[i:i+chunk_size] for i in range(0, len(encoded), chunk_size)]
    encoded_text = "\n".join(encoded_chunks)

    # Сохраняем только base64-файл
    save_to_file(output_file_b64, encoded_text)

if __name__ == "__main__":
    process_and_refilter(output_file_b64)
