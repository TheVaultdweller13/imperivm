#!/bin/env python
import argparse
import pprint
import re
from abc import abstractmethod
from typing import override

import grammar
import visitor


class Preprocessor:
    @abstractmethod
    def process(self, program: str):
        pass


class CommentsPreprocessor(Preprocessor):

    @override
    def process(self, program: str):
        cleaned_program = map(lambda line: re.sub(r'#.*$', '', line), program.splitlines())
        return "\n".join(cleaned_program)

class PipelinePreprocessor(Preprocessor):
    def __init__(self, preprocessor_actions ):
        self.preprocessor_actions = preprocessor_actions

    @override
    def process(self, program: str):
        for action in self.preprocessor_actions:
            program = action.process(program)
        return program


class ImperivmParser:
    def __init__(self, grammar=grammar.imperivm, visitor=visitor.ImperivmVisitor(), preprocessor = None):
        self.grammar = grammar
        self.visitor = visitor
        self.preprocessor = preprocessor or PipelinePreprocessor([CommentsPreprocessor()])

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
