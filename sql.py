import sqlite3

# Connect to SQLite database
connection = sqlite3.connect("data.db")

cursor = connection.cursor()

# Create a sample table
table_info = """
CREATE TABLE IF NOT EXISTS STUDENT(
NAME TEXT,
CLASS TEXT,
SECTION TEXT,
MARKS INT
);
"""

cursor.execute(table_info)

# Insert sample records
cursor.execute("INSERT INTO STUDENT VALUES('John','Data Science','A',90);")
cursor.execute("INSERT INTO STUDENT VALUES('Alice','Data Science','B',85);")
cursor.execute("INSERT INTO STUDENT VALUES('Bob','Data Science','A',78);")
cursor.execute("INSERT INTO STUDENT VALUES('Eve','Data Science','B',92);")

connection.commit()
connection.close()

print("Database created successfully!")
