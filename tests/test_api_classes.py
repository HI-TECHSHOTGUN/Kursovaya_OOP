import requests

from src.api_classes import HeadHunterAPI

# Фейк ответ API
FAKE_HH_RESPONSE = {
    'items': [
        {'name': 'Python Developer', 'alternate_url': 'url1', 'salary': {'from': 1000}, 'snippet': {'requirement': 'req1'}},
        {'name': 'Data Scientist', 'alternate_url': 'url2', 'salary': {'from': 1500}, 'snippet': {'requirement': 'req2'}},
    ]
}

def test_get_vacancies_success(mocker):
    """Тест успешного запроса к API."""
    mock_get = mocker.patch('requests.get')
    mock_get.return_value.status_code = 200
    mock_get.return_value.json.return_value = FAKE_HH_RESPONSE

    hh_api = HeadHunterAPI()
    vacancies = hh_api.get_vacancies("Python")

    assert len(vacancies) == 2
    assert vacancies[0]['name'] == 'Python Developer'
    mock_get.assert_called_once_with(
        "https://api.hh.ru/vacancies",
        params={'text': 'Python', 'area': 113, 'per_page': 100, 'only_with_salary': True}
    )

def test_get_vacancies_network_error(mocker):
    """Тест обработки ошибки сети."""
    mocker.patch('requests.get', side_effect=requests.RequestException)

    hh_api = HeadHunterAPI()
    vacancies = hh_api.get_vacancies("Python")
    assert vacancies == []