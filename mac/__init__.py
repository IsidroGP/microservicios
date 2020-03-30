import sqlite3
import json

import flask

app = flask.Flask(__name__)

@app.route('/netflix/original-content', methods=['GET', 'POST'])
def crud():
    if flask.request.method == 'GET':
        sqlite_conn = get_database_connection('./mac/original_content.db')
        sqlite_cursor = sqlite_conn.cursor()
        sqlite_cursor.execute('SELECT * FROM original_content')
        data = sqlite_cursor.fetchall()
        result = convert_cursor_to_json(data)
        return json.dumps(result)

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