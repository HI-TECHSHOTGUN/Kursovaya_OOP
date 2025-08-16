from abc import ABC, abstractmethod
from http.client import responses
from typing import List, Dict, Any

import requests


class API(ABC):
    """Абстрактный класс для работы с API"""
    @abstractmethod
    def _connect(self) -> None:
        """Абстрактный метод для проверки подключения к API."""
        pass

    @abstractmethod
    def get_vacancies(self, search_query):
        """Абстрактный метод для получения вакансий."""
        pass


class HeadHunterAPI(API):
    """Класс для работы с HH при помощи API"""

    __URL = "https://api.hh.ru/vacancies"

    def __init__(self) -> None:
        """Инициализирует объект и проверяет соединение с API."""
        self._connect()

    def _connect(self) -> None:
        """Приватный метод для проверки доступности API."""
        try:
            response = requests.get(self.__URL, timeout=5)
            response.raise_for_status()
        except requests.RequestException as e:
            raise ConnectionError(f"Не удалось подключиться к API hh.ru: {e}")

    def get_vacancies(self, search_query: str) -> List[Dict[str, Any]]:
        """Получает список вакансий с hh.ru по заданному поисковому запросу."""
        params = {"text": search_query, "area": 113, "per_page": 100, "only_with_salary": True}  # Поиск по России

        try:
            response = requests.get(self.__URL, params=params)
            response.raise_for_status()
            return response.json()["items"]
        except requests.RequestException as e:
            print(f"Ошибка API запроса {e}")
            return []
