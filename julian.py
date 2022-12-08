import os
import json
import csv

def json_extract(obj, key):
    """Recursively fetch values from nested JSON."""
    arr = []

    def extract(obj, arr, key):
        """Recursively search for values of key in JSON tree."""
        if isinstance(obj, dict):
            for k, v in obj.items():
                if isinstance(v, (dict, list)):
                    extract(v, arr, key)
                elif k == key:
                    arr.append(v)
        elif isinstance(obj, list):
            for item in obj:
                extract(item, arr, key)
        return arr

    values = extract(obj, arr, key)
    return values

class AppResult:
    name = ''
    score = 0
    broken_ssl = 0
    foreign_country = 0
    heartbleed = 0

apps = []

files = os.scandir()
for x in os.listdir():
    if x.endswith(".json"):
        f = open(x, encoding="utf8")
        data = json.load(f)
        
        for d in data:
            app = AppResult()
            app.name = json_extract(d, 'title')[0]
            app.score = json_extract(d, 'score')[0]
            app.broken_ssl = any(json_extract(d, 'broken_ssl'))
            countries = json_extract(d, 'country_short')
            app.foreign_country = any(country != 'US' for country in countries)
            app.heartbleed = json_extract(d, 'heartbleed_check')
            apps.append(app)
        
        f.close()

header = ['title', 'score', 'heartbleed', 'f_country']
data = []
for app in apps:
    row = []
    row.append(app.name)
    row.append(app.score)
    row.append(app.foreign_country)
    row.append(app.heartbleed)
    data.append(row)

    print(f'Title: {app.name} - Score: {app.score} - FC: {app.foreign_country}')

with open('results.csv', 'w', encoding='UTF8', newline='') as f:
    writer = csv.writer(f)
    writer.writerow(header)
    writer.writerows(data)
