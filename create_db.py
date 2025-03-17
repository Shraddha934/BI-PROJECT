import sqlite3

conn = sqlite3.connect("supplier.db")
cursor = conn.cursor()

# Create Suppliers Table
cursor.execute("""
CREATE TABLE IF NOT EXISTS Suppliers (
    SupplierID INTEGER PRIMARY KEY AUTOINCREMENT,
    CompanyName TEXT NOT NULL,
    City TEXT,
    Country TEXT
);
""")

# Create Categories Table
cursor.execute("""
CREATE TABLE IF NOT EXISTS Categories (
    CategoryID INTEGER PRIMARY KEY AUTOINCREMENT,
    CategoryName TEXT NOT NULL
);
""")

# Create Products Table
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

# Create OrderDetails Table
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
conn.close()
print("✅ Tables created successfully!")
