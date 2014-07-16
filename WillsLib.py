import sqlite3
import tkinter as tk
from types import methodType
# Put main DB interface functions from tshirtPicker in here. Generalize them, and they'll be useful. 
# Also, use this: http://www.ianlewis.org/en/dynamically-adding-method-classes-or-class-instanc
def insert(DB_name, id, description, lasttime):
	# I need to figure out how to get a variable amount of arguments and then put them into this line below, in the parens. 
	# Yay. 
	cursor.execute("insert into ? VALUES (?, ?, ?);", (id, description, lasttime))
	db.commit()