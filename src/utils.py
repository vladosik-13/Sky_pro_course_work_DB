from class_DBManager import DBManager
from hh_class import HeadHunterParser
from json_saver_class import JSONSaver


def collecting_vacancies(user_input):
    """
    Функция для сбора вакансии по запросу от пользователя.
    """
    parser = HeadHunterParser()
    search_query = user_input
    datas = parser.get_vacancies(search_query)
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
