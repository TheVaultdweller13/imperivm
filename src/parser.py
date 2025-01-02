import grammar
import preprocessor
import visitor


class ImperivmParser:
    def __init__(
        self,
        grammar=grammar.imperivm,
        visitor=visitor.ImperivmVisitor(),
        preprocessor=preprocessor.PipelinePreprocessor([preprocessor.CommentsPreprocessor()]),
    ):
        self.grammar = grammar
        self.visitor = visitor
        self.preprocessor = preprocessor

    def parse(self, program):
        program = self.preprocessor.process(program)
        tree = self.grammar.parse(program)
        return self.visitor.visit(tree)