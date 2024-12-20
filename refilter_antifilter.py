import requests
from datetime import datetime

# URLs для скачивания списков
url_ooni = "https://raw.githubusercontent.com/1andrevich/Re-filter-lists/main/ooni_domains.lst"  # URL ooni списка
url_community = "https://raw.githubusercontent.com/1andrevich/Re-filter-lists/main/community.lst"  # URL community списка
url_antifilter = "https://community.antifilter.download/list/domains.lst"  # URL списка antifilter 

# Имя итогового файла
output_file = "Re-filter+antifilter.txt"

def download_list(url):
    """Скачивает список доменов по URL."""
    try:
        print(f"Скачивание списка: {url}")
        response = requests.get(url)
        response.raise_for_status()
        print("Список успешно скачан.")
        return response.text.splitlines()
    except requests.exceptions.RequestException as e:
        print(f"Ошибка при скачивании списка: {e}")
        return []

def extract_domains(lines):
    """Извлекает домены из простого списка доменов."""
    return {line.strip() for line in lines if line.strip()}  # Убираем пробелы и пустые строки

def save_to_file(filename, data):
    """Сохраняет данные в текстовый файл."""
    with open(filename, "w", encoding="utf-8") as file:
        for line in data:
            file.write(line + "\n")
    print(f"Итоговый список сохранён в {filename}")

def process_and_refilter(url1, url2, url3, output_file):
    """Скачивает, обрабатывает списки и сохраняет результат."""
    # Скачиваем списки
    ooni_list = download_list(url1)
    community_list = download_list(url2)
    antifilter_list = download_list(url3)

    # Извлекаем домены из всех списков
    ooni_domains = extract_domains(ooni_list)
    community_domains = extract_domains(community_list)
    antifilter_domains = extract_domains(antifilter_list)

    # Создаем общий список доменов, убирая дубликаты
    all_domains = ooni_domains.union(community_domains).union(antifilter_domains)
    print(f"Объединено {len(all_domains)} уникальных доменов.")

    # Форматируем данные для SwitchyOmega
    formatted_domains = [f"*://*.{domain}/*" for domain in sorted(all_domains)]

    # Добавляем дату и время составления списка
    current_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    
    # Формируем итоговый список с заголовками и окончанием
    final_output = [
        "#BEGIN",
        "",  # Пустая строка
        "[Wildcard]"
    ] + formatted_domains + [
        "#END",
        f"# List compiled: {current_time}"  # Время составления списка в конце
    ]

    # Сохраняем итоговый список
    save_to_file(output_file, final_output)

if __name__ == "__main__":
    process_and_refilter(url_ooni, url_community, url_antifilter, output_file)
