from datetime import datetime
from . import core

def get_timestamp():
    return datetime.now().strftime("%Y-%m-%d %H:%M:%S")

def generate_id():
    return datetime.now().strftime("%Y%m%d%H%M%S%f")

def get_file_id(file_title: str):
    file_data = get_file_data()
    for file in file_data:
        if file["title"] == file_title:
            return file["id"]
    return ""

def get_file_title(file_id: str):
    file_data = core.get_file_data()
    for file in file_data:
        if file["id"] == file_id:
            return file["title"]
    return ""

def get_file_timestamp(file_id: str):
    file_data = core.get_file_data()
    for file in file_data:
        if file["id"] == file_id:
            return file["timestamp"]
    return ""

def get_file_data(title: str|None = None, file_id: str|None = None):
    file_data = core.get_file_data()
    for file in file_data:
        if title==file["title"] :
            return file
        if file_id==file["id"]:
            return file
    else:
        return None