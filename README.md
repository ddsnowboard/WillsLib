WillsLib
========

My library of python functions that I use often/like to have around, beginning with a set of mysqlite3 helper functions. 


######WillsLib.DBinsert(connection, table_name, vals)

Runs a sqlite3 "insert" command with the connection on the table name given. This is the name of the table within the .db file itself. `vals` is a list such that `vals[0]` is the first column, `vals[1]` is the second, and so on. Or, you can give `vals` as a dictionary in the form {`key:value}`


######WillsLib.DBselect(connection, table_name, columns, which)
	
Runs a sqlite3 "select" command with the given connection on the given `table_name`, selecting the given columns and returning an array of tuples containing the selected information. If you give `columns` as a string `'all'`, it will give you all the columns. If you want more than one column, give it as an array of strings. If you want only one, give it as an array of strings or a string. `which` is a dictionary in the format `{attribute:value}`, just like the others, or `'all'` to get all of the rows. If you give it a dictionary, it will only give you the rows whose values match the one(s) specified in the dictionary.  


######WillsLib.DBcreate(connection, table_name, columns)

Runs a sqlite3 "create" command with the given connection to create the given named table with the given columns. Columns are in an array of strings. 


######WillsLib.DBupdate(connection, table_name, set, which)

Updates the given attributes to the new ones in the "set" variable. Set and which are dictionaries, and they are in the format `{column:attribute}`. Set is what you want to change, and which is where you want to change it. If you wanted to change Zachary's address, you'd do this:
	
    DBupdate(connection, "table_name", {'address':'7278 Main St.'}, {'Name':'Zachary'})


You can also set all the table elements to have a certain attribute by passing 'all' to which instead of a dictionary. 
	
    DBupdate(connection, "hitlist", {"status":"dead"}, "all")


######WillsLib.DBdelete(connection, table_name, which)

Deletes the entries dictated by `which` in the given table, `table_name`. `which` is a dictionary in the format `{attribute:value}`, just like in DBupdate(). 
