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

######WillsLib.sanitize(string)

This is an attempt at sanitizing database inputs. If this were Java, it would probably be a private function, but it's not, so it isn't. It goes through a list of sqlite3 keywords and makes sure they're not in the input in a way that will cause problems, and either makes them safer or throws an error if it finds one.

######WillsLib.primes()

This will return a prime number generator, using the brute force method, with a slight optimization. 


######WillsLib.squares()

This returns a perfect square generator that is actually pretty fast. 

######*class* WillsLib.Equation(equation)

This returns an instance of the Equation object, made with the given equation in string form. It must have an equal sign. You can use either `^` or `**` for exponentiation. You can use any letter for the variable, but you must be consistent. 

######Equation methods:

+ Equation.evaluate(x)

  + This evaluates the equation for the given input. 

+ Equation.intersect(other)

  + Given another Equation, this finds the intersection of them if possible. It's not very robust, but it works sometimes. 

######WillsLib.myIndex(list, value, func = lambda x: x)

This is my own (probably slower) implementation of python's list.index() function. This allows you to set what aspect of each item you 
want to check, similar to the default list.sort() function. For example, if I want to find the first thing in a list that has a length 
of 5, I could say

```
WillsLib.myIndex(l, 5, len)
```

and it would return the index of that in the list. 


######WillsLib.tabsToList(input_list, output_filename, type = "ordered")

This takes a text file (or just a list of lines) that is indented with tabs and turns it into an HTML file that is indented with the given type (ordered or unordered) of HTML list. The formatting of the HTML isn't too pretty, so you might want to run it through a formatter, but it does work. 

######WillsLib.myRange(start, stop, step)

A version of range/xrange that returns a generator that goes from `start` (inclusive) to `stop` (exclusive) by `step` each time. It is not as fast as range/xrange, but it supports floats. 