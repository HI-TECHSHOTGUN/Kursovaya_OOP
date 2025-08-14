class Vacancy:
    """Класс для представления вакансии"""

    def __init__(self, name, url, salary, requirement):
        self.name = name
        self.url = url
        self.salary_from, self.salary_to, self.currency = self._validate_salary(salary)
        self.requirement = requirement if requirement else "Нет требований"

    def _validate_salary(self, salary):
        if not salary:
            return 0, 0, ""

        salary_from = salary.get("from", 0) or 0
        salary_to = salary.get("to", 0) or 0
        currency = salary.get("currency", "")

        return salary_from, salary_to, currency

    @property
    def salary_display(self):
        if self.salary_from == 0 and self.salary_to == 0:
            return "Зарплата не указана"
        elif self.salary_from != 0 and self.salary_to != 0:
            return f"от {self.salary_from} до {self.salary_to} {self.currency}"
        elif self.salary_from != 0:
            return f"от {self.salary_from} {self.currency}"
        else:
            return f"до {self.salary_to} {self.currency}"

    def __str__(self):
        return (
            f"Название: {self.name}\n"
            f"Ссылка: {self.url}\n"
            f"Зарплата: {self.salary_display}\n"
            f"Требования: {self.requirement}\n"
        )

    """Методы для сравнения вакансий между собой"""

    def __eq__(self, other):
        if not isinstance(other, Vacancy):
            return NotImplemented
        return self.salary_from == other.salary_from

    def __lt__(self, other):
        if not isinstance(other, Vacancy):
            return NotImplemented
        return self.salary_from < other.salary_from

    def __le__(self, other):
        if not isinstance(other, Vacancy):
            return NotImplemented
        return self.salary_from <= other.salary_from

    def __gt__(self, other):
        if not isinstance(other, Vacancy):
            return NotImplemented
        return self.salary_from > other.salary_from

    def __ge__(self, other):
        if not isinstance(other, Vacancy):
            return NotImplemented
        return self.salary_from >= other.salary_from

    @classmethod
    def cast_to_object_list(cls, vacancies_json):
        return [
            cls(v["name"], v["alternate_url"], v["salary"], v.get("snippet", {}).get("requirement"))
            for v in vacancies_json
        ]
