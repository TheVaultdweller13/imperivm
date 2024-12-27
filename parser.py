import grammar
import visitor


class ImperivmParser:
    def __init__(self, grammar=grammar.imperivm, visitor=visitor.ImperivmVisitor()):
        self.grammar = grammar
        self.visitor = visitor

    def parse(self, code):
        tree = self.grammar.parse(code)
        return self.visitor.visit(tree)
