import argparse


class Operation:
    def compute(self, **args):
        return


class Addition(Operation):

    def compute(self, a, b):
        return a + b


class Division(Operation):
    def compute(self, a, b):
        try:
            return b / a
        except ZeroDivisionError:
            print("Division by zero")


class Subtraction(Operation):
    def compute(self, a, b):
        return b - a


class Multiplication(Operation):
    def compute(self, a, b):
        return a * b


class Minus(Operation):
    def compute(self, a):
        return -a


class ReversePolishNotation:
    def __init__(self, expression):
        self.expression = expression
        self.stack = []
        self.output = []
        self.priority = {"+": 1, "-": 1, "/": 2, "*": 2, "(": 0, ")": 0, "u-": 3}
        self.operations = {"+": Addition, "-": Subtraction, "*": Multiplication,
                           "/": Division, "u-": Minus}

    def parse(self):
        parseexpr = [" "]
        for char in self.expression:
            if char.isdigit() or char in ".,":
                if parseexpr[-1][0].isdigit() or parseexpr[-1].endswith((".", ",")) or \
                        parseexpr[-1].startswith((".", ",")):
                    parseexpr[-1] += char
                else:
                    parseexpr.append(char)
            elif char == "(" and parseexpr[-1] == ")":
                parseexpr.append("*")
                parseexpr.append(char)
            elif char in '+-/*()':
                parseexpr.append(char)
            else:
                parseexpr.append(char)
        self.expression = parseexpr[1:]
        return self.expression

    def sort(self):
        self.parse()
        for i in range(len(self.expression)):
            if self.expression[i] == "-":
                if i == 0 or self.expression[i - 1] in self.operations.keys() \
                        or self.expression[i - 1] == "(":
                    self.expression[i] = "u-"
        for arg in self.expression:
            if arg in self.operations.keys():
                if self.stack:
                    if self.priority.get(arg) <= self.priority.get(self.stack[-1]):
                        p = self.stack.pop()
                        self.output.append(p)
                self.stack.append(arg)
            elif arg == "(":
                self.stack.append(arg)
            elif arg == ")":
                try:
                    while self.stack[-1] != "(":
                        p = self.stack.pop()
                        self.output.append(p)
                except IndexError:
                    print("Left bracket is not present, "
                          "it will be added to beginning of the expression")
                    self.stack.append("(")
                finally:
                    self.stack.pop()
            else:
                try:
                    self.output.append(int(arg))
                except ValueError:
                    try:
                        self.output.append(float(arg))
                    except ValueError:
                        print("Couldn't convert into int or float, "
                              "char will be replaced with 0 or 1")
                        if self.stack[-1] in ("+", "-", "u-"):
                            self.output.append(0)
                        elif self.stack[-1] in ("(", "*", "/", ")"):
                            self.output.append(1)
        while self.stack:
            popitem = self.stack.pop()
            self.output.append(popitem)
        return self.expression

    def compute(self):
        self.sort()
        for a in self.output:
            if a in self.operations.keys():
                op = self.operations.get(a)
                if op == Minus:
                    p1 = self.stack.pop()
                    p = op.compute(op, p1)
                else:
                    p1 = self.stack.pop()
                    p2 = self.stack.pop()
                    p = op.compute(op, p1, p2)
                self.stack.append(p)
            else:
                self.stack.append(a)
        result = self.stack.pop()
        print("Result:", result)
        return result


def arparser():
    parser = argparse.ArgumentParser()
    parser.add_argument('exp', type=str)
    return parser.parse_args()


if __name__ == '__main__':
    ar = arparser()
    r = ReversePolishNotation(ar.exp)
    r.compute()
