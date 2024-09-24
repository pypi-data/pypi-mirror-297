import unittest
from mageshbasiccalculator import Calculator, ScientificCalculator

class TestCalculator(unittest.TestCase):

    def setUp(self):
        self.calc = Calculator(10, 5)

    def test_add(self):
        self.assertEqual(self.calc.add(), 15)

    def test_subtract(self):
        self.assertEqual(self.calc.subtract(), 5)

    def test_multiply(self):
        self.assertEqual(self.calc.multiply(), 50)

    def test_divide(self):
        self.assertEqual(self.calc.divide(), 2.0)

    def test_divide_by_zero(self):
        self.calc = Calculator(10, 0)
        with self.assertRaises(ValueError):
            self.calc.divide()


class TestScientificCalculator(unittest.TestCase):

    def setUp(self):
        self.sci_calc = ScientificCalculator(2, 2)

    def test_add(self):
        self.assertEqual(self.sci_calc.add(), 5 , "incorrect addition")

    def test_power(self):
        self.assertEqual(self.sci_calc.power(), 8, "incorrect power")

if __name__ == '__main__':
    unittest.main()


