import requests
import time
import os
from terminaltables import AsciiTable
from itertools import count
from dotenv import load_dotenv


def predict_rub_salary_hh(vacancy):
    salary = vacancy["salary"]
    if salary:
        if salary['currency'] == 'RUR':
            if salary["from"] and salary["to"]:
                avarage_salary = (salary['from'] + salary['to']) / 2
                return avarage_salary
            elif salary["from"]:
                return salary["from"] * 1.2
            elif salary["to"]:
                return salary["to"] * 0.8
    return


def get_statistics_hh(text):
    statistic = {}
    vacancies_processed = 0
    sum_of_salary = 0
    for page in count(0):
        params = {
            'text': text,
            'area': 1,
            'page': page
        }
        response = requests.get('https://api.hh.ru/vacancies', params=params)
        response.raise_for_status()
        if page >= response.json()["pages"] - 1:
            statistic[text] = {
                "vacancies_found": response.json()['found'],
                "vacancies_processed": vacancies_processed,
                "average_salary": int(sum_of_salary/vacancies_processed)
            }
            return statistic
        for vacancy in response.json()['items']:
            if vacancy['salary']:
                salary = predict_rub_salary_hh(vacancy)
                if salary:
                    sum_of_salary += salary
                    vacancies_processed += 1
        time.sleep(0.5)


def predict_rub_salary_superJob(vacancy):
    if vacancy["payment_from"] and vacancy["payment_to"]:
        avarage_salary = (vacancy['payment_from'] + vacancy['payment_to']) / 2
        return avarage_salary
    elif vacancy["payment_from"]:
        return vacancy["payment_from"] * 1.2
    elif vacancy["payment_to"]:
        return vacancy["payment_to"] * 0.8
    return


def get_statistics_superJob(text):
    statistic = {}
    vacancies_processed = 0
    sum_of_salary = 0
    vacancies_found = None
    for page in count(0):
        headers = {
            'X-Api-App-Id': os.getenv('SECRET_KEY_SUPERJOB')
        }
        params = {
            'keyword': text,
            'town': '4',
            'page': page
        }
        response = requests.get('https://api.superjob.ru/2.0/vacancies/',
                                headers=headers, params=params)
        response.raise_for_status()
        if vacancies_found is None:
            vacancies_found = response.json()['total']
        if not response.json()['more']:
            if vacancies_processed == 0:
                statistic[text] = {
                    "vacancies_found": vacancies_found,
                    "vacancies_processed": vacancies_processed,
                    "average_salary": 0
                }
            else:
                statistic[text] = {
                    "vacancies_found": vacancies_found,
                    "vacancies_processed": vacancies_processed,
                    "average_salary": int(sum_of_salary/vacancies_processed)
                }
            return statistic
        for vacancy in response.json()['objects']:
            salary = predict_rub_salary_superJob(vacancy)
            if salary:
                sum_of_salary += salary
                vacancies_processed += 1
        time.sleep(0.5)


def get_table(statistics, title):
    table = [
        [
            'Язык программирования',
            'Вакансий найдено',
            'Вакансий обработано',
            'Средняя зарплата'
        ]
    ]
    for language in statistics:
        table.append([language,
                      statistics[language]['vacancies_found'],
                      statistics[language]['vacancies_processed'],
                      statistics[language]['average_salary']])
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
    for language in languages:
        statistics_superJob.update(get_statistics_superJob(language))
    get_table(statistics_superJob, "SuperJob Moscow")

    statistics_hh = {}
    for language in languages:
        statistics_hh.update(get_statistics_hh(language))
    get_table(statistics_hh, "HeadHunter Moscow")
