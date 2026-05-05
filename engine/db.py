import sqlite3


conn = sqlite3.connect("aru.db")

cursor = conn.cursor()

# Create sys_command table
cursor.execute("""
CREATE TABLE IF NOT EXISTS sys_command(
    id INTEGER PRIMARY KEY,
    name TEXT UNIQUE,
    path TEXT
)
""")

# to insert values
# query = "INSERT INTO sys_command VALUES(null,'OneNote', 'C:\\Program Files (x86)\\Microsoft Office\\root\\Office16\\ONENOTE')"
# cursor.execute(query)
# conn.commit()
# conn.close()


# Create web_command table
cursor.execute("""
CREATE TABLE IF NOT EXISTS web_command(
    id INTEGER PRIMARY KEY,
    name TEXT UNIQUE,
    url TEXT
)
""")

# Insert safely (no duplicates)
cursor.execute("""
INSERT OR IGNORE INTO web_command (name, url)
VALUES (?, ?)
""", ("Facebook", "https://facebook.com"))
conn.commit()
conn.close()