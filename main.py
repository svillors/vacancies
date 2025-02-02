import requests
import time
import os
from terminaltables import AsciiTable
from itertools import count
from dotenv import load_dotenv


def predict_salary(salary_from, salary_to):
    if salary_from and salary_to:
        avarage_salary = (salary_from + salary_to) / 2
        return avarage_salary
    elif salary_from:
        return salary_from * 1.2
    elif salary_to:
        return salary_to * 0.8
    return


def predict_rub_salary_hh(vacancy):
    salary = vacancy["salary"]
    if salary:
        if salary['currency'] == 'RUR':
            return predict_salary(salary["from"], salary['to'])
    return


def get_statistics_hh(text):
    statistic = {}
    vacancies_processed = 0
    sum_of_salary = 0
    moscow_id = 1
    for page in count(0):
        params = {
            'text': text,
            'area': moscow_id,
            'page': page
        }
        response = requests.get('https://api.hh.ru/vacancies', params=params)
        response.raise_for_status()
        vacancies = response.json()
        if page >= vacancies["pages"] - 1:
            break
        for vacancy in vacancies['items']:
            if vacancy['salary']:
                salary = predict_rub_salary_hh(vacancy)
                if salary:
                    sum_of_salary += salary
                    vacancies_processed += 1
        time.sleep(0.5)

    average_salary = (
        int(sum_of_salary/vacancies_processed)
        if vacancies_processed
        else 0
    )

    statistic[text] = {
        "vacancies_found": vacancies['found'],
        "vacancies_processed": vacancies_processed,
        "average_salary": average_salary
    }
    return statistic


def predict_rub_salary_superJob(vacancy):
    return predict_salary(vacancy["payment_from"], vacancy["payment_to"])


def get_statistics_superJob(text, secret_key):
    statistic = {}
    vacancies_processed = 0
    sum_of_salary = 0
    vacancies_found = None
    for page in count(0):
        headers = {
            'X-Api-App-Id': secret_key
        }
        params = {
            'keyword': text,
            'town': 'Moscow',
            'page': page
        }
        response = requests.get('https://api.superjob.ru/2.0/vacancies/',
                                headers=headers, params=params)
        response.raise_for_status()
        vacancies = response.json()
        if not vacancies_found:
            vacancies_found = vacancies['total']
        if not vacancies['more']:
            break
        for vacancy in vacancies['objects']:
            salary = predict_rub_salary_superJob(vacancy)
            if salary:
                sum_of_salary += salary
                vacancies_processed += 1
        time.sleep(0.5)

    average_salary = (
        int(sum_of_salary/vacancies_processed)
        if vacancies_processed
        else 0
    )

    statistic[text] = {
        "vacancies_found": vacancies_found,
        "vacancies_processed": vacancies_processed,
        "average_salary": average_salary
    }
    return statistic


def get_table(statistics, title):
    table = [
        [
            'Язык программирования',
            'Вакансий найдено',
            'Вакансий обработано',
            'Средняя зарплата'
        ]
    ]
    for language, language_statistic in statistics.items():
        table.append([language,
                      language_statistic['vacancies_found'],
                      language_statistic['vacancies_processed'],
                      language_statistic['average_salary']])
    table = AsciiTable(table)
    table.title = title
    print(table.table)


if __name__ == "__main__":
    load_dotenv()
    languages = [
        'python',
        'c#',
        'c++',
        'java',
        'javascript',
        'ruby',
        'go',
        'php'
    ]
    statistics_superJob = {}
    secret_key = os.getenv('SECRET_KEY_SUPERJOB')
    for language in languages:
        statistics_superJob.update(get_statistics_superJob(language,
                                                           secret_key))
    get_table(statistics_superJob, "SuperJob Moscow")

    statistics_hh = {}
    for language in languages:
        statistics_hh.update(get_statistics_hh(language))
    get_table(statistics_hh, "HeadHunter Moscow")
