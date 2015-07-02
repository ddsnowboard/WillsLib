#! /usr/bin/env python3
import sqlite3
import re
from collections import defaultdict
import math
from fractions import Fraction
def sanitize(string):
    WORD_LIST = ['ABORT', 'ACTION', 'ADD', 'AFTER', 'ALL', 'ALTER', 'ANALYZE', 'AND', 'AS', 'ASC', 'ATTACH', 'AUTOINCREMENT', 'BEFORE', 'BEGIN', 'BETWEEN', 'BY', 'CASCADE', 'CASE', 'CAST', 'CHECK', 'COLLATE', 'COLUMN', 'COMMIT', 'CONFLICT', 'CONSTRAINT', 'CREATE', 'CROSS', 'CURRENT_DATE', 'CURRENT_TIME', 'CURRENT_TIMESTAMP', 'DATABASE', 'DEFAULT', 'DEFERRABLE', 'DEFERRED', 'DELETE', 'DESC', 'DETACH', 'DISTINCT', 'DROP', 'EACH', 'ELSE', 'END', 'ESCAPE', 'EXCEPT', 'EXCLUSIVE', 'EXISTS', 'EXPLAIN', 'FAIL', 'FOR', 'FOREIGN', 'FROM', 'FULL', 'GLOB', 'GROUP', 'HAVING', 'IF', 'IGNORE', 'IMMEDIATE', 'IN', 'INDEX', 'INDEXED', 'INITIALLY', 'INNER', 'INSERT', 'INSTEAD', 'INTERSECT', 'INTO', 'IS', 'ISNULL', 'JOIN', 'KEY', 'LEFT', 'LIKE', 'LIMIT', 'MATCH', 'NATURAL', 'NO', 'NOT', 'NOTNULL', 'NULL', 'OF', 'OFFSET', 'ON', 'OR', 'ORDER', 'OUTER', 'PLAN', 'PRAGMA', 'PRIMARY', 'QUERY', 'RAISE', 'RECURSIVE', 'REFERENCES', 'REGEXP', 'REINDEX', 'RELEASE', 'RENAME', 'REPLACE', 'RESTRICT', 'RIGHT', 'ROLLBACK', 'ROW', 'SAVEPOINT', 'SELECT', 'SET', 'TABLE', 'TEMP', 'TEMPORARY', 'THEN', 'TO', 'TRANSACTION', 'TRIGGER', 'UNION', 'UNIQUE', 'UPDATE', 'USING', 'VACUUM', 'VALUES', 'VIEW', 'VIRTUAL', 'WHEN', 'WHERE', 'WITH', 'WITHOUT']
    for i in WORD_LIST:
        if ' ' + i.lower() + ' ' in string.lower() or ', '+i.lower() in string.lower() or string.lower() == i.lower():
            if i == 'DROP':
                raise Exception("You should not have used \"Drop\" in your input. Please use a different word")
            else:
                string = string.lower().replace(i.lower(),"'"+i.lower()+"'")
    return string
def DBinsert(connection, table_name, vals):
   DICT_STATEMENT = "insert into {table_name}({keys}) VALUES ({slots});"
   LIST_STATEMENT = "insert into {table_name} VALUES ({slots});"
   if type(vals) == type({}):
        s = DICT_STATEMENT.format(table_name=sanitize(table_name), keys=",".join(((sanitize(i) for i in vals.keys()))), slots=",".join(("?" for i in vals.values())))
        connection.cursor().execute(s, tuple(vals.values()))
   else:
        s = LIST_STATEMENT.format(table_name=sanitize(table_name), slots=','.join(("?" for i in vals)))
        connection.cursor().execute(s, tuple(vals))
        connection.commit()
def DBselect(connection, table_name, columns, which):
    out = []
    if columns == 'all':
        columns = ['*']
    elif type(columns) == str:
        columns = [columns]
    else:
        for i, j in enumerate(columns):
            columns[i] = sanitize(str(j))
    if which == 'all':
        for i in connection.cursor().execute('select %s from %s;' % (','.join(columns),sanitize(table_name))):
            out.append(i)
    else:
        strings = [sanitize(i) + " = ?" for i in which.keys()]
        for i in connection.cursor().execute("select %s from %s WHERE %s" % (','.join(columns), sanitize(table_name), ' and '.join(strings)), tuple([i for i in which.values()])):
            out.append(i)
    return out
