import psycopg2
from psycopg2 import sql
from config import config


class DBManager:
    """
    Класс DBManager для подключения к БД PostgreSQL.
    """

    def __init__(self):
        db_params = config()
        self.conn = psycopg2.connect(**db_params)

    def __del__(self):
        """
        Деструктор для закрытия соединения при удалении объекта.
        """
        if self.conn and not self.conn.closed:
            self.conn.close()

    def get_companies_and_vacancies_count(self):
        """
        Функция для получения списка компаний и количество вакансий в каждой.
        """
        with self.conn.cursor() as cur:
            cur.execute(
                sql.SQL(
                    "SELECT c.company_name, COUNT(v.company_id) AS vacancies_count "
                    "FROM companies c "
                    "LEFT JOIN vacancies v ON c.id = v.company_id "
                    "GROUP BY c.company_name;"
                )
            )
            return cur.fetchall()

    def get_all_vacancies(self):
        """
        Функция для получения списка вакансий с указанием названия компании,
        зарплаты и ссылки на вакансию.
        """
        with self.conn.cursor() as cur:
            cur.execute(
                sql.SQL(
                    "SELECT c.company_name, v.title, v.salary_from, v.salary_to, v.link "
                    "FROM companies c "
                    "JOIN vacancies v ON c.id = v.company_id;"
                )
            )
            return cur.fetchall()

    def get_avg_salary(self):
        """
        Функция для получения средней зарплаты по вакансиям.
        """
        with self.conn.cursor() as cur:
            cur.execute(
                sql.SQL(
                    "SELECT AVG((v.salary_from + v.salary_to) / 2) AS avg_salary "
                    "FROM vacancies v;"
                )
            )
            result = cur.fetchone()
            return result[0] if result else None

    def get_vacancies_with_higher_salary(self):
        """
        Функция для получения списка вакансий, у которых зарплата
        выше средней по вакансиям.
        """
        with self.conn.cursor() as cur:
            cur.execute(
                sql.SQL(
                    "WITH avg_salary AS ("
                    "    SELECT AVG((salary_from + salary_to) / 2) AS avg_salary "
                    "    FROM vacancies"
                    ")"
                    "SELECT c.company_name, v.title, v.salary_from, v.salary_to, v.link "
                    "FROM companies c "
                    "JOIN vacancies v ON c.id = v.company_id, avg_salary "
                    "WHERE (v.salary_from + v.salary_to) / 2 > avg_salary.avg_salary;"
                )
            )
            return cur.fetchall()

    def get_vacancies_with_keyword(self, keyword):
        """
        Функция для получения списка вакансий, в названии которых содержится
        переданное слово.
        """
        with self.conn.cursor() as cur:
            cur.execute(
                sql.SQL(
                    "SELECT c.company_name, v.title, v.salary_from, v.salary_to, v.link "
                    "FROM companies c "
                    "JOIN vacancies v ON c.id = v.company_id "
                    "WHERE v.title ILIKE %s;"
                ),
                [f"%{keyword}%"]
            )
            return cur.fetchall()


# Пример использования класса
"""if __name__ == "__main__":
    db_manager = DBManager()
    print("Companies and vacancies count:")
    print(db_manager.get_companies_and_vacancies_count())
    print("\nAll vacancies:")
    print(db_manager.get_all_vacancies())
    print("\nAverage salary:")
    print(db_manager.get_avg_salary())
    print("\nVacancies with higher salary:")
    print(db_manager.get_vacancies_with_higher_salary())
    print("\nVacancies with keyword 'Python':")
    print(db_manager.get_vacancies_with_keyword("Python"))"""