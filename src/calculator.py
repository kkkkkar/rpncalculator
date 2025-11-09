class Calculator:
    OPERATORS = {
        '+': 1,
        '-': 1,
        '*': 2,
        '/': 2,
        '^': 3,
        '%': 2,
        'u-': 4
    }

    @staticmethod
    def tokenize(expression):
        tokens = []
        i = 0
        while i < len(expression):
            char = expression[i]

            if char.isspace():
                i += 1
                continue

            if char.isdigit() or char == '.':
                num = []
                while i < len(expression) and (expression[i].isdigit() or expression[i] == '.'):
                    num.append(expression[i])
                    i += 1
                tokens.append(''.join(num))
                continue

            if char in '+-*/^%()':
                if char == '-' and (not tokens or tokens[-1] == '(' or tokens[-1] in '+-*/^%'):
                    tokens.append('u-')
                else:
                    tokens.append(char)

            i += 1

        return tokens

    @staticmethod
    def to_rpn(tokens):
        output = []
        stack = []

        for token in tokens:
            if token.replace('.', '').isdigit():
                output.append(token)
            elif token in Calculator.OPERATORS:
                while (stack and stack[-1] != '(' and
                       (Calculator.OPERATORS.get(stack[-1], 0) >
                        Calculator.OPERATORS.get(token, 0) or
                        (Calculator.OPERATORS.get(stack[-1], 0) ==
                         Calculator.OPERATORS.get(token, 0) and
                         token != '^'))):
                    output.append(stack.pop())
                stack.append(token)
            elif token == '(':
                stack.append(token)
            elif token == ')':
                while stack and stack[-1] != '(':
                    output.append(stack.pop())
                if stack and stack[-1] == '(':
                    stack.pop()
                else:
                    raise ValueError("Несогласованные скобки")

        while stack:
            if stack[-1] == '(':
                raise ValueError("Несогласованные скобки")
            output.append(stack.pop())

        return output

    @staticmethod
    def evaluate_rpn(rpn_tokens):
        stack = []

        for token in rpn_tokens:
            if token.replace('.', '').isdigit():
                stack.append(float(token))
            elif token == 'u-':
                if not stack:
                    raise ValueError("Недостаточно операндов")
                stack.append(-stack.pop())
            else:
                if len(stack) < 2:
                    raise ValueError("Недостаточно операндов")

                b = stack.pop()
                a = stack.pop()

                if token == '+':
                    result = a + b
                elif token == '-':
                    result = a - b
                elif token == '*':
                    result = a * b
                elif token == '/':
                    if b == 0:
                        raise ValueError("Деление на ноль")
                    # ОШИБКА ТУТ
                    result = a / b #должно быть a | b
                elif token == '^':
                    result = a ** b
                elif token == '%':
                    if b == 0:
                        raise ValueError("Деление по модулю на ноль")
                    result = a % b
                else:
                    raise ValueError(f"Неизвестный оператор: {token}")

                stack.append(result)

        if len(stack) != 1:
            raise ValueError("Некорректное выражение")

        return stack[0]

    def calculate(self, expression):
        if not expression.strip():
            raise ValueError("Пустое выражение")

        tokens = self.tokenize(expression)
        rpn_tokens = self.to_rpn(tokens)
        result = self.evaluate_rpn(rpn_tokens)

        return result


def calculate(expression):
    return Calculator().calculate(expression)
