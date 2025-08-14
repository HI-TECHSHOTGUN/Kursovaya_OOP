import json
import os
from abc import ABC, abstractmethod

from src.vacancy import Vacancy


class Saver(ABC):
    """Абстрактный класс для работы с файлами"""

    @abstractmethod
    def add_vacancy(self, vacancy):
        pass

    @abstractmethod
    def get_vacancies_by_criteria(self, keyword):
        pass

    @abstractmethod
    def delete_vacancy(self, vacancy):
        pass


class JSONSaver(Saver):
    def __init__(self, filename="data/vacancies.json"):
        self.filename = filename
        os.makedirs(os.path.dirname(filename), exist_ok=True)
        with open(self.filename, "w") as f:
            json.dump([], f)

    def _read_file(self):
        try:
            with open(self.filename, "r", encoding="utf-8") as f:
                data = json.load(f)
            return data
        except (FileNotFoundError, json.JSONDecodeError):
            return []

    def _write_file(self, data):
        with open(self.filename, "w", encoding="utf-8") as f:
            json.dump(data, f, ensure_ascii=False, indent=4)

    def add_vacancy(self, vacancy):
        data = self._read_file()
        data.append(vacancy.__dict__)
        self._write_file(data)

    def add_vacancies(self, vacancies):
        data = self._read_file()
        data.extend([v.__dict__ for v in vacancies])
        self._write_file(data)

    def get_vacancies_by_criteria(self, keyword):
        data = self._read_file()
        filtered_vacancies = []
        for v_dict in data:
            if keyword.lower() in v_dict.get("requirement", "").lower():
                filtered_vacancies.append(
                    Vacancy(
                        name=v_dict["name"],
                        url=v_dict["url"],
                        salary={
                            "from": v_dict["salary_from"],
                            "to": v_dict["salary_to"],
                            "currency": v_dict["currency"],
                        },
                        requirement=v_dict["requirement"],
                    )
                )
        return filtered_vacancies

    def delete_vacancy(self, vacancy: Vacancy):
        data = self._read_file()
        new_data = [v for v in data if v.get("url") != vacancy.url]
        self._write_file(new_data)
