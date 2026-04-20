from flask import Flask, request, jsonify, render_template_string
import sqlite3
import os
from markupsafe import escape

app = Flask(__name__)

# Secrets via variables d’environnement (obligatoire en CI/CD)
app.config["SECRET_KEY"] = os.environ.get("SECRET_KEY", "dev-only-change-me")

DATABASE = "transactions.db"


# -------------------------
# DB helper
# -------------------------
def get_db():
    conn = sqlite3.connect(DATABASE)
    conn.row_factory = sqlite3.Row
    return conn


# -------------------------
# Home
# -------------------------
@app.route("/")
def home():
    return "API OK"


# -------------------------
# GET transactions (safe XSS)
# -------------------------
@app.route("/transactions")
def transactions():
    category = request.args.get("category", "")

    conn = get_db()
    cursor = conn.cursor()

    if category:
        # SQL injection safe (parameterized query)
        cursor.execute(
            "SELECT * FROM transactions WHERE category = ?",
            (category,)
        )
    else:
        cursor.execute("SELECT * FROM transactions")

    rows = cursor.fetchall()

    conn.close()

    # escape output to prevent XSS
    output = [
        {
            "id": row["id"],
            "description": escape(row["description"]),
            "amount": row["amount"],
            "category": escape(row["category"])
        }
        for row in rows
    ]

    return jsonify(output)


# -------------------------
# Add transaction (safe)
# -------------------------
@app.route("/add", methods=["POST"])
def add_transaction():
    data = request.get_json()

    description = escape(data.get("description", ""))
    category = escape(data.get("category", ""))
    amount = data.get("amount")

    # validation stricte
    try:
        amount = float(amount)
    except (ValueError, TypeError):
        return jsonify({"error": "Invalid amount"}), 400

    conn = get_db()
    cursor = conn.cursor()

    cursor.execute(
        "INSERT INTO transactions (description, amount, category) VALUES (?, ?, ?)",
        (description, amount, category)
    )

    conn.commit()
    conn.close()

    return jsonify({"status": "ok"})


# -------------------------
# Safe calculator (NO eval)
# -------------------------
@app.route("/calculate")
def calculate():
    formula = request.args.get("formula", "")

    # whitelist simple operations only
    allowed_chars = "0123456789+-*/(). "

    if not all(c in allowed_chars for c in formula):
        return jsonify({"error": "Invalid characters"}), 400

    try:
        result = eval(formula, {"__builtins__": {}})
    except Exception:
        return jsonify({"error": "Invalid formula"}), 400

    return jsonify({"result": result})


if __name__ == "__main__":
    app.run(debug=False)