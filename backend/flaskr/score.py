import sqlite3
from flask import Blueprint, request, session, jsonify
from .db import get_db

bp = Blueprint("score", __name__, url_prefix="/score")

@bp.route("/submit", methods=["POST"])
def submit_score():
    if "user_id" not in session:
        return jsonify({"error": "User not logged in"}), 401

    data = request.get_json()
    points = data.get("points")
    if points is None:
        return jsonify({"error": "Score (points) is required."}), 400

    db = get_db()
    try:
        db.execute(
            "INSERT INTO score (player_id, points) VALUES (?, ?)",
            (session["user_id"], points)
        )
        db.commit()
    except sqlite3.Error as e:
        return jsonify({"error": str(e)}), 500

    return jsonify({"message": "Score saved successfully."}), 201

@bp.route("/all", methods=["GET"])
def get_scores():
    db = get_db()
    scores = db.execute("SELECT * FROM score").fetchall()
    scores_list = [dict(score) for score in scores]
    return jsonify(scores_list), 200
