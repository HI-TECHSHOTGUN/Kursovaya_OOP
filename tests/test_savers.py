import json
import pytest
from src.vacancy import Vacancy
from src.savers import JSONSaver


@pytest.fixture
def sample_vacancies():
    """Фикстура с примерами вакансий для тестов."""
    return [
        Vacancy("Python Dev", "url1", {"from": 100}, "reqs for python dev"),
        Vacancy("Java Dev", "url2", {"from": 120}, "reqs for java dev"),
        Vacancy("JS Dev", "url3", {"from": 110}, "reqs for js dev"),
    ]


@pytest.fixture
def json_saver(tmp_path):
    """Фикстура, создающая экземпляр JSONSaver во временной директории."""
    file_path = tmp_path / "test_vacancies.json"
    return JSONSaver(filename=str(file_path))


def test_add_and_read_vacancies(json_saver, sample_vacancies):
    """Тест добавления вакансий и чтения файла."""
    json_saver.add_vacancies(sample_vacancies)

    with open(json_saver.filename, 'r', encoding='utf-8') as f:
        data = json.load(f)

    assert len(data) == 3
    assert data[0]['name'] == "Python Dev"
    assert data[1]['salary_from'] == 120


def test_delete_vacancy(json_saver, sample_vacancies):
    """Тест удаления вакансии."""
    json_saver.add_vacancies(sample_vacancies)

    vacancy_to_delete = sample_vacancies[1]
    json_saver.delete_vacancy(vacancy_to_delete)

    with open(json_saver.filename, 'r', encoding='utf-8') as f:
        data = json.load(f)

    assert len(data) == 2
    assert data[0]['url'] == 'url1'
    assert data[1]['url'] == 'url3'


def test_get_vacancies_by_criteria(json_saver, sample_vacancies):
    """Тест получения вакансий по ключевому слову в требованиях."""
    json_saver.add_vacancies(sample_vacancies)

    filtered = json_saver.get_vacancies_by_criteria("java")

    assert len(filtered) == 1
    assert isinstance(filtered[0], Vacancy)
    assert filtered[0].name == "Java Dev"