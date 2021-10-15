from pymongo import MongoClient

from hw_3.parser_hh import parser_hh


def print_vacancy_to_db(vacancy, vacancy_date, mongodb_url):
    client = MongoClient(mongodb_url)
    db = client['vacancy_database']
    collection_name = f'{vacancy}_collection'
    collection = db[collection_name]
    collection.insert_many(vacancy_date)


if __name__ == "__main__":
    link = 'https://novosibirsk.hh.ru'
    vacancy = 'Python'
    mongodb_url = 'mongodb://localhost:27017/'
    vacancy_date = parser_hh(vacancy, link)
    print_vacancy_to_db(vacancy, vacancy_date, mongodb_url)
