from connect_sql import connection_to_data
from utils import (collecting_vacancies, creating_dictionary_list, get_print,
                   saver_json)

if __name__ == "__main__":
    list_of_company = [
        "IT-специалист",
        "Frontend developer (офис)",
        "Frontend-разработчик",
        "Python-разработчик (Django)",
        "Project manager IT (Middle)",
        "Программист Python",
        "Начинающий IT специалист",
        "Системный администратор",
        "Junior IT специалист / системный аналитик /" "программист Трудоустройство",
        "Норникель Спутник",
    ]  # Список компаний

    vacancies_list = []
    for search_query in list_of_company:
        coll_vacancies = collecting_vacancies(search_query)
        vacancies_list_item = {search_query: creating_dictionary_list(coll_vacancies)}
        vacancies_list.append(vacancies_list_item)

    saver_json(vacancies_list)
    connection_to_data(vacancies_list)

    while True:
        input_user = (
            input(
                """
Приветствуем вас! Наше приложение поможет вам получить данные о компаниях и вакансиях с сайта hh.ru.
Выберите пункт который интересует.
1. Получить список компаний и количество вакансий у каждой.
2. Получить список вакансий с указанием названия компании, вакансии, зарплаты и ссылки на данную вакансию.
3. Получить вывод средней зарплаты по выбранным вакансиям.
4. Получить список вакансий, у которых зарплата выше средней по выбранным вакансиям.
5. Получить список вакансий, в названии которых содержатся переданные в метод слова.

Наберите стоп или stop для окончания работы программы.
"""
            )
            .lower()
            .strip()
        )
        if get_print(input_user) == "стоп":
            break
