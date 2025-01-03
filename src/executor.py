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

    def execute_block(self, block, bindings: Bindings):
        for instruction in block:
            stop = self.execute_instruction(instruction, bindings)
            if stop:
                return True

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

    def execute_instruction(self, instruction, bindings: Bindings):
        operation, *args = instruction

        if operation == "add":
            self.instruction_add(args, bindings)
        elif operation == "subtract":
            self.instruction_subtract(args, bindings)
        elif operation == "multiply":
            self.instruction_multiply(args, bindings)
        elif operation == "divide":
            self.instruction_multiply(args, bindings)
        elif operation == "and":
            self.instruction_and(args, bindings)
        elif operation == "or":
            self.instruction_or(args, bindings)
        elif operation == "xor":
            self.instruction_xor(args, bindings)
        elif operation == "negate":
            self.instruction_negate(args, bindings)
        elif operation == "not":
            self.instruction_not(args, bindings)
        elif operation == "if":
            return self.instruction_if(args, bindings)
        elif operation == "while":
            return self.instruction_while(args, bindings)
        elif operation == "exit":
            exit(self.resolve_value(args[0], bindings))
        elif operation == "print":
            print(self.resolve_value(args[0], bindings))
        elif operation == "push":
            self.instruction_push(args, bindings)
        elif operation == "pop":
            self.instruction_pop(args, bindings)
        elif operation == "invocation":
            self.instruction_invocation(args)
        elif operation == "stop":
            return True
        elif operation == "store":
            self.instruction_store()
        elif operation == "load":
            self.instruction_load()
        else:
            print("error", instruction)

        return False

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
