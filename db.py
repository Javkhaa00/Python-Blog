import sqlite3
conn = sqlite3.connect('./test.db')

c = conn.cursor()

# Create table
c.execute('''CREATE TABLE post (id integer PRIMARY KEY AUTOINCREMENT, title text, body text, date text)''')

# Insert a row of data to Post
c.execute("INSERT INTO post (title, body, date) VALUES ('Fisrt post','Fisrt body of post', date())")
c.execute("INSERT INTO post (title, body, date) VALUES ('Second post','Second body of post', date())")

# Create users

c.execute('''CREATE TABLE users (id integer PRIMARY KEY AUTOINCREMENT, name text, password text, date text)''')

# Insert a row of data to Users
c.execute("INSERT INTO users (name, password, date) VALUES ('test', '123', date())")

# Save (commit) the changes
conn.commit()

# We can also close the connection if we are done with it.
# Just be sure any changes have been committed or they will be lost.
conn.close()
