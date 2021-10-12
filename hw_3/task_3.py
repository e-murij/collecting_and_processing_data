from pymongo import MongoClient

from hw_3.parser_hh import parser_hh


def print_new_vacancy_to_db(mongodb_url, vacancy, link):
    client = MongoClient(mongodb_url)
    db = client['vacancy_database']
    collection_name = f'{vacancy}_collection'
    collection = db[collection_name]
    vacancy_link_db = collection.find({}, {'vacancy_link': 1, '_id': 0})
    vacancy_link_db_list = []
    for obj in vacancy_link_db:
        vacancy_link_db_list.append(obj['vacancy_link'])
    vacancy_date_hh = parser_hh(vacancy, link)
    for obj in vacancy_date_hh:
        if obj['vacancy_link'] not in vacancy_link_db_list:
            collection.insert_one(obj)


if __name__ == "__main__":
    mongodb_url = 'mongodb://localhost:27017/'
    link = 'https://novosibirsk.hh.ru'
    vacancy = 'Python Junior'
    print_new_vacancy_to_db(mongodb_url, vacancy, link)
