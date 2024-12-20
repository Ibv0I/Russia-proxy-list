import requests
from datetime import datetime

# URLs для загрузки списков
URLS = {
    "antifilter": "https://community.antifilter.download/list/domains.txt",
    "list_1": "https://raw.githubusercontent.com/1andrevich/Re-filter-lists/main/community.lst",
    "list_2": "https://raw.githubusercontent.com/1andrevich/Re-filter-lists/main/ooni_domains.lst",
}

# Имя выходного файла
OUTPUT_FILE = "Re-filter+antifilter.txt"

# Функция для загрузки списка
def download_list(url):
    response = requests.get(url)
    response.raise_for_status()
    return response.text.splitlines()

# Функция для извлечения доменов из формата Switchy Omega
def extract_domains(lines):
    domains = set()
    for line in lines:
        line = line.strip()
        if line.startswith("*://") and "/*" in line:
            domain = line.replace("*://", "").replace("/*", "").lstrip("*")
            domain = domain.replace("..", ".")  # Убираем лишние точки
            domains.add(domain)
    return domains

# Функция для преобразования списка доменов в формат Switchy Omega
def convert_to_switchy(domains):
    switchy_lines = [f"*://*.{domain}/*" for domain in sorted(domains)]
    return switchy_lines

# Основная функция
def main():
    all_domains = set()

    # Обработка списка в формате Switchy Omega
    print("Загружаем и обрабатываем список antifilter...")
    switchy_lines = download_list(URLS["antifilter"])
    all_domains.update(extract_domains(switchy_lines))

    # Обработка дополнительных списков
    for name, url in {"list_1": URLS["list_1"], "list_2": URLS["list_2"]}.items():
        print(f"Загружаем и обрабатываем список {name}...")
        lines = download_list(url)
        all_domains.update(extract_domains(lines))

    # Удаление дубликатов и сортировка
    all_domains = sorted(set(all_domains))

    # Преобразование объединённого списка в формат Switchy Omega
    print("Преобразуем объединённый список в формат Switchy Omega...")
    switchy_lines = convert_to_switchy(all_domains)

    # Сохранение результата в файл
    print(f"Сохраняем результат в файл {OUTPUT_FILE}...")
    with open(OUTPUT_FILE, "w", encoding="utf-8") as outfile:
        outfile.write("#BEGIN\n\n[Wildcard]\n")
        outfile.write("\n".join(switchy_lines))
        outfile.write("\n#END\n")
        outfile.write(f"# Generated on {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n")

    print(f"Список успешно сохранён в {OUTPUT_FILE}")

if __name__ == "__main__":
    main()
