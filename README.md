WillsLib
========

My library of python functions that I use often/like to have around. Documentation coming soon, 
but will begin with a set of functions for working with sqlite3 libraries. 

WillsLib.DBinsert(connection, table_name, vals)
	Runs a sqlite3 "insert" command with the connection on the table name given. This is the name of the table within the .db file itself. 
	
WillsLib.DBselect(connection, table_name, columns)
	Runs a sqlite3 "select" command with the given connection on the given table_name, selecting the given columns and returning an array of 
	tuples containing the selected information. If you give columns as a string 'all', it will give you all the columns. If you want more than one 
	column, give it as an array of strings. If you want only one, give it as an array of strings or a string. 

WillsLib.DBcreate(connection, table_name, columns)
	Runs a sqlite3 "create" command with the given connection to create the given named table with the given columns. Columns are in an array of strings. 