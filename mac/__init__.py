import sqlite3
import json
import requests
from dbConn import *
from elements import *
from flask import Flask, render_template, request

app = Flask(__name__)
app.config['DEBUG'] = True

@app.route('/netflix/original-content', methods=['GET', 'POST'])
def crud():
    render_template("hola.html")
    sqlite_conn = get_database_connection('./mac/original_content.db')
    sqlite_cursor = sqlite_conn.cursor()

    if request.method == 'GET':
        genero = request.args.get('gen')
        type = request.args.get('type')
        popularity = request.args.get('pop')
        get_sentence(sqlite_cursor, genero, type, popularity)
    if request.method == 'POST':
        title = request.form
        apikey = "712828a0"
        headers = {"Authorization":apikey}
        req = requests.get("http://www.omdbapi.com/?t={0}&plot=full&apikey=712828a0&".format(title['title']))
        json_body = req.json();
        create_element(sqlite_cursor, json_body)
        sqlite_cursor.execute('SELECT * FROM original_content')
        sqlite_conn.commit()

    data = sqlite_cursor.fetchall()
    result = convert_cursor_to_json(data)
    return render_template('hola.html',results = (result))

@app.route('/netflix/original-content/<int:id>', methods=['GET','PATCH'])
def get_sentence_id(id):
    sqlite_conn = get_database_connection('./mac/original_content.db')
    sqlite_cursor = sqlite_conn.cursor()

    if request.method == 'GET':
        sqlite_cursor.execute("SELECT * FROM original_content WHERE id ="+str(id)+"")
    if request.method == 'PATCH':
        json_body = request.get_json()
        update_element(id,sqlite_cursor,json_body)
        sqlite_cursor.execute("SELECT * FROM original_content WHERE id ="+str(id)+"")
    data = sqlite_cursor.fetchall()
    result = convert_cursor_to_json(data)
    if request.method == 'PATCH':
        sqlite_conn.commit()
    return render_template('hola2.html', results = (result), datas = (result))

if __name__ == '__main__':
    # Se ejecuta el servicio definiendo el host '0.0.0.0'
    #  para que se pueda acceder desde cualquier IP
    app.run(host='0.0.0.0', port='8084', debug=True)
