from flask import Flask, render_template_string
import mariadb
import os

app = Flask(__name__)

DB_CONFIG = {
    "host": "localhost",
    "user": "week4_reader",
    "password": open(
        "/home/ubuntu/week4/db-password"
    ).read().strip(),
    "database": "viikko2",
    "port": 3306
}

HTML = """
<!DOCTYPE html>
<html lang="fi">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1">
    <title>Weekly Assignment 4</title>
    <style>
        body {
            font-family: Arial, sans-serif;
            background: #f1f5f9;
            text-align: center;
            padding: 40px 15px;
        }
        .container {
            background: white;
            max-width: 650px;
            margin: auto;
            padding: 30px;
            border-radius: 12px;
        }
        .counter {
            font-size: 64px;
            font-weight: bold;
            color: #2563eb;
            margin: 25px;
        }
    </style>
</head>
<body>
<div class="container">
    <h1>Weekly Assignment 4</h1>
    <h2>Server B - Read-only replica</h2>

    <p>This server displays data from its local MariaDB replica.</p>

    <div class="counter">{{ visits }}</div>

    <p>Replicated visitor counter</p>

    <hr>

    <p><a href="/viikko2/">Server A - Week 2</a></p>
    <p><a href="/viikko4/">Server B - Week 4</a></p>
    <p><a href="{{ github_url }}">GitHub repository</a></p>
</div>
</body>
</html>
"""

@app.route("/")
@app.route("/viikko4/")
def index():
    connection = None

    try:
        connection = mariadb.connect(**DB_CONFIG)
        cursor = connection.cursor()
        cursor.execute("SELECT visits FROM counter WHERE id = 1")
        result = cursor.fetchone()
        visits = result[0] if result else 0
        cursor.close()

    except mariadb.Error:
        return "Database read failed", 500

    finally:
        if connection:
            connection.close()

    return render_template_string(
        HTML,
        visits=visits,
        github_url="#"
    )
