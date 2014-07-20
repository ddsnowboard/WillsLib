from WillsLib import *
import sqlite3
db = sqlite3.connect('test.db')
c = db.cursor()
# DBinsert(db, 'test', ['Ames','Bink', 'Gruel', 'Dapper'])
print(DBselect(db, 'test', 'all'))
DBdelete(db, 'test', {'a':'alpha'})
print("\n\n\n")
print(DBselect(db, 'test', 'all'))