import sqlite3
import random
from faker import Faker

# Initialize Faker
fake = Faker()

# Connect to (or create) the SQLite database
conn = sqlite3.connect("supplier.db")
cursor = conn.cursor()

# --- Create Tables if They Don't Exist ---
cursor.execute("""
CREATE TABLE IF NOT EXISTS Suppliers (
    SupplierID INTEGER PRIMARY KEY AUTOINCREMENT,
    CompanyName TEXT NOT NULL,
    City TEXT,
    Country TEXT
);
""")

cursor.execute("""
CREATE TABLE IF NOT EXISTS Categories (
    CategoryID INTEGER PRIMARY KEY AUTOINCREMENT,
    CategoryName TEXT NOT NULL
);
""")

cursor.execute("""
CREATE TABLE IF NOT EXISTS Products (
    ProductID INTEGER PRIMARY KEY AUTOINCREMENT,
    ProductName TEXT NOT NULL,
    SupplierID INTEGER,
    CategoryID INTEGER,
    UnitPrice REAL,
    FOREIGN KEY (SupplierID) REFERENCES Suppliers(SupplierID)
);
""")

cursor.execute("""
CREATE TABLE IF NOT EXISTS OrderDetails (
    OrderID INTEGER PRIMARY KEY AUTOINCREMENT,
    ProductID INTEGER,
    Quantity INTEGER,
    UnitPrice REAL,
    FOREIGN KEY (ProductID) REFERENCES Products(ProductID)
);
""")

conn.commit()

# --- Insert Fake Data ---

# Insert Fake Data for Suppliers
num_suppliers = 100  # Increase this number as needed
suppliers_data = []
for _ in range(num_suppliers):
    company_name = fake.company()
    city = fake.city()
    country = fake.country()
    suppliers_data.append((company_name, city, country))

cursor.executemany(
    "INSERT INTO Suppliers (CompanyName, City, Country) VALUES (?, ?, ?);", 
    suppliers_data
)
print(f"Inserted {num_suppliers} suppliers.")

# Insert Fixed Categories
categories = ['Beverages', 'Dairy', 'Condiments', 'Confections', 'Grains/Cereals', 'Produce', 'Meat/Poultry']
categories_data = [(cat,) for cat in categories]
cursor.executemany(
    "INSERT INTO Categories (CategoryName) VALUES (?);", 
    categories_data
)
print(f"Inserted {len(categories)} categories.")

# Insert Fake Data for Products
num_products = 500  # Increase this number as needed
products_data = []
for _ in range(num_products):
    product_name = fake.word().capitalize()
    supplier_id = random.randint(1, num_suppliers)  # Assuming SupplierIDs start at 1
    category_id = random.randint(1, len(categories))  # Assuming CategoryIDs start at 1
    unit_price = round(random.uniform(1.0, 100.0), 2)
    products_data.append((product_name, supplier_id, category_id, unit_price))

cursor.executemany(
    "INSERT INTO Products (ProductName, SupplierID, CategoryID, UnitPrice) VALUES (?, ?, ?, ?);", 
    products_data
)
print(f"Inserted {num_products} products.")

# Insert Fake Data for OrderDetails
num_orders = 2000  # Increase this number as needed
order_details_data = []
for _ in range(num_orders):
    product_id = random.randint(1, num_products)
    quantity = random.randint(1, 50)
    
    # Retrieve the unit price for the selected product
    cursor.execute("SELECT UnitPrice FROM Products WHERE ProductID = ?;", (product_id,))
    result = cursor.fetchone()
    unit_price = result[0] if result else round(random.uniform(1.0, 100.0), 2)
    
    order_details_data.append((product_id, quantity, unit_price))

cursor.executemany(
    "INSERT INTO OrderDetails (ProductID, Quantity, UnitPrice) VALUES (?, ?, ?);", 
    order_details_data
)
print(f"Inserted {num_orders} order details.")

# Commit the transaction and close the connection
conn.commit()
conn.close()

print("✅ Database setup and data generation completed successfully!")
