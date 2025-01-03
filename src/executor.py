import inspect

from bindings import Bindings


class UnknownSubroutine(Exception):
    pass


class InvalidMemoryAddressException(Exception):
    pass


class ImperivmExecutor:
    def __init__(self, ast):
        self.subroutines = {}
        self.stack = []
        self.heap = []
        for _, (_, identifier), block in ast:
            self.subroutines[identifier] = block

        self.operations = {
            "add": self.instruction_add,
            "subtract": self.instruction_subtract,
            "multiply": self.instruction_multiply,
            "divide": self.instruction_divide,
            "and": self.instruction_and,
            "or": self.instruction_or,
            "xor": self.instruction_xor,
            "negate": self.instruction_negate,
            "not": self.instruction_not,
            "if": self.instruction_if,
            "while": self.instruction_while,
            "exit": lambda args, bindings: exit(self.resolve_value(args[0], bindings)),
            "print": lambda args, bindings: print(self.resolve_value(args[0], bindings)),
            "push": self.instruction_push,
            "pop": self.instruction_pop,
            "invocation": self.instruction_invocation,
            "stop": lambda: True,
            "store": self.instruction_store,
            "load": self.instruction_load,
        }

    def execute_block(self, block, bindings: Bindings):
        for instruction in block:
            stop = self.execute_instruction(instruction, bindings)
            if stop:
                return True

    def execute_instruction(self, instruction, bindings: Bindings):
        operation, *args = instruction

        if operation not in self.operations:
            print("Error: invalid operation", operation)
            return False

        func = self.operations[operation]
        num_args = len(inspect.signature(func).parameters)
        if callable(func):
            if num_args:
                return func(args, bindings) if num_args == 2 else func(args)
            else:
                return func

    def instruction_add(self, args, bindings):
        ((_, target),) = args
        current = self.stack.pop()
        old = bindings.resolve(target)
        bindings.assign(target, old + current)

    def instruction_subtract(self, args, bindings):
        ((_, target),) = args
        current = self.stack.pop()
        old = bindings.resolve(target)
        bindings.assign(target, old - current)

    def instruction_multiply(self, args, bindings):
        ((_, target),) = args
        current = self.stack.pop()
        old = bindings.resolve(target)
        bindings.assign(target, old * current)

    def instruction_divide(self, args, bindings):
        ((_, target),) = args
        current = self.stack.pop()
        old = bindings.resolve(target)
        bindings.assign(target, old // current)

    def instruction_and(self, args, bindings):
        ((_, target),) = args
        argument = self.stack.pop()
        old = bindings.resolve(target)
        bindings.assign(target, old & argument)

    def instruction_or(self, args, bindings):
        ((_, target),) = args
        argument = self.stack.pop()
        old = bindings.resolve(target)
        bindings.assign(target, old | argument)

    def instruction_xor(self, args, bindings):
        ((_, target),) = args
        argument = self.stack.pop()
        old = bindings.resolve(target)
        bindings.assign(target, old ^ argument)

    def instruction_negate(self, args, bindings):
        ((_, target),) = args
        old = bindings.resolve(target)
        bindings.assign(target, ~old)

    def instruction_not(self, args, bindings):
        ((_, target),) = args
        old = bindings.resolve(target)
        bindings.assign(target, 0 if old else old)

    def instruction_if(self, args, bindings):
        for index in range(0, len(args) - 1, 2):
            condition = args[index]
            block = args[index + 1]

            if self.resolve_value(condition, bindings):
                child_bindings = bindings.inherit()
                return self.execute_block(block, child_bindings)

        # odd numbered lists have an else, execute it if everything else failed
        if len(args) % 2:
            block = args[-1]
            child_bindings = bindings.inherit()
            return self.execute_block(block, child_bindings)

    def instruction_while(self, args, bindings):
        condition, block = args
        while self.resolve_value(condition, bindings):
            child_bindings = bindings.inherit()
            stop = self.execute_block(block, child_bindings)
            if stop:
                return True

        return False

    def instruction_push(self, args, bindings):
        value = self.resolve_value(args[0], bindings)
        self.stack.append(value)

    def instruction_pop(self, args, bindings):
        _, target = args[0]
        value = self.stack.pop()
        bindings.assign(target, value)

    def instruction_invocation(self, args):
        _, subroutine = args[0]
        self.invoke_subroutine(subroutine, Bindings())

    def instruction_store(self):
        while len(self.stack) >= 2:
            pos = self.stack.pop()
            value = self.stack.pop()

            if pos < 0:
                raise InvalidMemoryAddressException(f"Invalid position {pos}")

            if pos >= len(self.heap):
                self.heap.extend([None] * (pos - len(self.heap) + 1))

            self.heap[pos] = value

    def instruction_load(self):
        temp_positions = []
        while len(self.stack) > 0:
            pos = self.stack.pop()
            temp_positions.append(pos)

        for pos in reversed(temp_positions):
            if pos < 0 or pos >= len(self.heap):
                raise InvalidMemoryAddressException(f"Invalid memory access at position: {pos}")

            value = self.heap[pos]
            self.stack.append(value)

    def resolve_value(self, value, bindings: Bindings):
        kind, content = value
        if kind == "id":
            return bindings.resolve(content)

        return content

    def invoke_subroutine(self, name, bindings: Bindings):
        if name not in self.subroutines:
            raise UnknownSubroutine(f"No subroutine called {name}")
        self.execute_block(self.subroutines[name], bindings)

    def run(self):
        self.invoke_subroutine("main", Bindings())
