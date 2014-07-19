from WillsLib import *
import sqlite3
db = sqlite3.connect('test.db')
c = db.cursor()
# DBinsert(db, 'test', ['Ames','Bink', 'Gruel', 'Dapper'])
print(DBselect(db, 'test', 'all'))
DBupdate(db, 'test', {'b':'boring'}, {'c':'Gruel'})
print("\n\n\n")
print(DBselect(db, 'test', 'all'))