# Programming vacancies compare

Script for geting programmer vacancies statics 

## Example

```
$python3 main.py

+SuperJob Moscow--------+------------------+---------------------+------------------+
| Язык программирования | Вакансий найдено | Вакансий обработано | Средняя зарплата |
+-----------------------+------------------+---------------------+------------------+
| python                | 22               | 5                   | 167000           |
| c                     | 555              | 505                 | 137787           |
| c#                    | 3                | 0                   | 0                |
| c++                   | 4                | 0                   | 0                |
| java                  | 4                | 0                   | 0                |
| javascript            | 8                | 0                   | 0                |
| ruby                  | 0                | 0                   | 0                |
| go                    | 3                | 0                   | 0                |
| php                   | 7                | 0                   | 0                |
+-----------------------+------------------+---------------------+------------------+
+HeadHunter Moscow------+------------------+---------------------+------------------+
| Язык программирования | Вакансий найдено | Вакансий обработано | Средняя зарплата |
+-----------------------+------------------+---------------------+------------------+
| python                | 5039             | 438                 | 206099           |
| c#                    | 905              | 205                 | 219554           |
| c++                   | 1299             | 325                 | 218313           |
| java                  | 2033             | 241                 | 231565           |
| javascript            | 2052             | 549                 | 197051           |
| ruby                  | 102              | 30                  | 267586           |
| go                    | 1281             | 307                 | 189349           |
| php                   | 988              | 347                 | 199006           |
+-----------------------+------------------+---------------------+------------------+
```

### How to install

Python3 should be already installed. Then use pip (or pip3, if there is a conflict with Python2) to install dependencies:
```
pip install -r requirements.txt
```

You should create `.env` file in root directory and write in it this key:
- SECRET_KEY_SUPERJOB=your_key

If you don't have SuperJob secret key you should register on the site [SuperJob](https://www.superjob.ru/) and create an app in [API SuperJob](https://api.superjob.ru/)

### Project Goals

The code is written for educational purposes on online-course for web-developers [dvmn.org](https://dvmn.org/).