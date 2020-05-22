import sqlite3
import json
import requests
from dbConn import *
from elements import *
from flask import Flask, render_template, request

def get_sentence(sqlite_cursor, genero, type, popularity):
    command = "SELECT * FROM original_content"

    if genero != None or type != None or popularity != None:
        command = command + " WHERE "
        if genero != None:
            command = command + "genre = "+genero+""
            if type != None or popularity != None:
                command = command + " and "
        if type != None:
            command = command + "type = "+type+""
            if popularity != None:
                command = command + " and "
        if popularity != None:
            command = command + "imdb_rating ="+popularity+""

    sqlite_cursor.execute(command)


def get_database_connection(database_path):
    conn = sqlite3.connect(database_path)
    return conn

def convert_cursor_to_json(cursor_data):
    result_list = []
    for e in cursor_data:
        temp_dict = {}
        temp_dict['id'] = e[0]
        temp_dict['name'] = e[1]
        temp_dict['type'] = e[2]
        temp_dict['genre'] = e[3]
        temp_dict['imdb_rating'] = e[4]
        result_list.append(temp_dict)
    return result_list
