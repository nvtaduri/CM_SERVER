import sqlite3

connection = sqlite3.connect('database.db')

with open('schema.sql') as f:
    connection.executescript(f.read())

cur = connection.cursor()

cur.execute("INSERT INTO posts (person,status,assigned,priority,type,description) VALUES (?, ?,?,?,?,?)",
            ('vital','opened','developer','normal','type1','Content for the first change')
            )

cur.execute("INSERT INTO posts (person,status,assigned,priority,type,description) VALUES (?, ?,?,?,?,?)",
            ('chandu','created','designer','serious','type2','Content for the second change')
            )

connection.commit()
connection.close()