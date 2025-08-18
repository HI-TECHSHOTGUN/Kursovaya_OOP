import functools
from typing import Dict, Any, Tuple, List

@functools.total_ordering
class Vacancy:
    """Класс для представления вакансии."""
    __slots__ = ('name', 'url', 'salary_from', 'salary_to', 'currency', 'requirement')

    def __init__(self, name: str, url: str, salary: Dict[str, Any], requirement: str) -> None:
        """Инициализирует объект Vacancy."""
        self.name = name
        self.url = url
        self.salary_from, self.salary_to, self.currency = self.__validate_salary(salary)
        self.requirement = requirement if requirement else "Нет требований"

    def __validate_salary(self, salary: Dict[str, Any]) -> Tuple[int, int, str]:
        """Приватный метод для валидации данных о зарплате. Возвращает кортеж (зарплата от, зарплата до, валюта)."""
        if not salary:
            return 0, 0, ""

        salary_from = salary.get('from', 0) or 0
        salary_to = salary.get('to', 0) or 0
        currency = salary.get('currency', "")

        return int(salary_from), int(salary_to), currency

    @property
    def salary_display(self) -> str:
        """Возвращает строковое представление зарплаты для вывода."""
        if self.salary_from == 0 and self.salary_to == 0:
            return "Зарплата не указана"
        elif self.salary_from != 0 and self.salary_to != 0:
            return f"от {self.salary_from} до {self.salary_to} {self.currency}"
        elif self.salary_from != 0:
            return f"от {self.salary_from} {self.currency}"
        else:
            return f"до {self.salary_to} {self.currency}"

    def __str__(self) -> str:
        """Возвращает строковое представление"""
        return (f"Название: {self.name}\n"
                f"Ссылка: {self.url}\n"
                f"Зарплата: {self.salary_display}\n"
                f"Требования: {self.requirement}\n")

    def to_dict(self) -> Dict[str, Any]:
        """Возвращает словарное представление объекта Vacancy."""
        return {
            'name': self.name,
            'url': self.url,
            'salary_from': self.salary_from,
            'salary_to': self.salary_to,
            'currency': self.currency,
            'requirement': self.requirement
        }

    def __eq__(self, other: Any) -> bool:
        """Сравнение на равенство (==) по начальной зарплате."""
        if not isinstance(other, Vacancy):
            return NotImplemented
        return self.salary_from == other.salary_from

    def __lt__(self, other: Any) -> bool:
        """Сравнение "меньше чем" (<) по начальной зарплате."""
        if not isinstance(other, Vacancy):
            return NotImplemented
        return self.salary_from < other.salary_from

    @classmethod
    def cast_to_object_list(cls, vacancies_json: List[Dict[str, Any]]) -> List['Vacancy']:
        """Преобразует список JSON-объектов в список объектов Vacancy."""
        return [cls(v['name'], v['alternate_url'], v['salary'], v.get('snippet', {}).get('requirement'))
                for v in vacancies_json]