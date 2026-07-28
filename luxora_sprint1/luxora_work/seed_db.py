import sqlite3

# Your full 25-item inventory
all_products = [
    ('shoes', 'Leather Oxford', 8999, 'Classic black leather', '👞'),
    ('shoes', 'Running Sneaker', 5499, 'Comfortable sports shoe', '🏃'),
    ('shoes', 'Loafer Casual', 6499, 'Elegant daily wear', '👠'),
    ('shoes', 'Winter Boots', 7999, 'Premium leather boots', '🥾'),
    ('shoes', 'Heeled Pump', 6999, 'Sophisticated design', '👗'),
    
    ('electronics', 'Smart Watch', 14999, 'Advanced fitness tracker', '⌚'),
    ('electronics', 'Wireless Earbuds', 7999, 'Crystal clear sound', '🎧'),
    ('electronics', 'Tablet Pro', 29999, 'Portable computing', '📱'),
    ('electronics', 'Camera HD', 39999, 'Professional photography', '📷'),
    ('electronics', 'Laptop Stand', 3999, 'Ergonomic design', '💻'),
    
    ('clothing', 'Silk Blouse', 4999, 'Premium fabric', '👕'),
    ('clothing', 'Wool Sweater', 5999, 'Cozy winter wear', '🧥'),
    ('clothing', 'Tailored Blazer', 7999, 'Professional cut', '🎩'),
    ('clothing', 'Denim Jeans', 4499, 'Classic fit', '👖'),
    ('clothing', 'Cashmere Scarf', 3999, 'Luxurious texture', '🧣'),
    
    ('books', 'The Midnight Library', 399, 'Contemporary fiction', '📖'),
    ('books', 'Atomic Habits', 499, 'Self-improvement guide', '📚'),
    ('books', 'Sapiens', 599, 'History & science', '🔍'),
    ('books', 'Project Hail Mary', 449, 'Science fiction', '🚀'),
    ('books', 'Educated', 549, 'Memoir & inspiration', '🎓'),
    
    ('home', 'Ceramic Vase', 2999, 'Decorative art piece', '🏺'),
    ('home', 'Table Lamp', 3499, 'Modern design', '💡'),
    ('home', 'Silk Cushion', 1999, 'Premium comfort', '🛋️'),
    ('home', 'Wall Mirror', 4999, 'Elegant reflection', '🪞'),
    ('home', 'Plant Pot', 1499, 'Ceramic beauty', '🌿')
]

conn = sqlite3.connect('luxora.db')
cursor = conn.cursor()

# Drop the old table and create a fresh one
cursor.execute('DROP TABLE IF EXISTS products')
cursor.execute('''
CREATE TABLE products (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    category TEXT,
    name TEXT,
    price REAL,
    description TEXT,
    emoji TEXT
)
''')

# Insert all 25 products
cursor.executemany('''
INSERT INTO products (category, name, price, description, emoji)
VALUES (?, ?, ?, ?, ?)
''', all_products)

conn.commit()
conn.close()

print("✅ Database fully populated with 25 products!")