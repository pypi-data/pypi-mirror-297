# mageshbasiccalculator/scientific/scientific_calculator.py

from mageshbasiccalculator.basic.calculator import Calculator

class ScientificCalculator(Calculator):
    def power(self):
        return self.num1 ** self.num2
