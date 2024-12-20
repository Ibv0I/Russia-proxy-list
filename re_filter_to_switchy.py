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
    "community": "community.txt",
    "domains_all": "domains_all.txt",
    "ooni": "ooni.txt",
}

# Функция для загрузки списка
def download_list(url):
    response = requests.get(url)
    response.raise_for_status()
    return response.text.splitlines()

# Функция для преобразования списка в формат Switchy Omega
def convert_to_switchy(lines):
    switchy_lines = []
    for line in lines:
        domain = line.strip()
        if domain and not domain.startswith("#"):
            if domain.startswith("*://"):
                domain = domain.replace("*://", "").split("/", 1)[0]  # Убираем префикс и путь
            switchy_lines.append(f"*://*.{domain}/*")
    return switchy_lines

# Основная функция
def main():
    for name, url in URLS.items():
        print(f"Загружаем список {name}...")
        lines = download_list(url)

        print(f"Преобразуем список {name} в формат Switchy Omega...")
        switchy_lines = convert_to_switchy(lines)

        print(f"Сохраняем список {name} в файл {OUTPUT_FILES[name]}...")
        with open(OUTPUT_FILES[name], "w", encoding="utf-8") as outfile:
            outfile.write("#BEGIN\n\n[Wildcard]\n")
            outfile.write("\n".join(switchy_lines))
            outfile.write("\n#END\n")
            outfile.write(f"# Generated on {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n")

        print(f"Список {name} успешно сохранён в {OUTPUT_FILES[name]}\n")

if __name__ == "__main__":
    main()
