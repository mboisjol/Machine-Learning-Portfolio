import os

from clint.textui import puts, colored, prompt
from tinydb import TinyDB, Query

from config.qt_config import QTConfig

config = QTConfig.get_config()
db = TinyDB(config.db_path)

def insert(obj):
    if obj is not dict:
        obj = obj.__dict__

    db.insert(obj)


def insert_all(objs):
    for i in range(len(objs)):
        if objs[i] is not dict:
            objs[i] = objs[i].__dict__

    db.insert_multiple(objs)


def get_all():
    return db.all()


def get_by_id(id):
    document = Query()
    db.search(document.doc_id == id)


def get_by(field, value):
    document = Query()
    db.search(document[field] == value)


def delete_by_id(id):
    document = Query()
    db.delete(document.doc_id == id)


def delete_all():
    global db
    db.close()
    os.remove(config.db_path)
    db = TinyDB(config.db_path)



def to_csv(obj, name_file):
    refs = vars(obj).keys()
    separator = ","

    if os.path.exists(name_file):
        puts(colored.red(f"There is already a file named: {name_file}"))
        override = prompt.yn("Do you want to override it?")

        if not override:
            name_file = prompt.query("What should be the new name: ")

    with open(name_file, "w+", encoding="utf-8") as file:
        columns = separator.join(refs)
        file.write(columns + "\n")

        for doc in get_all():
            values = []
            for ref in refs:
                try:
                    values.append(doc[ref])
                except KeyError:
                    values.append("N/A")
            row = separator.join(values)
            file.write(row + "\n")
