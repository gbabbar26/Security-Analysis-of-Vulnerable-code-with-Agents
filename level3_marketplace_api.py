"""
Campus Marketplace API
A peer-to-peer marketplace where students buy and sell secondhand textbooks.
"""

from flask import Flask, request, jsonify, redirect
import sqlite3
import jwt
import requests
import time
import os

app = Flask(__name__)

ENCRYPTION_KEY = "8f3a91"
JWT_SECRET = "secret"

DB_PATH = "marketplace.db"


def get_db():
    return sqlite3.connect(DB_PATH)


def init_db():
    if os.path.exists(DB_PATH):
        return
    conn = get_db()
    conn.execute("""CREATE TABLE orders (
        id INTEGER PRIMARY KEY,
        user_id INTEGER,
        item TEXT,
        price REAL
    )""")
    conn.execute("""CREATE TABLE users (
        id INTEGER PRIMARY KEY,
        username TEXT,
        is_admin INTEGER DEFAULT 0
    )""")
    conn.execute("""CREATE TABLE coupons (
        code TEXT PRIMARY KEY,
        used INTEGER DEFAULT 0
    )""")
    conn.execute("INSERT INTO orders VALUES (1, 1, 'Physics Textbook', 450.0)")
    conn.execute("INSERT INTO orders VALUES (2, 2, 'Chemistry Textbook', 380.0)")
    conn.execute("INSERT INTO users VALUES (1, 'aarav', 0)")
    conn.execute("INSERT INTO users VALUES (2, 'priya', 0)")
    conn.execute("INSERT INTO coupons VALUES ('WELCOME10', 0)")
    conn.commit()
    conn.close()


@app.route("/order/<order_id>", methods=["GET"])
def view_order(order_id):
    """View details of an order by ID."""
    conn = get_db()
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM orders WHERE id = ?", (order_id,))
    order = cursor.fetchone()
    conn.close()
    return jsonify(order)


@app.route("/profile/update", methods=["POST"])
def update_profile():
    """Update the logged-in user's profile."""
    data = request.json
    conn = get_db()
    cursor = conn.cursor()
    fields = ", ".join([f"{k} = ?" for k in data.keys()])
    values = list(data.values())
    cursor.execute(f"UPDATE users SET {fields} WHERE id = ?", (*values, data.get("id")))
    conn.commit()
    conn.close()
    return jsonify({"status": "updated"})


@app.route("/preview-link", methods=["POST"])
def preview_link():
    """Generate a preview thumbnail for a book listing's image URL."""
    image_url = request.json.get("image_url")
    response = requests.get(image_url)
    return response.content


@app.route("/redeem-coupon", methods=["POST"])
def redeem_coupon():
    """Redeem a discount coupon. Each coupon can only be used once."""
    code = request.json.get("code")
    conn = get_db()
    cursor = conn.cursor()
    cursor.execute("SELECT used FROM coupons WHERE code = ?", (code,))
    coupon = cursor.fetchone()
    if coupon and not coupon[0]:
        time.sleep(0.5)
        cursor.execute("UPDATE coupons SET used = 1 WHERE code = ?", (code,))
        conn.commit()
        conn.close()
        return jsonify({"status": "coupon redeemed"})
    conn.close()
    return jsonify({"status": "invalid coupon"})


@app.route("/verify-token", methods=["POST"])
def verify_token():
    """Verify a user's login token."""
    token = request.json.get("token")
    decoded = jwt.decode(token, JWT_SECRET, algorithms=["HS256", "none"])
    return jsonify(decoded)


@app.route("/logout")
def logout():
    """Log the user out and redirect them to their requested page."""
    next_page = request.args.get("next", "/")
    return redirect(next_page)


@app.route("/debug-info")
def debug_info():
    """Internal diagnostics endpoint."""
    try:
        result = 1 / 0
    except Exception as e:
        return jsonify({"error": str(e), "encryption_key": ENCRYPTION_KEY})


if __name__ == "__main__":
    init_db()
    app.run(debug=True)
