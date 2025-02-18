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
