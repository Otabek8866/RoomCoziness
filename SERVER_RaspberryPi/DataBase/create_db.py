import sqlite3

db = sqlite3.connect('mainDB')
cursor = db.cursor()

stm1 = "CREATE TABLE roomA(id integer PRIMARY KEY AUTOINCREMENT,date text NOT NULL,time text NOT NULL,temperature text NOT NULL,noise text NOT NULL,light text NOT NULL,co2 text NOT NULL,humidity text NOT NULL);"
stm2 = "CREATE TABLE roomB(id integer PRIMARY KEY AUTOINCREMENT,date text NOT NULL,time text NOT NULL,temperature text NOT NULL,noise text NOT NULL,light text NOT NULL,co2 text NOT NULL,humidity text NOT NULL);"
stm3 = "CREATE TABLE roomC(id integer PRIMARY KEY AUTOINCREMENT,date text NOT NULL,time text NOT NULL,temperature text NOT NULL,noise text NOT NULL,light text NOT NULL,co2 text NOT NULL,humidity text NOT NULL);"

cursor.execute(stm1)
cursor.execute(stm2)
cursor.execute(stm3)

cursor.connection.commit()

cursor.close()
db.close()
print("DataBase created successfully")
