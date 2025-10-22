class CalculatorException(Exception):
    '''Exception for calculator errors.'''
    pass


class Calculator(object):
    def read(self) :
        '''read input from stdin'''
        return input('> ')
    
    def formatResult(self, result: float) -> str:
        '''remove unnecessary decimal places'''
        if result.is_integer():
            return str(int(result))
        else:
            return str(result)
    
    def loop(self):
        """read a line of input, evaluate and print it
        repeat the above until the user types 'quit'. """

        while True:
            line = self.read()
            if (line == 'quit'):
                print('bye!')
                return
            
            result = self.formatResult(self.eval(line))
            print(result)

        
    def splitString(self, string: str):
        '''takes in a string and splits it into an array of numbers and operators'''
        arr = []
        current_num: str = ''
        operators = ['+', '-', '*', '/']
        separators = ['(', ')']
        
        cleanStr = string.replace(" ", "").replace("\t", "")
        
        if not cleanStr:
            raise CalculatorException("Empty expression")

        def addCurrentNum():
            # Apelam arr.append(current_num) DOAR daca are un nr in el 
            if (current_num != ""):
                arr.append(current_num)

        i = 0
        while i < len(cleanStr):
            char = cleanStr[i]
            
            if char == '-' and (i == 0 or cleanStr[i-1] in operators + ['(']):
                current_num = '-' #inseamna ca avem nr negativ 
                i += 1
                continue # ne intoarcem la while la urm char
            
            if char in operators:
                addCurrentNum()
                arr.append(char)
                current_num = ""
            elif char in separators:
                addCurrentNum()
                arr.append(char)
                current_num = ""
            elif char.isdigit() or char == '.': 
                current_num = current_num + char
            else:
                raise CalculatorException(f"Invalid character in expression: '{char}'")
            
            i += 1
            
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

    def addPrecedenceParentheses(self, tokens: list[str]) -> list[str]:
        result = tokens.copy()

        while True:
            found = False
            i = 0
            
            while i < len(result):
                token = result[i]
                if token in ['*', '/']:
                    left_idx = i - 1
                    if left_idx >= 0 and result[left_idx] == ')':
                        paren_depth = 1
                        left_idx -= 1
                        while left_idx >= 0 and paren_depth > 0:
                            if result[left_idx] == ')':
                                paren_depth += 1
                            elif result[left_idx] == '(':
                                paren_depth -= 1
                            left_idx -= 1
                        left_idx += 1

                    right_idx = i + 1
                    if right_idx < len(result) and result[right_idx] == '(':
                        paren_depth = 1
                        right_idx += 1
                        while right_idx < len(result) and paren_depth > 0:
                            if result[right_idx] == '(':
                                paren_depth += 1
                            elif result[right_idx] == ')':
                                paren_depth -= 1
                            right_idx += 1
                        right_idx -= 1

                    if left_idx > 0 and result[left_idx-1] == '(' and right_idx+1 < len(result) and result[right_idx+1] == ')':
                        i += 1
                        continue # deja in paranteze - sarim peste el 
 
                    if left_idx >= 0 and right_idx < len(result):
                        result = result[:left_idx] + ['('] + result[left_idx:right_idx+1] + [')'] + result[right_idx+1:]
                        found = True
                        break
                i += 1

            if not found:
                break

        return result


    def calculate(self, tokens: list[str]) -> int:
        if not tokens or len(tokens) == 0:
            raise CalculatorException("Empty expression in calculation")
        
        if ('(' in tokens):
            startIndex = tokens.index('(')
            endIndex = self.findPairParantesisIndex(startIndex, tokens)

            if (startIndex == 0 and endIndex == len(tokens) - 1): 
                return self.calculate(tokens[1:endIndex]) #daca parantezele sunt pe toata expresia, le eliminam si continuam

            innerValue = self.calculate(tokens[startIndex + 1 : endIndex]) # de la startIndex + 1 (inclusiv) pana la endIndex (exclusiv)
            newTokens = tokens[:startIndex] + [str(innerValue)] + tokens[endIndex + 1:]
            return self.calculate(newTokens)

        if len(tokens) == 1:
            try:
                return float(tokens[0])
            except ValueError:
                raise CalculatorException(f"Invalid number '{tokens[0]}'")
        
        
        tkLen = len(tokens)
        lastElem = tokens[tkLen - 1]
        stlElem = tokens[tkLen - 2] # Second To Last (penultim)

        try:
            lastValue = float(lastElem) #ultimul element nu poate fi paranteza pentru ca am tratat cazul de mai sus  
        except ValueError:
            raise CalculatorException(f"Invalid number '{lastElem}'")

        if (stlElem == '*'):
            return self.calculate(tokens[:-2]) * lastValue
        elif (stlElem == '/'):
            if float(lastValue) == 0.0:
                raise CalculatorException("Invalid division by 0")
            return self.calculate(tokens[:-2]) / lastValue
        elif (stlElem == '-' ):
            return self.calculate(tokens[:-2]) - lastValue
        elif (stlElem == '+'):
            return self.calculate(tokens[:-2]) + lastValue
    
    def eval(self, string: str) -> int | None:
        '''evaluates an infix arithmetic expression'''
        try: 
            numOrOperatorArr = self.splitString(string)
            numOrOperatorArr = self.addPrecedenceParentheses(numOrOperatorArr) # paranteze extra pt ordinea * si / 
            return self.calculate(numOrOperatorArr)

        except CalculatorException as e:
            print(f"Error: {e}")

        return None


if __name__ == '__main__':
    calc = Calculator()
    calc.loop()

    # print("-> Unit tests")
    # print("23 - 5 =", calc.eval("23 - 5"))
    # print("5 - 4 =", calc.eval("5 - 4"))
    # print("12 / 2 =", calc.eval("12 / 2"))
    # print("4 * 3 =", calc.eval("4 * 3"))
    # print("2 * 4 * 3 + 1 =", calc.eval("2 * 4 * 3 + 1"))
    # print("4 * (-3 - 1) =", calc.eval("4 * (-3 - 1)"))
    # print("4 * (100 - 9 * 10) =", calc.eval("4 * (100 - 9 * 10)"))
    # print("3 / 1 + 5 =", calc.eval("3 / 1 + 5"))
    # print("12 * (3 - 1 + 5) - (10 * (4 - 2)) / 4 =", calc.eval("12 * (3 - 1 + 5) - (10 * (4 - 2)) / 4"))
    # print("(INVALID): 13 / 0 =", calc.eval("13 / 0"))