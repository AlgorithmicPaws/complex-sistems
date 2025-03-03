class TuringMachine:
    def __init__(self, tape):
        valid_chars = set("01+-*/%^r()= ")
        if any(char not in valid_chars for char in tape):
            raise ValueError("Error: La cinta contiene caracteres no permitidos.")
        
        self.tape = list(tape) + [' ']  # Agregar espacio en blanco al final
        self.head = 0
        self.state = 'q0'

    def move(self, direction):
        if direction == 'R':
            self.head += 1
        elif direction == 'L' and self.head > 0:
            self.head -= 1
    
    def read_symbol(self):
        return self.tape[self.head]
    
    def write_symbol(self, symbol):
        self.tape[self.head] = symbol
    
    def execute(self):
        while self.state != 'qf':
            symbol = self.read_symbol()
            
            if self.state == 'q0':
                if symbol in '01':
                    self.move('R')
                elif symbol in '+-*/%^r()':
                    self.move('R')
                elif symbol == '=':
                    self.calculate_result()
                    self.state = 'qf'
                elif symbol == ' ':
                    self.state = 'qf'

    def calculate_result(self):
        expression = ''.join(self.tape).strip()
        if '=' in expression:
            expression = expression.split('=')[0]
        
        result = self.evaluate_expression(expression)
        result_bin = bin(result)[2:]  # Convertir a binario sin prefijo '0b'
        self.tape = list(result_bin) + [' ']  # Sobreescribir la cinta
        self.head = 0

    def evaluate_expression(self, expression):
        postfix = self.infix_to_postfix(expression)
        return self.evaluate_postfix(postfix)

    def infix_to_postfix(self, expression):
        precedence = {'+': 1, '-': 1, '*': 2, '/': 2, '%': 2, '^': 3, 'r': 4}
        output = []
        stack = []
        buffer = ''
        
        for char in expression:
            if char in '01':
                buffer += char
            elif char == '(':
                stack.append(char)
            elif char == ')':
                if buffer:
                    output.append(int(buffer, 2))
                    buffer = ''
                while stack and stack[-1] != '(':
                    output.append(stack.pop())
                stack.pop()
            else:
                if buffer:
                    output.append(int(buffer, 2))
                    buffer = ''
                while stack and precedence.get(stack[-1], 0) >= precedence.get(char, 0):
                    output.append(stack.pop())
                stack.append(char)
        
        if buffer:
            output.append(int(buffer, 2))
        while stack:
            output.append(stack.pop())
        
        return output

    def evaluate_postfix(self, postfix):
        stack = []
        for token in postfix:
            if isinstance(token, int):
                stack.append(token)
            else:
                if token == 'r':
                    a = stack.pop()
                    stack.append(int(a ** 0.5))
                else:
                    b = stack.pop()
                    a = stack.pop()
                    if token == '+':
                        stack.append(a + b)
                    elif token == '-':
                        stack.append(a - b)
                    elif token == '*':
                        stack.append(a * b)
                    elif token == '/':
                        stack.append(a // b if b != 0 else 0)
                    elif token == '%':
                        stack.append(a % b if b != 0 else 0)
                    elif token == '^':
                        stack.append(a ** b)
        return stack[0] if stack else 0
    
    def get_tape(self):
        return ''.join(self.tape).strip()

# Ejemplos de uso:
#tape_input = "1100+101-11="  # (12 + 5 - 3) = 14 -> 1110
#tape_input = "((1001+11)%11)="  # (9+3)%3 = 0 -> 0
#tape_input = "((101+11)*10/10)="  # ((5+3)*2/2) = 8 -> 1000

tape_input = input("Ingrese la cinta: ")

tm = TuringMachine(tape_input)
tm.execute()
print("Resultado en la cinta:", tm.get_tape())
