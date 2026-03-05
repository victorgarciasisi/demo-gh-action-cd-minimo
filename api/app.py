import os

import psycopg2
from flask import Flask, jsonify

app = Flask(__name__)


def get_db():
    return psycopg2.connect(
        host=os.getenv('DB_HOST', 'db'),
        database=os.getenv('DB_NAME', 'appdb'),
        user=os.getenv('DB_USER', 'postgres'),
        password=os.getenv('DB_PASSWORD', 'demo-password'),
    )


@app.get('/health')
def health():
    return jsonify({"status": "APP ok"})


@app.get('/users')
def users():
    conn = get_db()
    cur = conn.cursor()
    cur.execute("SELECT id, name FROM users ORDER BY id")
    rows = cur.fetchall()
    cur.close()
    conn.close()
    return jsonify([{"id": r[0], "name": r[1]} for r in rows])


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
