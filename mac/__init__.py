import sqlite3
import json
import requests
from flask import Flask, render_template, request

app = Flask(__name__)
app.config['DEBUG'] = True

@app.route('/netflix/original-content', methods=['GET', 'POST'])
def crud():
    render_template("hola.html")
    if request.method == 'GET':
        genero = request.args.get('gen')
        type = request.args.get('type')
        popularity = request.args.get('pop')
        sqlite_conn = get_database_connection('./mac/original_content.db')
        sqlite_cursor = sqlite_conn.cursor()
        get_sentence(sqlite_cursor, genero, type, popularity)
        data = sqlite_cursor.fetchall()
        result = convert_cursor_to_json(data)
        return render_template('hola.html',results = (result))
    elif request.method == 'POST':
        title = request.form
        apikey = "712828a0"
        headers = {"Authorization":apikey}
        sqlite_conn = get_database_connection('./mac/original_content.db')
        sqlite_cursor = sqlite_conn.cursor()
        sqlite_cursor.execute('SELECT * FROM original_content')
        data = sqlite_cursor.fetchall()
        result = convert_cursor_to_json(data)
        req = requests.get("http://www.omdbapi.com/?t={0}&plot=full&apikey=712828a0&".format(title['title']))
        json_body = req.json();
        create_element(sqlite_cursor, json_body)
        sqlite_cursor.execute('SELECT * FROM original_content')
        data = sqlite_cursor.fetchall()
        result = convert_cursor_to_json(data)
        sqlite_conn.commit()
        return render_template('hola.html',results = (result))

@app.route('/netflix/original-content/<int:id>', methods=['GET','PATCH'])
def get_sentence_id(id):
    if request.method == 'GET':
        print("get")
        sqlite_conn = get_database_connection('./mac/original_content.db')
        sqlite_cursor = sqlite_conn.cursor()
        sqlite_cursor.execute("SELECT * FROM original_content WHERE id ="+str(id)+"")
        data = sqlite_cursor.fetchall()
        result = convert_cursor_to_json(data)
        return render_template('hola2.html', results = (result), datas = (result))
    if request.method == 'PATCH':
        print("patch")
        json_body = request.get_json()
        print(json_body)
        print("dsadasdasd")
        return "HOLA"

def get_sentence(sqlite_cursor, genero, type, popularity):
    if genero != None:
        sqlite_cursor.execute("SELECT * FROM original_content WHERE genre ="+genero+"")
    elif type != None:
        sqlite_cursor.execute("SELECT * FROM original_content WHERE type ="+type+"")
    elif popularity != None:
        sqlite_cursor.execute("SELECT * FROM original_content WHERE imdb_rating ="+popularity+"")
    else:
        sqlite_cursor.execute("SELECT * FROM original_content")

def create_element(sqlite_cursor, json_body):
    sqlite_cursor.execute('SELECT id FROM original_content WHERE id = (SELECT MAX(id) FROM original_content)')
    id = int(str(sqlite_cursor.fetchone()[0])) + 1
    title = json_body['Title']
    type = json_body['Type']
    genre = json_body['Genre'].split()[0].split(",")[0]
    imdb_rtg = json_body['imdbRating']
    sqlite_cursor.execute("INSERT INTO original_content VALUES (?,?,?,?,?)",(str(id), title, type, genre, str(imdb_rtg)))



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

if __name__ == '__main__':
    # Se ejecuta el servicio definiendo el host '0.0.0.0'
    #  para que se pueda acceder desde cualquier IP
    app.run(host='0.0.0.0', port='8084', debug=True)
