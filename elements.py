#import sqlite3
#import json
#import requests
#from controllers import *
#from dbConn import *
#from elements import *
#from flask import Flask, render_template, request

def update_element(id,sqlite_cursor,json_body):
    title = json_body['Title']
    genre = json_body['Genre']
    type = json_body['Type']
    imdb_rtg = json_body['imdbRag']
    sqlite_cursor.execute("UPDATE original_content SET name = ?, type = ?,genre = ?,imdb_rating = ? WHERE id = ?",(title,type,genre,imdb_rtg,str(id)))

def create_element(sqlite_cursor, json_body):
    sqlite_cursor.execute('SELECT id FROM original_content WHERE id = (SELECT MAX(id) FROM original_content)')
    id = int(str(sqlite_cursor.fetchone()[0])) + 1
    title = json_body['Title']
    type = json_body['Type']
    genre = json_body['Genre'].split()[0].split(",")[0]
    imdb_rtg = json_body['imdbRating']
    sqlite_cursor.execute("INSERT INTO original_content VALUES (?,?,?,?,?)",(str(id), title, type, genre, str(imdb_rtg)))