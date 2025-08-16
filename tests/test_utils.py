from src.utils import user_interaction
from src.vacancy import Vacancy


def test_user_interaction_full_cycle(mocker, capsys):
    """Тест полного цикла взаимодействия с пользователем:"""
    fake_api_response = [
        {
            "name": "Python Developer",
            "alternate_url": "url1",
            "salary": {"from": 200000, "currency": "RUR"},
            "snippet": {"requirement": "Требования: Python, Django"}
        },
        {
            "name": "Junior Python Developer",
            "alternate_url": "url2",
            "salary": {"from": 100000, "currency": "RUR"},
            "snippet": {"requirement": "Требования: Python, Flask"}
        }
    ]
    mocker.patch('src.api_classes.HeadHunterAPI.get_vacancies', return_value=fake_api_response)

    user_inputs = [
        "Python",   # Поисковый запрос
        "1",        # Выбор меню "топ N"
        "1",        # Ввод N = 1
        "2",        # Выбор меню "фильтрация"
        "Django",   # Ключевое слово для фильтрации
        "3"         # Выбор меню "выход"
    ]
    mocker.patch('builtins.input', side_effect=user_inputs)

    filtered_vacancy = Vacancy(
        name=fake_api_response[0]['name'],
        url=fake_api_response[0]['alternate_url'],
        salary=fake_api_response[0]['salary'],
        requirement=fake_api_response[0]['snippet']['requirement']
    )

    mocker.patch('src.savers.JSONSaver.add_vacancies')
    mocker.patch('src.savers.JSONSaver.get_vacancies_by_criteria', return_value=[filtered_vacancy])

    user_interaction()

    captured = capsys.readouterr()
    output = captured.out

    assert "Найдено и сохранено 2 вакансий." in output
    assert "--- Вакансия #1 ---" in output
    assert "Название: Python Developer" in output
    assert "Junior Python Developer" not in output.split("--- Вакансия #1 ---")[1]
    assert "Найдено 1 вакансий с ключевым словом 'Django'" in output
    assert "Требования: Python, Django" in output
    assert "Завершение работы." in output