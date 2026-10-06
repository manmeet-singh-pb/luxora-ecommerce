import sqlite3

# Connect to SQLite (this automatically creates a file named 'luxora.db')
conn = sqlite3.connect('luxora.db')
cursor = conn.cursor()

# Create a table for our products
cursor.execute('''
CREATE TABLE IF NOT EXISTS products (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    category TEXT,
    name TEXT,
    price REAL,
    description TEXT,
    emoji TEXT
)
''')

# Users table — added in Phase 2 for authentication
cursor.execute('''
CREATE TABLE IF NOT EXISTS users (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    name TEXT NOT NULL,
    email TEXT NOT NULL UNIQUE,
    password_hash TEXT NOT NULL,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
)
''')

# The initial data to insert
initial_products = [
    ('shoes', 'Leather Oxford', 8999, 'Classic black leather', '👞'),
    ('shoes', 'Running Sneaker', 5499, 'Comfortable sports shoe', '🏃'),
    ('electronics', 'Smart Watch', 14999, 'Advanced fitness tracker', '⌚'),
    ('electronics', 'Wireless Earbuds', 7999, 'Crystal clear sound', '🎧')
]

# Insert the data into the database
cursor.executemany('''
INSERT INTO products (category, name, price, description, emoji)
VALUES (?, ?, ?, ?, ?)
''', initial_products)

# Save (commit) the changes and close the connection
conn.commit()
conn.close()

print("✅ Database 'luxora.db' created successfully with initial products!")