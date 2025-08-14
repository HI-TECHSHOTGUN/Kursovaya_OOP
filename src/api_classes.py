from abc import ABC, abstractmethod
from http.client import responses

import requests


class API(ABC):
    """Абстрактный класс для работы с API"""

    @abstractmethod
    def get_vacancies(self, search_query):
        pass


class HeadHunterAPI(API):
    """Класс для работы с HH при помощи API"""

    URL = "https://api.hh.ru/vacancies"

    def get_vacancies(self, search_query):
        params = {"text": search_query, "area": 113, "per_page": 100, "only_with_salary": True}  # Поиск по России

        try:
            response = requests.get(self.URL, params=params)
            response.raise_for_status()
            return response.json()["items"]
        except requests.RequestException as e:
            print(f"Ошибка API запроса {e}")
            return []
