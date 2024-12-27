KEY_PARENT = "$parent"


class UnknownNameException(Exception):
    pass


class UnknownSubroutine(Exception):
    pass


class ImperivmExecutor:
    def __init__(self, ast):
        self.subroutines = {}
        self.stack = []
        for _, (_, identifier), block in ast:
            self.subroutines[identifier] = block

    def execute_block(self, block, bindings):
        for instruction in block:
            stop = self.execute_instruction(instruction, bindings)
            if stop:
                return True

    def execute_instruction(self, instruction, bindings):
        operation, *rest = instruction

        if operation == "add":
            value, (_, target) = rest
            old = self.resolve_id(target, bindings)
            current = self.resolve_value(value, bindings)
            self.assign_value(bindings, target, old + current)
        elif operation == "subtract":
            value, (_, target) = rest
            old = self.resolve_id(target, bindings)
            current = self.resolve_value(value, bindings)
            self.assign_value(bindings, target, old - current)
        elif operation == "multiply":
            value, (_, target) = rest
            old = self.resolve_id(target, bindings)
            current = self.resolve_value(value, bindings)
            self.assign_value(bindings, target, old * current)
        elif operation == "divide":
            value, (_, target) = rest
            old = self.resolve_id(target, bindings)
            current = self.resolve_value(value, bindings)
            self.assign_value(bindings, target, old / current)
        elif operation == "if":
            for index in range(0, len(rest) - 1, 2):
                condition = rest[index]
                block = rest[index + 1]

                if self.resolve_value(condition, bindings):
                    child_bindings = self.inherit_bindings(bindings)
                    return self.execute_block(block, child_bindings)

            # odd numbered lists have an else, execute it if everything else failed
            if len(rest) % 2:
                block = rest[-1]
                child_bindings = self.inherit_bindings(bindings)
                return self.execute_block(block, child_bindings)

        elif operation == "while":
            condition, block = rest
            while self.resolve_value(condition, bindings):
                child_bindings = self.inherit_bindings(bindings)
                stop = self.execute_block(block, child_bindings)
                if stop:
                    return True
        elif operation == "print":
            print(self.resolve_value(rest[0], bindings))
        elif operation == "push":
            value = self.resolve_value(rest[0], bindings)
            self.stack.append(value)
        elif operation == "pop":
            _, target = rest[0]
            value = self.stack.pop()
            self.assign_value(bindings, target, value)
        elif operation == "assign":
            value, (_, target) = rest
            result = self.resolve_value(value, bindings)
            self.assign_value(bindings, target, result)
        elif operation == "invocation":
            _, subroutine = rest[0]
            self.invoke_subroutine(subroutine, {})
        elif operation == "stop":
            return True
        else:
            print("error", instruction)

        return False

    def resolve_value(self, value, bindings: dict):
        kind, content = value
        if kind == "id":
            return self.resolve_id(content, bindings)

        return content

    @staticmethod
    def resolve_id(name, bindings):
        if name not in bindings:
            if KEY_PARENT not in bindings:
                raise UnknownNameException(f"Unbound name {name}")
            return ImperivmExecutor.resolve_id(name, bindings[KEY_PARENT])
        return bindings[name]

    @staticmethod
    def inherit_bindings(bindings):
        return {KEY_PARENT: bindings}

    @staticmethod
    def assign_value(bindings, name, value):
        current = bindings
        while name not in current and KEY_PARENT in bindings:
            current = bindings[KEY_PARENT]

        if name in current:
            current[name] = value
        else:
            bindings[name] = value

    def invoke_subroutine(self, name, bindings):
        if name not in self.subroutines:
            raise UnknownSubroutine(f"No subroutine called {name}")
        self.execute_block(self.subroutines[name], bindings)

    def run(self):
        self.invoke_subroutine("main", {})