def DBcreate(connection, table_name, columns):
    s = 'create table '+sanitize(table_name)+'('
    s+= ', '.join([sanitize(i) for i in columns])
    s+=');'
    print(s)
    connection.cursor().execute(s)
    connection.commit()
def DBupdate(connection, table_name, set, which):
    # Set and which will be dictionaries that have the syntax {column: value}
    # "Which" could also be the string "all"
    if not set:
        raise Exception("""You didn't give the right parameters!\nYou need
                         to give 2 dictionaries, \"set\" and \"which\", that\n
                         are in the format {attribute:value}. See the \n
                         documentation for more details.""")
    elif not which:
        raise Exception("""You didn't give the right parameters!\nYou need
                         to give 2 dictionaries, \"set\" and \"which\", that\n
                         are in the format {attribute:value}. See the \n
                         documentation for more details.\n
                         If you want to select all and change, use\n
                         which='all'""")
    strings = []
    for i in set.keys():
        strings.append(sanitize(str(i)) + ' = ?')
    if which == 'all':
        connection.cursor().execute("update " + sanitize(table_name) + " SET " + ', '.join(strings), tuple([j for j in set.values()]))
        connection.commit()
    else:
        params = []
        for i in which.keys():
            params.append(sanitize(str(i))+' = ?')
        connection.cursor().execute("update " + table_name + " SET "+', '.join(strings)+" WHERE "+' and '.join(params), tuple([j for j in set.values()] + [i for i in which.values()]))
    connection.commit()
def DBdelete(connection, table_name, which):
    if which == 'all':
        connection.cursor().execute("delete from %s" % sanitize(table_name))
        db.commit()
        return
    strings = [sanitize(i) + " = ?" for i in which.keys()]
    connection.cursor().execute("delete from " + sanitize(table_name) + " WHERE " + ' and '.join(strings), tuple([i for i in which.values()]))
    connection.commit()
# A generator that will generate perfect squares forever.
def squares():
    out = 1
    odd = 3
    while True:
        yield out
        out += odd
        odd += 2
def primes():
    """
    This generator will kick out primes forever, given enough memory and time.
    """
    yield 2
    prime = True
    out = 3
    while True:
        prime = True
        for i in range(2, int(math.sqrt(out))+1):
            if out %i ==0:
                prime = False
        if prime:
            yield out
        out += 2
# This is a class for polynomial equations. Give it the equation as a string, and you can evaluate it and maybe find the intersection
# with another line.
def roundUp(i):
    """
    I'm sure this is unnecessary, but I apparently couldn't find a good way to
    do it in the standard library, so I have this.
    """
    if i % 1 > 0:
        return int(i)+1
    return i
class ZeroError(Exception):
    pass
