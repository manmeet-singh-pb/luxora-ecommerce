from flask import Flask, jsonify, render_template
from flask_cors import CORS
import sqlite3

app = Flask(__name__)
CORS(app)  # Kept for now — see note in the chat about when this can be removed

# Pages we're allowed to serve. Keeping an explicit allow-list (instead of
# blindly rendering any filename the browser asks for) is a small but
# important security habit: it stops someone from requesting arbitrary
# files from the templates/ folder via the URL.
ALLOWED_PAGES = {'index.html', 'products.html', 'cart.html', 'login.html'}

@app.route('/')
def home():
    print(">>> HOME ROUTE CALLED <<<")
    return render_template('index.html')

@app.route('/<page_name>')
def serve_page(page_name):
    if page_name in ALLOWED_PAGES:
        return render_template(page_name)
    return "Page not found", 404

# Helper function to connect to the database
def get_db_connection():
    conn = sqlite3.connect('luxora.db')
    conn.row_factory = sqlite3.Row # This lets us access columns by name (like a dictionary)
    return conn

@app.route('/api/products', methods=['GET'])
def get_products():
    # 1. Connect to the DB and get all products
    conn = get_db_connection()
    db_products = conn.execute('SELECT * FROM products').fetchall()
    conn.close()

    # 2. Format the database rows into the exact JSON structure your frontend expects
    formatted_products = {
        "shoes": [],
        "electronics": [],
        "clothing": [],
        "books": [],
        "home": []
    }
    
    for row in db_products:
        cat = row['category']
        if cat not in formatted_products:
            formatted_products[cat] = [] # Safety check in case of a new category
            
        formatted_products[cat].append({
            "id": row['id'],
            "name": row['name'],
            "price": row['price'],
            "description": row['description'],
            "emoji": row['emoji']
        })

    # 3. Send it to the frontend!
    return jsonify(formatted_products)

if __name__ == '__main__':
    print("🚀 LUXORA Backend is running on http://localhost:5001")
    app.run(port=5001)