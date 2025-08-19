import psycopg2
from typing import List, Dict, Any, Tuple


class DBManager:
    """Класс для работы с данными в БД PostgreSQL."""

    def __init__(self, params: dict):
        self.params = params
        self.conn = psycopg2.connect(**self.params)

    def __execute_query(self, query: str, fetch: str = "all") -> Any:
        """Вспомогательный метод для выполнения запросов."""
        with self.conn.cursor() as cur:
            cur.execute(query)
            if fetch == "all":
                return cur.fetchall()
            elif fetch == "one":
                return cur.fetchone()
        return None

    def get_companies_and_vacancies_count(self) -> List[Tuple[str, int]]:
        """Получает список всех компаний и количество вакансий у каждой."""
        query = """
            SELECT c.name, COUNT(v.vacancy_id) AS vacancies_count
            FROM companies c
            LEFT JOIN vacancies v ON c.employer_id = v.employer_id
            GROUP BY c.name
            ORDER BY vacancies_count DESC;
        """
        return self.__execute_query(query)

    def get_all_vacancies(self) -> List[Tuple[str, str, int, str]]:
        """Получает список всех вакансий с указанием названия компании, названия вакансии, зарплаты и ссылки на вакансию."""
        query = """
            SELECT c.name, v.name, v.salary_from, v.url
            FROM vacancies v
            JOIN companies c ON v.employer_id = c.employer_id
            ORDER BY c.name, v.salary_from DESC;
        """
        return self.__execute_query(query)

    def get_avg_salary(self) -> Tuple[float, None]:
        """Получает среднюю зарплату по вакансиям."""
        query = "SELECT AVG(salary_from) FROM vacancies WHERE salary_from IS NOT NULL;"
        result = self.__execute_query(query, fetch="one")
        return result[0] if result else None

    def get_vacancies_with_higher_salary(self) -> List[Dict[str, Any]]:
        """Получает список вакансий, у которых зарплата выше средней."""
        avg_salary = self.get_avg_salary()
        if avg_salary is None:
            return []

        query = f"""
            SELECT name, salary_from, url
            FROM vacancies
            WHERE salary_from > {avg_salary}
            ORDER BY salary_from DESC;
        """
        return self.__execute_query(query)

    def get_vacancies_with_keyword(self, keyword: str) -> List[Tuple[str, int, str]]:
        """Получает список вакансий, в названии которых содержатся переданные слова."""
        query = f"""
            SELECT name, salary_from, url
            FROM vacancies
            WHERE lower(name) LIKE '%{keyword.lower()}%'
            ORDER BY salary_from DESC;
        """
        return self.__execute_query(query)

    def close_connection(self) -> None:
        """Закрывает соединение с БД."""
        self.conn.close()