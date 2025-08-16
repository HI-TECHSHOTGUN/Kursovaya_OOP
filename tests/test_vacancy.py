from src.vacancy import Vacancy


def test_vacancy_initialization(sample_vacancy_data):
    """Тест инициализации объекта Vacancy."""
    vacancy = Vacancy(**sample_vacancy_data)
    assert vacancy.name == "Python Developer"
    assert vacancy.url == "https://hh.ru/vacancy/123"
    assert vacancy.salary_from == 100000
    assert vacancy.salary_to == 150000
    assert vacancy.currency == "RUR"
    assert "Django" in vacancy.requirement


def test_vacancy_salary_validation():
    """Тест валидации зарплаты (None, только 'from', только 'to')."""
    v1 = Vacancy("Test1", "url1", None, "req1")
    assert v1.salary_from == 0 and v1.salary_to == 0
    assert v1.salary_display == "Зарплата не указана"

    v2 = Vacancy("Test2", "url2", {"from": 50000, "currency": "USD"}, "req2")
    assert v2.salary_from == 50000 and v2.salary_to == 0
    assert v2.salary_display == "от 50000 USD"


def test_vacancy_comparison():
    """Тест сравнения вакансий по зарплате."""
    v_low = Vacancy("Junior", "url_j", {"from": 50000}, "req_j")
    v_high = Vacancy("Senior", "url_s", {"from": 200000}, "req_s")
    v_equal = Vacancy("Middle", "url_m", {"from": 200000}, "req_m")

    assert v_high > v_low
    assert v_low < v_high
    assert v_high == v_equal
    assert not (v_low == v_high)


def test_vacancy_str_representation(sample_vacancy_data):
    """Тест строкового представления объекта."""
    vacancy = Vacancy(**sample_vacancy_data)
    vacancy_str = str(vacancy)
    assert "Python Developer" in vacancy_str
    assert "от 100000 до 150000 RUR" in vacancy_str
