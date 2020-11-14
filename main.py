import csv
from urllib.parse import urlencode

import requests


def main():
    # Создание URL
    LIMIT = 5000 # Как вариант - загружать количество данных по запросу и делать пагинацию
    params = {
        "orientation": 3,  # Техническая организация
        "page": 1,  # Начинать с первой страницы
        "perPage": LIMIT,  # Загружать не больше лимита
        "region": 42,  # Московская область
        "institution_type": 188,  # Организации доп образования
        "status": 1  # Организация функционирует
    }
    request_url = f"http://dop.edu.ru/organization/list?{urlencode(params)}"

    # Получение данных и обработка ошибок
    resp = requests.get(request_url)
    resp.raise_for_status()
    data = resp.json()
    if not data['success']:
        print("Не получилось запросить список")
        exit(-1)

    # Запись организаций в CSV файл
    organizations = data['data']['list']
    with open("results.csv", "w", newline="") as f:
        fieldnames = ['id', 'name', 'full_name', 'site_url']
        csv_writer = csv.DictWriter(f, fieldnames=fieldnames)

        csv_writer.writeheader()
        for organization in organizations:
            csv_writer.writerow({field: organization[field] for field in fieldnames})


if __name__ == '__main__':
    main()
