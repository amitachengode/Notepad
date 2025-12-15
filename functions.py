from datetime import datetime
from json import load,dump

def get_timestamp():
    return datetime.now().strftime("%Y-%m-%d %H:%M:%S")

def read():
    with open("file.json", "r") as file:
        data = load(file)
    return data

def write(data):
    with open("file.json", "w") as file:
        dump(data, file, indent=4)