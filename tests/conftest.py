import pytest


@pytest.fixture
def sample_vacancy_data():
    return {
        "name": "Python Developer",
        "url": "https://hh.ru/vacancy/123",
        "salary": {"from": 100000, "to": 150000, "currency": "RUR"},
        "requirement": "Опыт работы с Django.",
    }
