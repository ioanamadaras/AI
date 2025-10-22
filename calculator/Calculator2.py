class CalculatorException(Exception):
    '''Exception for calculator errors.'''
    pass


class Calculator(object):
    def read(self) :
        '''read input from stdin'''
        return input('> ')
    
    def loop(self):
        """read a line of input, evaluate and print it
        repeat the above until the user types 'quit'. """

        line = self.read()
        if (line == 'quit'):
            print('bye!')
            return
        
        result = self.eval(line)
        print(result)
        self.loop()

        
    def splitString(self, string: str):
        '''takes in a string and splits it into an array of numbers and operators'''
        arr = []
        current_num: str = ''
        operators = ['+', '-', '*', '/']
        separators = ['(', ')']
        
        cleanStr = string.replace(" ", "").replace("\t", "")
        
        def addCurrentNum():
            # Apelam arr.append(current_num) DOAR daca are 
            if (current_num != ""):
                arr.append(current_num)

        for char in cleanStr:
            if char in operators:
                addCurrentNum()
                arr.append(char)
                current_num = ""
            elif char in separators:
                addCurrentNum()
                arr.append(char)
                current_num = ""
            elif char.isdigit():
                current_num = current_num + char
            else:
                raise CalculatorException("Invalid character in expression")
        addCurrentNum()
        return arr
    
    def findPairParantesisIndex(self, startIndex: int, tokens: list[str]) -> int:
        level = 1
        for i in range(startIndex + 1, len(tokens)):
            char = tokens[i]
            if char == '(':
                level += 1
            elif char == ')':
                level -= 1

            if level == 0:
                return i

        raise CalculatorException("Invalid parenthesis placement!")

    def calculate(self, tokens: list[str]) -> float:
        """Evaluates tokens respecting operator precedence and parentheses."""

        def helper(tokens: list[str]) -> float:
            # Pasul 1: rezolvă parantezele
            i = 0
            while i < len(tokens):
                if tokens[i] == '(':
                    endIndex = self.findPairParantesisIndex(i, tokens)
                    innerValue = helper(tokens[i + 1:endIndex])
                    tokens = tokens[:i] + [str(innerValue)] + tokens[endIndex + 1:]
                    i = 0  # restart după modificare
                else:
                    i += 1

            # Pasul 2: rezolvă * și /
            i = 0
            while i < len(tokens):
                if tokens[i] in ('*', '/'):
                    left = float(tokens[i - 1])
                    right = float(tokens[i + 1])
                    if tokens[i] == '*':
                        result = left * right
                    else:
                        if right == 0:
                            raise CalculatorException("Division by zero")
                        result = left / right
                    tokens = tokens[:i - 1] + [str(result)] + tokens[i + 2:]
                    i = 0
                else:
                    i += 1

            # Pasul 3: rezolvă + și -
            i = 0
            while i < len(tokens):
                if tokens[i] in ('+', '-'):
                    left = float(tokens[i - 1])
                    right = float(tokens[i + 1])
                    result = left + right if tokens[i] == '+' else left - right
                    tokens = tokens[:i - 1] + [str(result)] + tokens[i + 2:]
                    i = 0
                else:
                    i += 1

            if len(tokens) != 1:
                raise CalculatorException("Invalid expression")

            return float(tokens[0])

        return helper(tokens)
    
    def eval(self, string: str) -> float | None:
        '''evaluates an infix arithmetic expression'''
        try: 
            numOrOperatorArr = self.splitString(string)
            # print(numOrOperatorArr)
            return self.calculate(numOrOperatorArr)

        except CalculatorException as e:
            print(f"Error: {e}")

        return None


if __name__ == '__main__':
    calc = Calculator()
    calc.loop()

    print("23 - 5 =", Calculator().eval("23 - 5"))
    print("5 - 4 =", Calculator().eval("5 - 4"))
    print("12 / 2 =", Calculator().eval("12 / 2"))
    print("4 * 3 =", Calculator().eval("4 * 3"))
    print("4 * 3 + 1 =", Calculator().eval("4 * 3 + 1"))
    print("4 * (3 + 1) =", Calculator().eval("4 * (3 + 1)"))
    print("(3 / 1 + 5) =", Calculator().eval("(3 / 1 + 5)"))
    # print("(INVALID): 13 / 0 =", Calculator().eval("13 / 0"))
    # print("(INVALID): 12 3 =", Calculator().eval("12 3"))

