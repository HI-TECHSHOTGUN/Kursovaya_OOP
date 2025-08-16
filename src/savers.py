import json
import os
from abc import ABC, abstractmethod
from typing import List, Any, Dict

from src.vacancy import Vacancy


class Saver(ABC):
    """Класс для работы с JSON"""
    @abstractmethod
    def add_vacancy(self, vacancy: Vacancy) -> None:
        """Метод для добавления вакансии в файл"""
        pass

    @abstractmethod
    def get_vacancies_by_criteria(self, keyword: str) -> List[Vacancy]:
        """Метод для возвращения списка вакансий"""
        pass

    @abstractmethod
    def delete_vacancy(self, vacancy: Vacancy) -> None:
        """Метод для удаления вакансии"""
        pass


class JSONSaver(Saver):
    """Класс для сохранения информации о вакансиях в JSON-файл."""
    def __init__(self, filename: str = "data/vacancies.json") -> None:
        """Инициализирует JSONSaver, создает директорию и очищает файл."""
        self.__filename = filename
        os.makedirs(os.path.dirname(self.__filename), exist_ok=True)
        with open(self.__filename, 'w', encoding='utf-8') as f:
            json.dump([], f)

    def _read_file(self) -> List[Dict[str, Any]]:
        """Читает данные из файла. Возвращает пустой список, если файл пуст или не существует."""
        try:
            with open(self.__filename, 'r', encoding='utf-8') as f:
                return json.load(f)
        except (FileNotFoundError, json.JSONDecodeError):
            return []

    def _write_file(self, data: List[Dict[str, Any]]) -> None:
        """Записывает данные в файл."""
        with open(self.__filename, 'w', encoding='utf-8') as f:
            json.dump(data, f, ensure_ascii=False, indent=4)

    def add_vacancy(self, vacancy: Vacancy) -> None:
        """Добавляет одну вакансию в файл."""
        data = self._read_file()
        data.append(vacancy.to_dict())
        self._write_file(data)

    def add_vacancies(self, vacancies: List[Vacancy]) -> None:
        """Добавляет список вакансий в файл."""
        data = self._read_file()
        data.extend([v.to_dict() for v in vacancies])
        self._write_file(data)

    def get_vacancies_by_criteria(self, keyword: str) -> List[Vacancy]:
        """Возвращает список вакансий, у которых в требовании есть ключевое слово."""
        data = self._read_file()
        filtered_vacancies = []
        for v_dict in data:
            if keyword.lower() in v_dict.get('requirement', '').lower():
                filtered_vacancies.append(Vacancy(
                    name=v_dict['name'],
                    url=v_dict['url'],
                    salary={'from': v_dict['salary_from'], 'to': v_dict['salary_to'], 'currency': v_dict['currency']},
                    requirement=v_dict['requirement']
                ))
        return filtered_vacancies

    def delete_vacancy(self, vacancy: Vacancy) -> None:
        """Удаляет вакансию из файла по совпадению URL."""
        data = self._read_file()
        new_data = [v for v in data if v.get('url') != vacancy.url]
        self._write_file(new_data)
