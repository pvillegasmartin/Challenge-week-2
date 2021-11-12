import sqlite3 as sl
import pandas as pd
import pickle
import numpy as np
con = sl.connect('google_fit.db')
import datetime
#with con:
#    con.execute("""
#        CREATE TABLE USER (
#            id INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT,
#            name TEXT,
#            surname TEXT,
#            gender TEXT NOT NULL,
#            age INTEGER NOT NULL,
#            weight INTEGER NOT NULL,
#            height INTEGER NOT NULL,
#            mail TEXT NOT NULL UNIQUE,
#            password TEXT NOT NULL
#        );
#    """)
#with con:
#    con.execute(
#        """
#        CREATE TABLE DATA (
#            id INTEGER NOT NULL,
##            date datetime default current_timestamp,
#            walking INTEGER,
#           car INTEGER,
#            train INTEGER,
#            still INTEGER,
#            bus INTEGER
#        );
#        """
#    )
'''
a='Pepe'
#sql = f'INSERT INTO DATA (name, surname, age, weight, height, mail, password) values({a}, "Lopez", 20, 51, 165, pepito@gmail.com, pepito)'
con.executemany('INSERT INTO USER (name, surname, age, weight, height, mail, password) values(?, ?, ?, ?, ?, ?, ?)', [(a, "Lopez", 20, 51, 165, 'pepito@gmail.com', 'pepito')])

data = [
    (3, 1/1/2021, 20, 51, 165, 4, 6)
]

with con:
    con.executemany(sql, data)
with con:
    data = con.execute("SELECT * FROM DATA")
    
    for row in data:
        print()

registered = []
df = pd.read_sql_query("SELECT * FROM DATA", con)



a = pd.read_csv('test_U2.csv')
filename = 'finalized_model.sav'
model = pickle.load(open(filename, 'rb'))
y_pred = model.predict(a)
data_to_insert = [(1,datetime.datetime.now(),np.count_nonzero(y_pred == 0),np.count_nonzero(y_pred == 1),np.count_nonzero(y_pred == 2),np.count_nonzero(y_pred == 3),np.count_nonzero(y_pred == 4))]
con.executemany('INSERT INTO DATA (id, date, walking, car, train, still, bus) values(?, ?, ?, ?, ?, ?, ?)',
                data_to_insert)
con.commit()
a = pd.read_csv('test_U5.csv')
filename = 'finalized_model.sav'
model = pickle.load(open(filename, 'rb'))
y_pred = model.predict(a)
data_to_insert = [(1,datetime.datetime.now(),np.count_nonzero(y_pred == 0),np.count_nonzero(y_pred == 1),np.count_nonzero(y_pred == 2),np.count_nonzero(y_pred == 3),np.count_nonzero(y_pred == 4))]
con.executemany('INSERT INTO DATA (id, date, walking, car, train, still, bus) values(?, ?, ?, ?, ?, ?, ?)',
                data_to_insert)
con.commit()
a = pd.read_csv('test_U9.csv')
filename = 'finalized_model.sav'
model = pickle.load(open(filename, 'rb'))
y_pred = model.predict(a)
data_to_insert = [(1,datetime.datetime.now(),np.count_nonzero(y_pred == 0),np.count_nonzero(y_pred == 1),np.count_nonzero(y_pred == 2),np.count_nonzero(y_pred == 3),np.count_nonzero(y_pred == 4))]
con.executemany('INSERT INTO DATA (id, date, walking, car, train, still, bus) values(?, ?, ?, ?, ?, ?, ?)',
                data_to_insert)
con.commit()
a = pd.read_csv('test_U11.csv')
filename = 'finalized_model.sav'
model = pickle.load(open(filename, 'rb'))
y_pred = model.predict(a)
data_to_insert = [(1,datetime.datetime.now(),np.count_nonzero(y_pred == 0),np.count_nonzero(y_pred == 1),np.count_nonzero(y_pred == 2),np.count_nonzero(y_pred == 3),np.count_nonzero(y_pred == 4))]
con.executemany('INSERT INTO DATA (id, date, walking, car, train, still, bus) values(?, ?, ?, ?, ?, ?, ?)',
                data_to_insert)
con.commit()
'''
df_user = pd.read_sql_query("SELECT * FROM DATA", con)
print('a')

