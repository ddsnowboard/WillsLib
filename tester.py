from WillsLib import *
import sqlite3
db = sqlite3.connect('test.db')
c = db.cursor()
# DBinsert(db, 'test', ['Ames','Bink', 'Gruel', 'Dapper'])
# DBinsert(db, 'test', ['Abel','Bink', 'Gruel', 'Dapper'])
# DBinsert(db, 'test', ['Aaron','Bink', 'Gabe', 'Drew'])
# DBinsert(db, 'test', ['Adam','Bink', 'Gruel', 'Dapper'])
print(DBselect(db, 'test', 'all', {'a':'Aaron', 'c':"Gabe"}))
print("\n\n\n")
print(DBselect(db, 'test', 'all', 'all'))