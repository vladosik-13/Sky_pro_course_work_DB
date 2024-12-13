import requests

from class_DBManager import DBManager
from hh_class import HeadHunterParser
from json_saver_class import JSONSaver


def collecting_vacancies(user_input):
    """
    Функция для сбора вакансии по запросу от пользователя.
    """
    parser = HeadHunterParser()
    search_query = user_input
    try:
        datas = parser.get_vacancies(search_query)
    except requests.exceptions.HTTPError as http_err:
        print(f"HTTP error occurred: {http_err}")
        return []
    except Exception as err:
        print(f"Other error occurred: {err}")
        return []
    return datas


def creating_dictionary_list(other):
    """
    Функция для создания списка словарей по атрибутам.
    """
    vacancies_list = []
    for item in other["items"]:
        salary_from = item["salary"].get("from") if item["salary"] else None
        salary_to = item["salary"].get("to") if item["salary"] else None
        vacancies_list.append(
            {
                "id": item["id"],
                "title": item["name"],
                "city": item["area"]["name"],
                "salary_from": salary_from,
                "salary_to": salary_to,
                "link": item["url"],
            }
        )
    return vacancies_list


def get_employer_info(parser, employer_id):
    """
    Функция для получения информации о работодателе.
    """
    try:
        employer_info = parser.get_employer(employer_id)
    except requests.exceptions.HTTPError as http_err:
        print(f"HTTP error occurred while getting employer info for ID {employer_id}: {http_err}")
        return None
    except Exception as err:
        print(f"Other error occurred while getting employer info for ID {employer_id}: {err}")
        return None
    return employer_info


def get_employer_vacancies(parser, employer_id):
    """
    Функция для получения вакансий работодателя.
    """
    try:
        employer_vacancies = parser.get_employer_vacancies(employer_id)
    except requests.exceptions.HTTPError as http_err:
        print(f"HTTP error occurred while getting vacancies for employer ID {employer_id}: {http_err}")
        return []
    except Exception as err:
        print(f"Other error occurred while getting vacancies for employer ID {employer_id}: {err}")
        return []
    return employer_vacancies


def get_print(input_user):
    """
    Функция для вывода результата по запросу.
    """
    db = DBManager()

    if input_user == "1":
        print(db.get_companies_and_vacancies_count())
    elif input_user == "2":
        print(db.get_all_vacancies())
    elif input_user == "3":
        print(db.get_avg_salary())
    elif input_user == "4":
        print(db.get_vacancies_with_higher_salary())
    elif input_user == "5":
        input_keyword = input(
            "Введите ключевое слово названия компании или её вакансии\n"
        )
        print(db.get_vacancies_with_keyword(input_keyword))
    elif input_user == "стоп" or input_user == "stop":
        print("Работа программы завершена. Желаем успеха в поиске новой вакансии!")
        return "стоп"
    else:
        print(
            "Неправильный ввод номера интересующего вас пункта. Выберите пункт интересующий вас."
        )


def saver_json(other):
    """
    Функция для записи списка в JSON
    """
    saver = JSONSaver()
    saver.insert(other)


def collecting_employers_vacancies(employer_ids):
    parser = HeadHunterParser()
    vacancies_list = []
    for employer_id in employer_ids:
        employer_info = get_employer_info(parser, employer_id)
        if employer_info and "name" in employer_info:
            employer_name = employer_info["name"]
            employer_vacancies = get_employer_vacancies(parser, employer_id)
            vacancies = creating_dictionary_list(employer_vacancies)
            vacancies_list.append({employer_name: vacancies})
        else:
            print(f"Не удалось получить информацию о работодателе с ID {employer_id}.")
    return vacancies_list