import sqlite3


def createConnection():
    global con
    global cur
    con = sqlite3.connect('database.db')
    cur = con.cursor()
    
    
def closeConnection():
    con.close()
    
    
def logRetrive():
    createConnection()
    with con:
        cur.execute('SELECT * FROM database WHERE name=:name ', {"name": 'logs'})
    return cur.fetchall()


def logAdd(date, action, name):
    createConnection()
    with con:
        cur.execute('INSERT INTO database VALUES (:date, :action, :name)', {"date": date, "action": action, "name": name})
    return "Sucess"



# createConnection()
# cur.execute('''CREATE TABLE database
#                (date text, hours text, name text)''')
# # print(logAdd("2021/11/20", "Test", "logs"))
# # print(logRetrive())
# con.commit()
# closeConnection()
