import functools
import sqlite3
from flask import Blueprint, request, session, g, jsonify
from werkzeug.security import check_password_hash, generate_password_hash
from .db import get_db

bp = Blueprint("auth", __name__, url_prefix="/auth")

@bp.route("/test", methods=["GET"])
def test():
    return jsonify({"message": "Auth blueprint is working!"})

@bp.route("/register", methods=["POST"])
def register():
    data = request.get_json()
    username = data.get("username")
    password = data.get("password")
    db = get_db()

    if not username:
        return jsonify({"error": "Username is required."}), 400
    if not password:
        return jsonify({"error": "Password is required."}), 400

    try:
        db.execute(
            "INSERT INTO player (username, password) VALUES (?, ?)",
            (username, generate_password_hash(password, method="pbkdf2:sha256"))
        )
        db.commit()
    except sqlite3.IntegrityError:
        return jsonify({"error": f"User {username} is already registered."}), 400

    return jsonify({"message": "User registered successfully."}), 201

@bp.route("/login", methods=["POST"])
def login():
    data = request.get_json()
    username = data.get("username")
    password = data.get("password")
    db = get_db()

    user = db.execute(
        "SELECT * FROM player WHERE username = ?", (username,)
    ).fetchone()

    if user is None:
        return jsonify({"error": "Incorrect username."}), 400
    elif not check_password_hash(user["password"], password):
        return jsonify({"error": "Incorrect password."}), 400

    session.clear()
    session["user_id"] = user["id"]
    return jsonify({"message": "Logged in successfully."}), 200


@bp.route("/logout", methods=["POST"])
def logout():
    session.clear()
    return jsonify({"message": "Logged out."}), 200

