from bindings import Bindings


class UnknownSubroutine(Exception):
    pass


class ImperivmExecutor:
    def __init__(self, ast):
        self.subroutines = {}
        self.stack = []
        for _, (_, identifier), block in ast:
            self.subroutines[identifier] = block

    def execute_block(self, block, bindings: Bindings):
        for instruction in block:
            stop = self.execute_instruction(instruction, bindings)
            if stop:
                return True

    def execute_instruction(self, instruction, bindings: Bindings):
        operation, *rest = instruction

        if operation == "add":
            value, (_, target) = rest
            old = bindings.resolve(target)
            current = self.resolve_value(value, bindings)
            bindings.assign(target, old + current)
        elif operation == "subtract":
            value, (_, target) = rest
            old = bindings.resolve(target)
            current = self.resolve_value(value, bindings)
            bindings.assign(target, old - current)
        elif operation == "multiply":
            value, (_, target) = rest
            old = bindings.resolve(target)
            current = self.resolve_value(value, bindings)
            bindings.assign(target, old * current)
        elif operation == "divide":
            value, (_, target) = rest
            old = bindings.resolve(target)
            current = self.resolve_value(value, bindings)
            bindings.assign(target, old // current)
        elif operation == "if":
            for index in range(0, len(rest) - 1, 2):
                condition = rest[index]
                block = rest[index + 1]

                if self.resolve_value(condition, bindings):
                    child_bindings = bindings.inherit()
                    return self.execute_block(block, child_bindings)

            # odd numbered lists have an else, execute it if everything else failed
            if len(rest) % 2:
                block = rest[-1]
                child_bindings = bindings.inherit()
                return self.execute_block(block, child_bindings)

        elif operation == "while":
            condition, block = rest
            while self.resolve_value(condition, bindings):
                child_bindings = bindings.inherit()
                stop = self.execute_block(block, child_bindings)
                if stop:
                    return True
        elif operation == 'exit':
            exit(self.resolve_value(rest[0], bindings))
        elif operation == "print":
            print(self.resolve_value(rest[0], bindings))
        elif operation == "push":
            value = self.resolve_value(rest[0], bindings)
            self.stack.append(value)
        elif operation == "pop":
            _, target = rest[0]
            value = self.stack.pop()
            bindings.assign(target, value)
        elif operation == "assign":
            value, (_, target) = rest
            result = self.resolve_value(value, bindings)
            bindings.assign(target, result)
        elif operation == "invocation":
            _, subroutine = rest[0]
            self.invoke_subroutine(subroutine, Bindings())
        elif operation == "stop":
            return True
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
