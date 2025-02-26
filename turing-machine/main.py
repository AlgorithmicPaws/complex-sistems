import re

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
        result = self.evaluate_expression(expression)
        if result is not None:
            self.tape = list(self.to_binary(result))
        else:
            self.tape = list("ERROR")
        self.current_state = 'HALT'

    def to_decimal(self, binary_str):
        return int(binary_str, 2)

    def to_binary(self, number):
        return bin(number)[2:]  # Eliminar el prefijo '0b'

    def evaluate_expression(self, expression):
        try:
            # Convierte números binarios a decimales y procesa paréntesis
            expression = self.handle_parentheses(expression)
            return expression
        except:
            return None

    def handle_parentheses(self, expression):
        # Busca y evalúa los paréntesis más internos primero
        while '(' in expression:
            inner_expr = re.search(r'\(([^()]+)\)', expression)
            if not inner_expr:
                return None  # Paréntesis mal formados

            inner_value = self.evaluate_simple_expression(inner_expr.group(1))
            if inner_value is None:
                return None

            # Sustituir la expresión evaluada en la cadena original
            expression = expression[:inner_expr.start()] + self.to_binary(inner_value) + expression[inner_expr.end():]

        # Evaluar la expresión sin paréntesis
        return self.evaluate_simple_expression(expression)

    def evaluate_simple_expression(self, expr):
        # Convierte binarios a decimales
        tokens = re.split(r'([+\-*/%^√])', expr)
        tokens = [self.to_decimal(token) if re.fullmatch(r'[01]+', token) else token for token in tokens]

        # Aplica operaciones según prioridad
        tokens = self.apply_operations(tokens, ['^', '√'])
        tokens = self.apply_operations(tokens, ['*', '/', '%'])
        tokens = self.apply_operations(tokens, ['+', '-'])

        return tokens[0] if tokens else None

    def apply_operations(self, tokens, operators):
        i = 0
        while i < len(tokens):
            if tokens[i] in operators:
                operator = tokens[i]
                if operator == '√':
                    operand = tokens[i + 1]
                    result = int(operand ** 0.5)
                    tokens[i:i + 2] = [result]
                else:
                    left = tokens[i - 1]
                    right = tokens[i + 1]
                    result = self.perform_operation(left, right, operator)
                    tokens[i - 1:i + 2] = [result]
                    i -= 1
            i += 1
        return tokens

    def perform_operation(self, left, right, operator):
        if operator == '+':
            return left + right
        elif operator == '-':
            return max(0, left - right)  # Evita negativos
        elif operator == '*':
            return left * right
        elif operator == '/':
            return left // right if right != 0 else 0
        elif operator == '%':
            return left % right if right != 0 else 0
        elif operator == '^':
            return left ** right
        else:
            return 0


# 🔥 Ejecutar desde consola
if __name__ == "__main__":
    while True:
        expression = input("💻 Ingresa una operación en binario con paréntesis (o 'salir' para terminar): ")
        if expression.lower() == 'salir':
            print("👋 ¡Hasta luego!")
            break

        # 🛠️ Elimina espacios antes de procesar la expresión
        expression = expression.replace(" ", "")

        # Validación de binario y caracteres permitidos
        valid_chars = {'0', '1', '+', '-', '*', '/', '%', '^', '√', '(', ')'}
        if not set(expression).issubset(valid_chars):
            print("❌ Solo se permiten números binarios, operadores válidos y paréntesis.")
            continue

        tm = TuringMachine(tape=expression)
        tm.process_expression()
        print("✅ Resultado en binario:", tm.get_tape())

#funciona con 2 expresiones