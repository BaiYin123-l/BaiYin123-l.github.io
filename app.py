
from flask import Flask, render_template, request, jsonify
import os
import glob
import datetime
import sqlite3
import json
import time

app = Flask(__name__)


def execute_query(file_name, table_name, columns):
    db_path = os.path.join(app.static_folder, 'sql', f'{file_name}.db')
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()

    columns_str = ','.join(columns) if columns else '*'
    query = f"SELECT {columns_str} FROM {table_name}"  # Removed unnecessary semicolon
    cursor.execute(query)
    rows = cursor.fetchall()

    conn.close()
    return rows


@app.route('/')
def index():
    articles = []

    # Path to your text files directory
    text_files_path = os.path.join(app.static_folder, 'file/*.txt')

    # Fetch all txt files in the directory
    files = glob.glob(text_files_path)

    for file_path in files:
        # Read content of each txt file
        with open(file_path, 'r', encoding='utf-8') as file:
            content = file.read().strip()

        # Get file modification time
        modification_time = os.path.getmtime(file_path)
        mod_time_str = datetime.datetime.fromtimestamp(modification_time).strftime('%Y-%m-%d %H:%M:%S')

        # Extract title (first line of the content)
        first_line = content.split('\n')[0] if '\n' in content else content

        articles.append({
            'title': first_line,
            'content': content,
            'modified_time': mod_time_str
        })

    return render_template('index.html', articles=articles)


@app.route('/projects/')
def projects():
    # Path to your sql folder
    sql_folder_path = os.path.join(app.static_folder, 'sql')

    # Fetch all txt files in the sql folder
    files = [f[:-3] for f in os.listdir(sql_folder_path) if f.endswith('.db')]
    # print("Found database files:", files)

    # Prepare data to pass to template
    tabs = []

    for file_name in files:
        db_path = os.path.join(sql_folder_path, f'{file_name}.db')
        conn = sqlite3.connect(db_path)
        cursor = conn.cursor()

        # Get tables in the database
        cursor.execute("SELECT name FROM sqlite_master WHERE type='table'")
        tables = cursor.fetchall()

        file_tabs = []
        for table in tables:
            table_name = table[0]
            cursor.execute(f"PRAGMA table_info({table_name})")
            columns = [column[1] for column in cursor.fetchall()]
            file_tabs.append({
                'name': table_name,
                'columns': columns
            })

        tabs.append({
            'file_name': file_name,
            'tabs': file_tabs
        })

        conn.close()

    return render_template('projects.html', tabs=tabs)


@app.route('/query')
def query():
    file_name = request.args.get('file', '')
    table_name = request.args.get('table', '')

    # From JSON file, get columns
    json_file_path = os.path.join(app.static_folder, 'sql', 'sql_show.txt')
    with open(json_file_path, 'r', encoding='utf-8') as json_file:
        json_data = json.load(json_file)

    try:
        columns = json_data[file_name][table_name] if table_name else []
    except KeyError:
        columns = []

    # If table_name is empty, prepare a message or handle as needed
    if not table_name:
        return jsonify({'message': 'Please select a sub-option'})

    # Execute SQL query
    results = execute_query(file_name, table_name, columns)

    return jsonify(results)



@app.route('/about/')
def about():
    return render_template('about.html')


if __name__ == '__main__':
    app.run(debug=True)