class Equation:
    """
    This is an object that represents a polynomial equation.
    It isn't terribly extensible, so you have to be careful what
    you give it. It will take decimals and fractions as coefficients,
    and in exponents.
    """
    def __init__(self, eq):    # y=2x^2-3x+5
    # If the equation is already a string, we have to turn it into an Equation
    # object.
        if type(eq) == type(""):
            eq = eq.replace(" ", "")
            # "normal" is an exponent greater than 1. "first" is an exponent of
            # 1.
            self.regexes = {"normal"   : re.compile(r"(?P<number>[\+-]?([\d\./])*)?[A-Za-z][\^](?P<exponent>[0-9/.]+)"),
                            "constant" : re.compile(r"^[\+-]?[\d/^]+$"),
                            "first"    : re.compile(r"(?P<number>[\+-]?[\d\./]*)?[A-Za-z]")}

            self.coefficients = defaultdict(float)
            self.eq = re.subn(r"^y=|=y$", '', eq)[0]   # 2x^2-3x+5
            # Add in spaces for later.
            self.eq = self.eq.replace("**", "^").replace("+", " +").replace("-", ' -')  # 2x^2 -3x +5
            self.terms = self.eq.split(" ")     # "2x^2", "-3x", "+5"
            self.terms = [i for i in self.terms if i != '']
            for i in self.terms:
                if self.regexes['constant'].match(i):
                    self.coefficients[0] += eval(i.replace("^", "**"))  # "+5"
                elif self.regexes['normal'].match(i):
                    match = self.regexes['normal'].match(i)
                    # If there is a number part on the term and it isn't just a
                    # plus sign (either a minus sign or an actual number)
                    if match.group("number") and match.group("number") != '+':
                        if match.group("number") == "-":
                            self.coefficients[Fraction(match.group("exponent"))] -= 1
                        else:
                            self.coefficients[Fraction(match.group("exponent"))] += Fraction(match.group("number"))
                    else:
                        # If the number is just a plus sign, make it one.
                        self.coefficients[Fraction(match.group("exponent"))] += 1
                elif self.regexes["first"].match(i):
                    match = self.regexes["first"].match(i)
                    if match.group("number") and match.group("number") != "+":
                        if match.group("number") == '-':
                            self.coefficients[1] -= 1
                        else:
                            self.coefficients[1] += Fraction(match.group('number'))      #"-3"
                    else:
                        self.coefficients[1] += 1
        elif type(eq) == type({}):
            # If our input is a dictionary, make that dictionary the coefficients
            # dictionary and be done.
            self.coefficients = defaultdict(float)
            for i, j in eq.items():
                self.coefficients[i] = j
        self.degree = max(self.coefficients.keys())
    def evaluate(self, x):
        """
        This function simply evaluates the Equation. You cal also use
        the __call__ function (eqn(x)).
        It goes through the coefficients dictionary and adds up all the
        terms.
        """
        end = 0
        for i, j in self.coefficients.items():
            try:
                end+=j*x**i
            except ZeroDivisionError:
                raise Exception("I had to divide by zero.")
        return end
    def zero(self):
        """
        This will find the zero of a quadratic function using the quadratic
        equation.
        I could implement a way to find it numerically for other
        types, but maybe another time.
        """
        if not self.isQuadratic():
            raise ZeroError("This function isn't quadratic")
        a = self.coefficients[2]
        b = self.coefficients[1]
        c = self.coefficients[0]
        try:
            return tuple(sorted(((-1 * b + math.sqrt(b**2 - 4 * a * c)) / (2 * a), (-1 * b - math.sqrt(b**2 - 4 * a * c)) / (2 * a))))
        except ValueError:
            return None
    def intersect(self, other):
        """
        This function finds the intersection of two equations.
        It returns a tuple of the form (x, y), or a boolean if the functions are
        the same or will never intersect.
        """
        if not type(other) == type(Equation("5")):
            raise Exception("Arguments {}, {} don't match Equation, Equation".format(type(self), type(other)))
            return
        # Left will be variables; right will be constants.
        # Left starts as self, right starts as other.
        left = defaultdict(float)
        right = 0
        # Go through the left hand function (self) and move all the constants to
        # the right and leave the variables on the left.
        for i, j in self.coefficients.items():
            if i == 0:
                right-=j
            else:
                left[i]+=j
        # Then do the same on the right.
        for i, j in other.coefficients.items():
            if i == 0:
                right+=j
            else:
                left[i]-=j
        if self.degree == 0 and other.degree == 0:
            return right == 0
        elif self.degree <= 1 and other.degree <= 1 :
            return (right/left[1], self.evaluate(right/left[1]))
        # Runs the quadratic equation if a degree is two.
        elif self.degree == 2 or other.degree == 2:
            return (((-1*left[1]+math.sqrt(left[1]**2-4*(left[2])*(-1*right)))/(2*left[2]), self.evaluate((-1*left[1]+math.sqrt(left[1]**2-4*(left[2])*(-1*right)))/(2*left[2]))), ((-1*left[1]-math.sqrt(left[1]**2-4*(left[2])*(-1*right)))/(2*left[2]), self.evaluate((-1*left[1]-math.sqrt(left[1]**2-4*(left[2])*(-1*right)))/(2*left[2]))))
        else:
            raise Error("I really can't get an accurate intersection with just this data.")
    def __str__(self):
        out = ""
        sortedDict = OrderedDict(sorted(self.coefficients.items(), key=lambda x: -1*abs(x[0])))
        for degree, number in sortedDict.items():
            if number == 0:
                continue
            elif degree == 0:
                out+= ('+' if number > 0 else "") + str(number)
            elif number == 1 and degree == 1:
                out+= '+x'
            elif number == -1 and degree == 1:
                out += '-x'
            elif degree == 1:
                out += "{}{}x".format(('+' if number > 0 and degree != self.degree else ''), number)
            else:
                out+="{}{}x^{}".format(('+' if number > 0 and degree != self.degree else ""),str(number),str(degree))
        return out
    def derivative(self):
        new = {}
        for i, j in self.coefficients.items():
            new[i-1] = j*i if i != 0 else 0
        return Equation(new)
    def isQuadratic(self):
        POSSIBLE_DEGREES = [0, 1, 2]
        if self.degree != 2:
            return False
        for i in self.coefficients.keys():
            if not i in POSSIBLE_DEGREES:
                return False
        return True
    def __eq__(self, other):
        if self.degree == other.degree:
            if self.coefficients == other.coefficients:
                return True
        return False
    def __ne__(self, other):
        return not self.__eq__(self, other)
    def __bool__(self, other):
        return self == Equation("0")
    def __getitem__(self, key):
        return self.coefficients[key]
    def __setitem__(self, key, value):
        self.coefficients[key] = value
    def __call__(self, x):
        return self.evaluate(x)
