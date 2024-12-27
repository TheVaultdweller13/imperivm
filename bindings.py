class UnboundNameException(Exception):
    pass


class Bindings:
    def __init__(self, parent=None):
        self.parent = parent
        self.names = {}

    def inherit(self):
        return Bindings(self)

    def resolve(self, name):
        if name not in self.names:
            if not self.parent:
                raise UnboundNameException(f"Unbound name {name}")
            return self.parent.resolve(name)
        return self.names[name]

    def assign(self, name, value):
        current = self
        while name not in current.names and self.parent:
            current = current.parent

        if name in current.names:
            # if found in parent bindings assign there
            current.names[name] = value
        else:
            # else assign here
            self.names[name] = value
