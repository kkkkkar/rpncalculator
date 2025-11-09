import pytest
from src.calculator import Calculator, calculate


class TestTokenizer:

    def test_simple_numbers(self):
        calc = Calculator()
        assert calc.tokenize("123") == ["123"]
        assert calc.tokenize("12.34") == ["12.34"]

    def test_operators(self):
        calc = Calculator()
        assert calc.tokenize("1+2") == ["1", "+", "2"]
        assert calc.tokenize("1-2*3") == ["1", "-", "2", "*", "3"]

    def test_parentheses(self):
        calc = Calculator()
        assert calc.tokenize("(1+2)") == ["(", "1", "+", "2", ")"]

    def test_unary_minus(self):
        calc = Calculator()
        assert calc.tokenize("-5") == ["u-", "5"]
        assert calc.tokenize("1+-2") == ["1", "+", "u-", "2"]

    def test_spaces(self):
        calc = Calculator()
        assert calc.tokenize("1 + 2") == ["1", "+", "2"]


class TestRPNConversion:

    def test_simple_expression(self):
        calc = Calculator()
        tokens = calc.tokenize("1+2")
        rpn = calc.to_rpn(tokens)
        assert rpn == ["1", "2", "+"]

    def test_operator_precedence(self):
        calc = Calculator()
        tokens = calc.tokenize("1+2*3")
        rpn = calc.to_rpn(tokens)
        assert rpn == ["1", "2", "3", "*", "+"]

    def test_parentheses(self):
        calc = Calculator()
        tokens = calc.tokenize("(1+2)*3")
        rpn = calc.to_rpn(tokens)
        assert rpn == ["1", "2", "+", "3", "*"]


class TestRPNEvaluation:

    def test_simple_addition(self):
        calc = Calculator()
        result = calc.evaluate_rpn(["1", "2", "+"])
        assert result == 3

    def test_operations(self):
        calc = Calculator()
        assert calc.evaluate_rpn(["2", "3", "*"]) == 6
        assert calc.evaluate_rpn(["6", "2", "/"]) == 3
        assert calc.evaluate_rpn(["2", "3", "^"]) == 8

    def test_unary_minus(self):
        calc = Calculator()
        result = calc.evaluate_rpn(["5", "u-"])
        assert result == -5

    def test_division_by_zero(self):
        calc = Calculator()
        with pytest.raises(ValueError, match="Деление на ноль"):
            calc.evaluate_rpn(["1", "0", "/"])

    def test_division(self):
        # Этот тест упадет, потому что мы специально сделаем ошибку в коде
        calc = Calculator()
        # Мы ожидаем, что 6/2 = 3, но в коде ошибк
        assert calc.calculate("6/2") == 3


class TestIntegration:

    def test_simple_calculations(self):
        assert calculate("2+2") == 4
        assert calculate("3*4") == 12
        assert calculate("10/2") == 5

    def test_complex_expressions(self):
        assert calculate("(2+3)*4") == 20
        assert calculate("2+3*4") == 14

    def test_unary_operations(self):
        assert calculate("-5") == -5
        assert calculate("1+-2") == -1

    def test_error_cases(self):
        with pytest.raises(ValueError):
            calculate("1/0")
        with pytest.raises(ValueError):
            calculate("")
