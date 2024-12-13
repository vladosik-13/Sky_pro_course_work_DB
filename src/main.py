from connect_sql import connection_to_data
from utils import collecting_employers_vacancies, saver_json, get_print

if __name__ == "__main__":
    list_of_employers = [
        "1740",  # Skyeng
        "1",     # Яндекс
        "3529",  # Ozon
        "3522",  # Сбербанк
        "1879467",  # Норникель Спутник
        # Добавьте остальные работодатели по их ID
    ]  # Список работодателей по их ID

    vacancies_list = collecting_employers_vacancies(list_of_employers)

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