def myIndex(l, value, func = lambda x: x):
    for i, j in enumerate(l):
        if func(j) == value:
            return i

def tabsToList(input_list, output_filename, type = "ordered"):
    with open(output_filename, "w") as w:
        tabs = lambda x: x.count("\t")
        if type == "ordered":
            tag = ["<ol>", "</ol>"]
        elif type == "unordered":
            tag = ["<ul>", "</ul>"]
        # In case they give it to me as a file.
        l = list(input_list)
        depth = 0
        w.write("<html>{}".format(tag[0]))
        for n, i in enumerate(l):
            if tabs(i) > depth:
                w.write(tag[0])
            elif tabs(i) < depth:
                for p in range(depth - tabs(i)):
                    w.write("{}</li>".format(tag[1]))
            w.write("<li>{}".format(i))
            if tabs(i) < depth:
                for p in range(tabs(i)-depth):
                    w.write(tag[1])
            depth = tabs(i)
def myRange(start, stop, step = 1):
    yield start
    out = start + step
    while out < stop:
        yield out
        out += step
def euler(f, x, x0, y0, h):
    currx = x0
    curry = y0
    while currx < x:
        curry = curry + f(currx, curry)*h
        currx += h
    return curry
def eulerTable(f, x, x0, y0, h, mainloop):
    import tkinter as tk
    root = tk.Tk()
    class EulerRow(tk.Frame):
        def __init__(self, master, *args):
            tk.Frame.__init__(self, master)
            self.master = master
            for i in args:
                box = tk.Entry(self, width=5)
                box.insert(0, i)
                box.config(state='readonly')
                box.pack(side="left")
    currx = x0
    curry = y0
    EulerRow(root, 'x', 'y', 'F(x, y)', 'Δx', 'Δy').pack()
    EulerRow(root, currx, curry, f(currx, curry), h, f(currx, curry) * h).pack()
    while currx < x:
        curry = curry + f(currx, curry) * h
        currx += h
        EulerRow(root, currx, curry, f(currx, curry), h, f(currx, curry) * h).pack()
    if mainloop:
        root.mainloop()
def factors(integer):
    if integer % 1 != 0:
        raise Exception("{} is not an integer!".format(integer))
    out = {}
    curr = integer
    i = 1
    while curr != 1:
        i += 1
        if curr % i == 0:
            out[int(i)] = True
            out[int(curr/i)] = True
        elif i > integer / 2:
            if not out:
                return []
            else:
                return sorted([i for i, j in out.items() if j])
class PrimeFactorizer:
    def __init__(self):
        self.primes = []
        self.prime_generator = primes()
        self.primes.append(next(self.prime_generator))
    def factorize(self, number):
        out = []
        current_number = number
        # I have to do this weird for loop thing because I'm changing the length of the
        # list as I go.
        counter = 0
        while True:
            if current_number in self.primes:
                out.append(current_number)
                return sorted(out)
            elif current_number == 1:
                return sorted(out)
            if len(self.primes) == counter and number not in self.primes:
                self.primes.append(next(self.prime_generator))
            if current_number % self.primes[counter] == 0:
                out.append(self.primes[counter])
                current_number /= self.primes[counter]
                counter = 0
            else:
                counter += 1
