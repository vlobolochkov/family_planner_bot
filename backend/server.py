from flask import Flask, request, jsonify
from flask_cors import CORS
import sqlite3
import os

app = Flask(__name__)
CORS(app)

def init_db():
    conn = sqlite3.connect("tasks.db")
    c = conn.cursor()
    c.execute('''
        CREATE TABLE IF NOT EXISTS tasks (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            user_id TEXT NOT NULL,
            text TEXT NOT NULL
        )
    ''')
    conn.commit()
    conn.close()

@app.route("/")
def home():
    return "Сервер работает. Используйте /tasks для API."

@app.route("/tasks", methods=["GET"])
def get_tasks():
    user_id = request.args.get("user_id")
    if not user_id:
        return jsonify({"error": "user_id is required"}), 400

    conn = sqlite3.connect("tasks.db")
    c = conn.cursor()
    c.execute("SELECT id, text FROM tasks WHERE user_id = ?", (user_id,))
    tasks = [{"id": row[0], "text": row[1]} for row in c.fetchall()]
    conn.close()
    return jsonify(tasks)

@app.route("/tasks", methods=["POST"])
def add_task():
    data = request.get_json()
    user_id = data.get("user_id")
    text = data.get("text")

    if not user_id or not text:
        return jsonify({"error": "user_id and text are required"}), 400

    conn = sqlite3.connect("tasks.db")
    c = conn.cursor()
    c.execute("INSERT INTO tasks (user_id, text) VALUES (?, ?)", (user_id, text))
    conn.commit()
    conn.close()

    return jsonify({"status": "ok"})

if __name__ == "__main__":
    init_db()
    port = int(os.environ.get("PORT", 5000))  # Используем порт Render или локальный по умолчанию
    app.run(host="0.0.0.0", port=port)
