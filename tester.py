from WillsLib import *
import sqlite3
db = sqlite3.connect('test.db')
c = db.cursor()
DBinsert(db, 'test', ['alpha','beta', 'gamma', 'delta'])
print(DBselect(db, 'test', 'all'))
DBcreate(db, 'test1', ['red', 'green','blue'])