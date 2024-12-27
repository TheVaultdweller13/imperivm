#!/bin/env python
import argparse
import pprint
import grammar
import visitor


class ImperivmParser:
    def __init__(self, grammar=grammar.imperivm, visitor=visitor.ImperivmVisitor()):
        self.grammar = grammar
        self.visitor = visitor

    def parse(self, code):
        tree = self.grammar.parse(code)
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
