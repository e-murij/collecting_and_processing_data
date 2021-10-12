from pymongo import MongoClient


def print_vacancy_salary_gt(salary, mongodb_url, vacancy):
    client = MongoClient(mongodb_url)
    db = client['vacancy_database']
    collection_name = f'{vacancy}_collection'
    collection = db[collection_name]
    objects = collection.find({'$or': [{'salary_max': {'$gt': salary}}, {'salary_min': {'$gt': salary}}]}, {'_id' : 0})
    for obj in objects:
        print(obj)


if __name__ == "__main__":
    mongodb_url = 'mongodb://localhost:27017/'
    vacancy = 'Python Junior'
    salary = 49000
    print_vacancy_salary_gt(salary, mongodb_url, vacancy)
