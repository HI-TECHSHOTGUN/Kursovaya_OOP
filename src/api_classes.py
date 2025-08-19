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


class HeadHunterAPI:
    """Класс для работы с API hh.ru."""
    __URL = "https://api.hh.ru/"

    def get_employers(self, employer_ids: List[str]) -> List[Dict[str, Any]]:
        """Получает данные о работодателях по их ID."""
        employers_data = []
        for employer_id in employer_ids:
            try:
                response = requests.get(f"{self.__URL}employers/{employer_id}")
                response.raise_for_status()
                employers_data.append(response.json())
            except requests.RequestException as e:
                print(f"Ошибка при запросе данных о компании {employer_id}: {e}")
        return employers_data

    def get_vacancies_by_employer(self, employer_id: str) -> List[Dict[str, Any]]:
        """Получает вакансии для конкретного работодателя."""
        params = {
            'employer_id': employer_id,
            'area': 113,  # Россия
            'per_page': 100,
        }
        try:
            response = requests.get(f"{self.__URL}vacancies", params=params)
            response.raise_for_status()
            return response.json()['items']
        except requests.RequestException as e:
            print(f"Ошибка при запросе вакансий для компании {employer_id}: {e}")
            return []
