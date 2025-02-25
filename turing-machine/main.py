class TuringMachine:
    def __init__(self, tape="", blank_symbol=" ", initial_state="", final_states=None, transition_function=None):
        self.tape = list(tape)
        self.blank_symbol = blank_symbol
        self.head_position = 0
        self.current_state = initial_state
        self.final_states = final_states if final_states is not None else set()
        self.transition_function = transition_function if transition_function is not None else {}

    def step(self):
        current_symbol = self.tape[self.head_position] if self.head_position < len(self.tape) else self.blank_symbol
        action = self.transition_function.get((self.current_state, current_symbol))

        if action:
            new_state, new_symbol, direction = action
            if self.head_position < len(self.tape):
                self.tape[self.head_position] = new_symbol
            else:
                self.tape.append(new_symbol)

            if direction == "R":
                self.head_position += 1
            elif direction == "L" and self.head_position > 0:
                self.head_position -= 1

            self.current_state = new_state

    def run(self):
        while self.current_state not in self.final_states:
            self.step()

    def get_tape(self):
        return ''.join(self.tape).strip()

    def process_expression(self):
        expression = self.get_tape()
        if '+' in expression:
            self.add()
        elif '-' in expression:
            self.subtract()
        elif '*' in expression:
            self.multiply()
        elif '/' in expression:
            self.divide()
        elif '%' in expression:
            self.modulo()
        elif '^' in expression:
            self.power()
        elif '√' in expression:
            self.square_root()
        else:
            self.tape = list("ERROR")
        self.current_state = 'HALT'

    def to_decimal(self, binary_str):
        return int(binary_str, 2)

    def to_binary(self, number):
        return bin(number)[2:]  # Eliminar el prefijo '0b'

    def add(self):
        numbers = self.get_tape().split('+')
        result = self.to_decimal(numbers[0]) + self.to_decimal(numbers[1])
        self.tape = list(self.to_binary(result))

    def subtract(self):
        numbers = self.get_tape().split('-')
        result = self.to_decimal(numbers[0]) - self.to_decimal(numbers[1])
        result = max(0, result)  # Evitar negativos
        self.tape = list(self.to_binary(result))

    def multiply(self):
        numbers = self.get_tape().split('*')
        result = self.to_decimal(numbers[0]) * self.to_decimal(numbers[1])
        self.tape = list(self.to_binary(result))

    def divide(self):
        numbers = self.get_tape().split('/')
        divisor = self.to_decimal(numbers[1])
        if divisor == 0:
            result = 'ERROR'
        else:
            result = self.to_decimal(numbers[0]) // divisor
            result = self.to_binary(result)
        self.tape = list(result)

    def modulo(self):
        numbers = self.get_tape().split('%')
        divisor = self.to_decimal(numbers[1])
        if divisor == 0:
            result = 'ERROR'
        else:
            result = self.to_decimal(numbers[0]) % divisor
            result = self.to_binary(result)
        self.tape = list(result)

    def power(self):
        numbers = self.get_tape().split('^')
        result = self.to_decimal(numbers[0]) ** self.to_decimal(numbers[1])
        self.tape = list(self.to_binary(result))

    def square_root(self):
        number = self.to_decimal(self.get_tape().replace('√', ''))
        result = int(number ** 0.5)
        self.tape = list(self.to_binary(result))


# 🔥 Ejecutar desde consola
if __name__ == "__main__":
    while True:
        expression = input("💻 Ingresa una operación en binario (o 'salir' para terminar): ")
        if expression.lower() == 'salir':
            print("👋 ¡Hasta luego!")
            break

        # Validación de binario
        valid_chars = {'0', '1', '+', '-', '*', '/', '%', '^', '√'}
        if not set(expression).issubset(valid_chars):
            print("❌ Solo se permiten números binarios y operadores válidos.")
            continue

        tm = TuringMachine(tape=expression)
        tm.process_expression()
        print("✅ Resultado en binario:", tm.get_tape())
