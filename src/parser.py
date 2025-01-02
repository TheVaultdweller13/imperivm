#!/bin/env python
import argparse
import pprint

import grammar
import visitor
import preprocessor


class ImperivmParser:
    def __init__(
        self,
        grammar=grammar.imperivm,
        visitor=visitor.ImperivmVisitor(),
        preprocessor=preprocessor.PipelinePreprocessor(
            [preprocessor.CommentsPreprocessor()]
        ),
    ):
        self.grammar = grammar
        self.visitor = visitor
        self.preprocessor = preprocessor

    def parse(self, program):
        program = self.preprocessor.process(program)
        tree = self.grammar.parse(program)
        return self.visitor.visit(tree)


if __name__ == "__main__":
    argparser = argparse.ArgumentParser()
    argparser.add_argument("filename", nargs=1)
    args = argparser.parse_args()
    data = None
    with open(args.filename[0], "r") as file:
        code = file.read()

    ast = ImperivmParser().parse(code)
    pprint.pprint(ast)
