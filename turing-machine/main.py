import string

class TuringMachine:
    def __init__(self, tape):
        self.tape = list(tape) + [' ']
        self.head = 0
        self.state = 'q0'
    
    def run(self):
        if not self.is_valid_tape():
            print("Error: La cinta debe terminar con '=' para ejecutar la operación.")
            return
        
        self.convert_numbers_to_binary()
        self.execute()
    
    def is_valid_tape(self):
        """ Verifica que la cinta contenga '=' y que esté al final. """
        return '=' in self.tape and self.tape[-2] == '='
    
    def convert_numbers_to_binary(self):
        new_tape = []
        num = ""
        for char in self.tape:
            if char.isdigit():
                num += char
            else:
                if num:
                    new_tape.extend(list(bin(int(num))[2:]))  # Convertir número a binario
                    num = ""
                new_tape.append(char)
        self.tape = new_tape
    
    def execute(self):
        expression = "".join(self.tape).strip(" ")
        expression = expression.replace("=", "")  # Eliminar '=' para evaluar
        result = self.evaluate_expression(expression)

        # Verificar si el resultado es negativo
        if result < 0:
            print("Error: El resultado es negativo. No se puede representar en binario.")
            self.tape = ["Error"]
        else:
            result_bin = bin(result)[2:]  # Convertir resultado a binario
            self.tape = list(result_bin) + [' ']
        
        self.print_result()
    
    def evaluate_expression(self, expression):
        expression = expression.replace(" ", "")
        postfix = self.infix_to_postfix(expression)
        return self.evaluate_postfix(postfix)
    
    def infix_to_postfix(self, expression):
        precedence = {'+': 1, '-': 1, '*': 2, '/': 2, '^': 3, 'r': 3}
        output, stack = [], []
        num = ""
        for char in expression:
            if char in string.digits:
                num += char
            else:
                if num:
                    output.append(num)
                    num = ""
                if char in precedence:
                    while stack and precedence.get(stack[-1], 0) >= precedence[char]:
                        output.append(stack.pop())
                    stack.append(char)
                elif char == '(':  
                    stack.append(char)
                elif char == ')':  
                    while stack and stack[-1] != '(':
                        output.append(stack.pop())
                    stack.pop()
        if num:
            output.append(num)
        while stack:
            output.append(stack.pop())
        return output
    
    def evaluate_postfix(self, postfix):
        stack = []
        for token in postfix:
            if token.isdigit():
                stack.append(int(token, 2))
            else:
                b = stack.pop()
                a = stack.pop() if stack else 0
                if token == '+': stack.append(a + b)
                elif token == '-': stack.append(a - b)
                elif token == '*': stack.append(a * b)
                elif token == '/': stack.append(a // b)
                elif token == '^': stack.append(a ** b)
                elif token == 'r': stack.append(int(b ** 0.5))
        return stack[0] if stack else 0
    
    def print_result(self):
        if self.tape == ["Error"]:
            return
        result_bin = "".join(self.tape).strip()
        result_dec = int(result_bin, 2)
        print(f"Resultado en binario: {result_bin}")
        print(f"Resultado en decimal: {result_dec}")

    def get_tape(self):
        return "".join(self.tape).strip()


# Ejemplo de uso:
tape_input = input("Ingrese la cinta: ")

machine = TuringMachine(tape_input)
machine.run()

if machine.get_tape() != "Error":
    print("Resultado en la cinta:", machine.get_tape())
