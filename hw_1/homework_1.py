import requests
import json

# Посмотреть документацию к API GitHub, разобраться как вывести
# список репозиториев для конкретного пользователя, сохранить JSON-вывод в файле *.json.
url = 'https://api.github.com'
user = 'e-murij'
req = requests.get(f'{url}/users/{user}/repos')
result = {}
for i in req.json():
    result[i["name"]] = i["html_url"]

with open('task_1.json', 'w') as f:
    json.dump(result, f)

# Изучить список открытых API. Найти среди них любое, требующее авторизацию (любого типа).
# Выполнить запросы к нему, пройдя авторизацию. Ответ сервера записать в файл.
# https://vk.com/dev
url = 'https://api.vk.com'
method = 'users.get'
params = 'user_ids=669910806'
token= 'c11a057cc11a057cc11a057cf1c162fff6cc11ac11a057ca00172f89237a7d3cd9b73be'
fields= 'relation, sex, bdate, city, country'
req = requests.get(f'{url}/method/{method}?{params}&fields={fields}&access_token={token}&v=5.131')
with open('task_2.json', 'w') as f:
    json.dump(req.json(), f)




