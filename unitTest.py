import unittest
# So I can copy and paste to Newton'sMethod
import WillsLib as eqSolver
WillsLib = eqSolver
import sqlite3 as sql
from os import remove
class EquationSolverTest(unittest.TestCase):
    def test_RoundUp(self):
        """
        This tests the roundUp() function
        """
        self.assertEqual(eqSolver.roundUp(1.001), 2)
        self.assertEqual(eqSolver.roundUp(81.999), 82)
        self.assertEqual(eqSolver.roundUp(100.000001), 101)
    def test_ZeroDegree(self):
        """
        This makes sure that a zeroth-degree function runs properly.
        It didn't used to, so I thought I should have this test to make sure.
        """
        eqn = eqSolver.Equation("5^2")
        for i in range(1000):
            with self.subTest(number=i):
                self.assertEqual(eqn.evaluate(i), 5**2)
    def test_NormalEqn(self):
        """
        This should test for pretty much normal equations
        """
        eqn = eqSolver.Equation("x^2-5x+5")
        for i in range(1000):
            with self.subTest(number=i):
                self.assertEqual(eqn.evaluate(i), i**2-5*i+5)
    def test_Fractions(self):
        """
        This makes sure that the fraction functionality works.
        It took some extra logic, and I want to make sure that it is always right.
        """
        eqn = eqSolver.Equation("1/2x^2-5/8x+105/2")
        for i in range(1000):
            with self.subTest(number=i):
                self.assertEqual(eqn.evaluate(i), .5 * i ** 2 - 5 / 8 * i + 105 / 2)
    def test_FractionalExponents(self):
        """
        This tests if fractional exponents work. They don't by default, and I
        want to make sure that the extra code I included to make them work is
        right.
        """
        eqn = eqSolver.Equation("2x^1.5+x^1/2-x^5/3")
        for i in range(1000):
            with self.subTest(number=i):
                self.assertEqual(eqn.evaluate(i), 2 * i ** 1.5 + i ** .5 - i ** (5/3))
        eqn = eqSolver.Equation("1/2x^5/8")
        for i in range(1000):
            with self.subTest(number=i):
                self.assertEqual(eqn(i), .5 * i ** (5 / 8))
    def test_Spaces(self):
        """
        I needed to make sure that spaces are handled properly.
        """
        eqn = eqSolver.Equation("y = 2 x ^2 /  3- 23x   ^4- 3 3 x^4")
        for i in range(1000):
            with self.subTest(number=i):
                self.assertAlmostEqual(eqn(i), 2 * i ** (2/3) - 23 * i ** 4 - 33 * i ** 4, delta = 1) # The numbers are too big, so I have to use assertAlmostEqual.
    def test_Degree(self):
        """
        Makes sure that the degree counting functionality works.
        """
        s = ""
        for i in range(1, 50):
           with self.subTest():
               s += "+2x^{}".format(i)
        self.assertEqual(eqSolver.Equation(s).degree, i)
    def test_Dictionary(self):
        """
        Makes sure that the Equation constructor takes a dictionary properly.
        """
        d = {2:2, 1:-5, 0:3}
        eqn = eqSolver.Equation(d)
        for i in range(1000):
            with self.subTest(number=i):
                self.assertEqual(eqn(i), 2*i**2-5*i+3)
    def test_Zero(self):
        """
        Checks some things on the Equation.zero() function.
        """
        eqns = [(eqSolver.Equation("x^2-6x+9"), (3.0, 3.0)), (eqSolver.Equation("x^2"), (0.0, 0.0)), (eqSolver.Equation("x^2-2x-15"), (-3.0, 5.0)), (eqSolver.Equation("x^2+x+15"), None)]
        for i, j in eqns:
            with self.subTest(equation=i):
                self.assertEqual(i.zero(), j)
        eq = eqSolver.Equation("5x")
        with self.subTest(equation=eq):
            with self.assertRaises(eqSolver.ZeroError):
                eq.zero()
        eq = eqSolver.Equation("x^2-2x^.5+4x")
        with self.subTest(equation=eq):
            with self.assertRaises(eqSolver.ZeroError):
                print(eq.zero())
class DatabaseTest(unittest.TestCase):
    file_name = "unitTest.db"
    table_name = "TABLE_TEST"
    column_names = ["A", "B", "C"]
    def setUp(self):
        """
        Starts up database and opens up connection for other tests. 
        Inserts a few rows to for testing of select function. 
        """
        self.connection = sql.connect(self.file_name)
        c = self.connection.cursor()
        c.execute("create table {} ({})".format(self.table_name, ",".join(self.column_names)))
        self.connection.commit()
        self.test_rows = [("apples", "broccoli", "carrots"), ("apes", "bears", "cougars")]
        for i in self.test_rows:
            c.execute("insert into {} VALUES ('{}')".format(self.table_name, "','".join(i)))
        self.connection.commit()
    def tearDown(self):
        """
        Cleans out directory and closes everything. 
        """
        self.connection.close()
        remove(self.file_name)
    def test_DBinsert(self):
        """
        Tests the DBinsert() function of WillsLib
        """
        test_values = [("audi", "bmw", "cadillac"), ("amperstand", "bang", "comma"), ("alligator", "bear", "cat"), ("Anglo-saxon", "Belarusan", "Croatian"),
                {DatabaseTest.column_names[0]:"Arrhenious", DatabaseTest.column_names[1]:"base", DatabaseTest.column_names[2]:"chemistry"}]
        c = self.connection.cursor()
        for i in test_values:
            with self.subTest(values=i, type=type(i)):
                WillsLib.DBinsert(self.connection, self.table_name, i)
                # This would be unsafe, but this is just a unit test and I have a pretty good idea if what the inputs will be. 
                # Set up something so that it checks and if the input is a dictionary, it does this dictionary style. 
                # or, better yet, think of a properly elegant solution
                if type(i) == type(()):
                    c.execute("select * from {name} where a = '{l[0]}' and b = '{l[1]}' and c = '{l[2]}'".format(name=self.table_name, l=i))
                    self.assertEqual(c.fetchone(), i)
                elif type(i) == type({}):
                    c.execute("select * from {name} where a = '{colone}' and b = '{coltwo}' and c = '{colthree}'".format(name=self.table_name, 
                        colone=i[self.column_names[0]],
                        coltwo=i[self.column_names[1]],
                        colthree=i[self.column_names[2]]))
                    self.assertEqual(c.fetchone(), tuple(sorted(i.values())))
if __name__ == "__main__":
    unittest.main()
