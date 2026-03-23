from flask import Flask, jsonify, request
from flask_cors import CORS
import sqlite3

app = Flask(__name__)
CORS(app)


def get_db():
    conn = sqlite3.connect("skills.db")
    conn.row_factory = sqlite3.Row
    return conn


def init_db():
    conn = get_db()
    conn.execute(
        """
        CREATE TABLE IF NOT EXISTS skills (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            nama TEXT NOT NULL
        )
    """
    )
    conn.commit()
    conn.close()


@app.route("/skills", methods=["GET"])
def get_skills():
    conn = get_db()
    skills = conn.execute("SELECT * FROM skills").fetchall()
    conn.close()
    return jsonify([dict(s) for s in skills])


@app.route("/skills", methods=["POST"])
def add_skills():
    data = request.json
    conn = get_db()
    conn.execute("INSERT INTO skills (nama) VALUES (?)", (data["nama"],))
    conn.commit()
    conn.close()
    return jsonify({"pesan": "skill ditambahkan"}), 201


@app.route("/skills/<int:id>", methods=["DELETE"])
def delete_skill(id):
    conn = get_db()
    skill = conn.execute("SELECT * FROM skills WHERE id = ?", (id,)).fetchone()
    if skill is None:
        return jsonify({"error": "skill tidak ditemukan"}), 404
    conn.execute("DELETE FROM skills WHERE id = ?", (id,))
    conn.commit()
    conn.close()
    return jsonify({"pesan": "skill berhasil dihapus"})


if __name__ == "__main__":
    init_db()
    app.run(debug=True)
