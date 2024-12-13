from abc import ABC, abstractmethod

import requests


class Parser(ABC):
    @abstractmethod
    def get_vacancies(self, keyword):
        pass

    @abstractmethod
    def get_employer(self, employer_id):
        pass

    @abstractmethod
    def get_employer_vacancies(self, employer_id):
        pass


class HeadHunterParser(Parser):
    """
    Класс для работы с API HeadHunter
    Класс Parser(ABC) является родительским классом.
    """

    def get_vacancies(self, keyword):
        url = "https://api.hh.ru/vacancies"
        params = {"text": keyword, "page": 0, "per_page": 100}
        response = requests.get(url, params=params)
        response.raise_for_status()  # Проверка на ошибки HTTP
        return response.json()

    def get_employer(self, employer_id):
        url = f"https://api.hh.ru/employers/{employer_id}"
        response = requests.get(url)
        response.raise_for_status()  # Проверка на ошибки HTTP
        return response.json()

    def get_employer_vacancies(self, employer_id):
        url = f"https://api.hh.ru/vacancies"
        params = {"employer_id": employer_id, "page": 0, "per_page": 100}
        response = requests.get(url, params=params)
        response.raise_for_status()  # Проверка на ошибки HTTP
        return response.json()