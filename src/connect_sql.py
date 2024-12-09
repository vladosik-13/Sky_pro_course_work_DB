import psycopg2
from psycopg2 import sql
from config import config

def connection_to_data(vacancies_list):
    """
    Создание базы данных для хранения и полученных данных о
    работодателях и вакансиях.
    """
    db_params = config()
    try:
        with psycopg2.connect(**db_params) as conn:
            with conn.cursor() as cur:
                cur.execute("DROP TABLE IF EXISTS vacancies")
                cur.execute("DROP TABLE IF EXISTS companies")
                cur.execute(
                    sql.SQL("CREATE TABLE companies ("
                            "id SERIAL PRIMARY KEY,"
                            "company_name VARCHAR(100))"
                    )
                )

                cur.execute(
                    sql.SQL("CREATE TABLE vacancies ("
                            "company_id INT REFERENCES companies(id),"
                            "title VARCHAR(100),"
                            "city VARCHAR(50),"
                            "salary_from INT,"
                            "salary_to INT,"
                            "link VARCHAR(100))"
                    )
                )

                id_company = 0
                for company_dict in vacancies_list:
                    if not company_dict:
                        continue
                    company_name = next(iter(company_dict))
                    vacancies = company_dict.get(company_name, [])
                    id_company += 1
                    cur.execute(
                        sql.SQL("INSERT INTO companies (company_name) VALUES (%s) RETURNING id"),
                        (company_name,)
                    )
                    company_id = cur.fetchone()[0]

                    for vacancy in vacancies:
                        title = vacancy.get("title", "")
                        city = vacancy.get("city", "")
                        salary_from = vacancy.get("salary_from", None)
                        salary_to = vacancy.get("salary_to", None)
                        link = vacancy.get("link", "")

                        cur.execute(
                            sql.SQL("INSERT INTO vacancies (company_id, title, city, salary_from, salary_to, link)"
                                    " VALUES (%s, %s, %s, %s, %s, %s) RETURNING *"),
                            (company_id, title, city, salary_from, salary_to, link)
                        )

                conn.commit()

    except Exception as e:
        print(f"An error occurred: {e}")
