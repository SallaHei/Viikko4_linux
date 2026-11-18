from flask import Flask, render_template_string
import mariadb

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
    <meta name="viewport"
          content="width=device-width, initial-scale=1">

    <title>Viikko 4 - MariaDB Replica</title>

    <style>
        body {
            margin: 0;
            padding: 50px 20px;
            font-family: Arial, sans-serif;
            background: #101827;
            color: white;
            text-align: center;
        }

        .container {
            max-width: 700px;
            margin: auto;
            padding: 40px;
            background: #1e293b;
            border-radius: 20px;
        }

        h1 {
            color: #38bdf8;
        }

        .counter {
            font-size: 75px;
            color: #4ade80;
            font-weight: bold;
            margin: 30px;
        }

        .info {
            background: #334155;
            padding: 20px;
            border-radius: 12px;
            margin-top: 25px;
            line-height: 1.7;
        }

        a {
            color: #38bdf8;
        }

        .status {
            color: #4ade80;
            font-weight: bold;
            font-size: 18px;
        }

        .label {
            display: inline-block;
            background: #164e63;
            color: #67e8f9;
            padding: 8px 16px;
            border-radius: 20px;
            font-weight: bold;
        }
    </style>
</head>

<body>
    <div class="container">

        <h1>Python-verkkosovellus</h1>

        <p>
            Tervetuloa viikon 4 palvelimelle!
        </p>

        <div class="label">
            SERVER B - READ-ONLY REPLICA
        </div>

        <h2>Replikoitu kävijälaskuri</h2>

        <div class="counter">{{ visits }}</div>

        <p>
            Tämä laskuri näyttää Server A:n tietokannasta
            replikoidun arvon.
        </p>

        <div class="info">

            <h2>Tekninen toteutus</h2>

            <p>
                Sovellus on toteutettu Pythonilla
                käyttäen Flask-sovelluskehystä.
            </p>

            <p>
                Nginx toimii välityspalvelimena
                ja Gunicorn suorittaa Python-sovellusta.
            </p>

            <h2>Tietokanta ja replikaatio</h2>

            <p>
                Server A toimii MariaDB Master -palvelimena
                ja Server B toimii Replica-palvelimena.
            </p>

            <p>
                Tämä sivu lukee kävijälaskurin Server B:n
                paikallisesta MariaDB-tietokannasta.
                Tiedot päivittyvät automaattisesti
                Server A:lta replikaation kautta.
            </p>

            <p class="status">
                Database access: READ ONLY
            </p>

            <p>
                Sivun lataaminen ei kasvata kävijälaskuria
                eikä muuta tietokannan tietoja.
            </p>

            <h2>Palvelinten verkkosivut</h2>

            <p>
                <a href="http://193.166.24.7/viikko2/">
                    Server A - Week 2
                </a>
            </p>

            <p>
                <a href="http://86.50.252.36/viikko4/">
                    Server B - Week 4
                </a>
            </p>

            <h2>GitHub-repository</h2>

            <p>
                <a href="https://github.com/SallaHei/Viikko4_linux"
                   target="_blank">
                    Week 4 GitHub repository
                </a>
            </p>

            <h2>Uudelleenkäynnistystesti</h2>

            <p>
                Palvelimen uudelleenkäynnistystesti on suoritettu.
                Nginx, MariaDB ja Python-sovellus tarkistettiin
                uudelleenkäynnistyksen jälkeen.
            </p>

        </div>
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

        # Vain luku -kysely.
        # Laskuria ei kasvateta tällä sivulla.
        cursor.execute(
            "SELECT visits FROM counter WHERE id = 1"
        )

        result = cursor.fetchone()
        visits = result[0] if result else 0

        cursor.close()

    except mariadb.Error:
        app.logger.exception("Database read failed")
        return "Database read failed", 500

    finally:
        if connection:
            connection.close()

    return render_template_string(
        HTML,
        visits=visits
    )


if __name__ == "__main__":
    app.run()
