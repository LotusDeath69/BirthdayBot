import sqlite3


def createConnection():
    global con
    global cur
    con = sqlite3.connect("database.db")
    cur = con.cursor()
    
    
def closeConnection():
    con.close()
    
    
def logRetrive():
    createConnection()
    with con:
        cur.execute('SELECT * FROM database')
    return cur.fetchall()


def logAdd(date, action, name):
    createConnection()
    with con:
        cur.execute('INSERT INTO database VALUES (:date, :action, :name)', {"date": date, "action": action, "name": name})
    return "Sucess"





# createConnection()
# cur.execute('''CREATE TABLE database
#                (date text, hours text, name text)''')
# print(logAdd("2022/04/07", "birthdayPing", "Stella"))
# print(logRetrive())
# con.commit()
# closeConnection()
