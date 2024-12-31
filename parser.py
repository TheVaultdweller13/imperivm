#!/bin/env python
import argparse
import pprint
import re

import grammar
import visitor

class PreProcessor:
    @staticmethod
    def remove_comments(program: str):
        lines = program.splitlines()
        cleaned_lines = []
        for line in lines:
            cleaned_line = re.sub(r'#.*$', '', line).strip()
            if cleaned_line:
                cleaned_lines.append(cleaned_line)
        return "\n".join(cleaned_lines)

class ImperivmParser:
    def __init__(self, grammar=grammar.imperivm, visitor=visitor.ImperivmVisitor()):
        self.grammar = grammar
        self.visitor = visitor

    def parse(self, program):
        program = PreProcessor.remove_comments(program)
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
