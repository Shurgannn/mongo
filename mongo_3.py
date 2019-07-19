import csv
import re
from pymongo import MongoClient
from pprint import pprint


def read_data(csv_file, db):
    client = MongoClient()
    netology_artists = client[db]
    collection = netology_artists['artists-collection']
    """
    Загрузить данные в бд из CSV-файла
    """
    with open(csv_file, encoding='utf8') as csvfile:
        # прочитать файл с данными и записать в коллекцию
        reader = csv.DictReader(csvfile)
        artists = []
        for line in reader:
            artists_dict = {}
            artists_dict["Исполнитель"] = line["Исполнитель"]
            artists_dict["Цена"] = int(line["Цена"])
            artists_dict["Место"] = line["Место"]
            artists_dict["Дата"] = line["Дата"]
            artists.append(artists_dict)
        # result = collection.insert_many(artists).inserted_ids
        return collection
        # pprint(list(collection.find()))
        # print(len(list(collection.find())))
        # print(collection.find_one({'Исполнитель': 'T-Fest'}))


def find_cheapest(db):
    """
    Отсортировать билеты из базы по возрастания цены
    Документация: https://docs.mongodb.com/manual/reference/method/cursor.sort/
    """
    sort_by_price = []
    for col in read_data('artists.csv', db).find().sort('Цена'):
        sort_by_price.append(col)
    pprint(sort_by_price)


def find_by_name(name, db):
    """
    Найти билеты по имени исполнителя (в том числе – по подстроке),
    и вернуть их по возрастанию цены
    """
    for col in read_data('artists.csv', db).find().sort('Цена'):
        regex = re.compile(name)
        match = re.search(regex, col['Исполнитель'])
        if match:
            print('Found "{}"'.format(col))
            break
    else:
        print('Did not find "{}"'.format(name))


if __name__ == '__main__':
    # read_data('artists.csv', 'netology_artists')
    # find_cheapest('netology_artists')
    find_by_name('Шуф', 'netology_artists')
