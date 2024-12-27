#!/bin/env python

import argparse
from parsimonious.grammar import Grammar
from parsimonious.nodes import NodeVisitor

grammar = Grammar(
    r"""
    program         = subroutine (sp_0n br ws_0n subroutine)* ws_0n
    subroutine      = identifier ws_1n block
    block           = begin ws_1n (instruction (sp_0n br ws_0n instruction)*)? ws_1n end
    instruction     = assignment / conditional / loop / stack_op / arithmetic_op / io_op / stop / invocation

    assignment      = assign sp_1n value sp_1n identifier
    conditional     = if sp_1n value ws_1n block (ws_1n elif sp_1n value ws_1n block)* (ws_1n else ws_1n block)?
    loop            = while sp_1n value ws_1n block
    stack_op        = (push sp_1n value) / (pop sp_1n identifier)
    arithmetic_op   = (add / subtract / multiply / divide) sp_1n value sp_1n identifier
    io_op           = print sp_1n value
    invocation      = identifier

    value           = identifier / literal
    literal         = integer / float / string

    identifier      = !reserved ~r"[a-z][a-z0-9_]*"i
    
    integer         = ~r"0|([1-9][0-9]*)"
    float           = ~r"(0|([1-9][0-9]*))\.[0-9]+"
    string          = quote string_text quote

    quote           = "\""
    string_text     = ~r"([^\"\\]|\\.)*"

    br              = ~r"\n"
    ws_0n           = ~r"\s*"
    ws_1n           = ~r"\s+"
    sp_0n           = ~r"[ \t]*"
    sp_1n           = ~r"[ \t]+"

    reserved        = begin / end / stop / if / elif / else / while / push / pop / assign / add / subtract / multiply / divide / print
    begin           = ~r"begin"i / ~r"do"i
    end             = ~r"end"i
    stop            = ~r"stop"i
    if              = ~r"if"i
    elif            = ~r"elif"i
    else            = ~r"else"i
    while           = ~r"while"i
    push            = ~r"push"i
    pop             = ~r"pop"i
    assign          = ~r"assign"i
    add             = ~r"add"i
    subtract        = ~r"subtract"i
    multiply        = ~r"multiply"i
    divide          = ~r"divide"i
    print           = ~r"print"i
    """
)


class ImperivmVisitor(NodeVisitor):
    def visit_program(self, _, visited_children):
        first, rest, _ = visited_children
        subroutines = [first]
        for _, _, _, subroutine in rest:
            subroutines.append(subroutine)

        return tuple(subroutines)

    def visit_subroutine(self, _, visited_children):
        identifier, _, block = visited_children
        return ("subroutine", identifier, block)

    def visit_block(self, _, visited_children):
        _, _, instructions, _, _ = visited_children
        [child] = instructions
        [first], rest = child
        result = list(map(lambda instruction: instruction[3][0], rest))
        result.insert(0, first)
        return tuple(result)

    def visit_assignment(self, _, visited_children):
        instruction, _, value, _, target = visited_children
        return (instruction.text, value, target)

    def visit_conditional(self, _, visited_children):
        operation, _, condition, _, block, elif_operations, else_operations = (
            visited_children
        )

        elif_tree = []
        if type(elif_operations) is list:
            for _, _, _, elif_condition, _, elif_block in elif_operations:
                elif_tree.append(elif_condition)
                elif_tree.append(elif_block)

        else_tree = []
        if type(else_operations) is list:
            for _, _, _, else_block in else_operations:
                else_tree.append(else_block)

        return tuple([operation.text, condition, block] + elif_tree + else_tree)

    def visit_loop(self, _, visited_children):
        operation, _, condition, _, block = visited_children
        return (operation.text, condition, block)

    def visit_stack_op(self, _, visited_children):
        [child] = visited_children
        operation, _, target = child
        return (operation.text, target)

    def visit_arithmetic_op(self, _, visited_children):
        [operation], _, value, _, target = visited_children
        return (operation.text, value, target)

    def visit_io_op(self, _, visited_children):
        operation, _, target = visited_children
        return (operation.text, target)

    def visit_stop(self, _, __):
        return ("stop",)

    def visit_invocation(self, _, visited_children):
        return ("invocation", visited_children)

    def visit_value(self, _, visited_children):
        return visited_children[0]

    def visit_literal(self, _, visited_children):
        return visited_children[0]

    def visit_string(self, _, visited_children):
        _, content, _ = visited_children
        return ("string", content.text)

    def visit_integer(self, node, _):
        return ("integer", int(node.text))

    def visit_float(self, node, _):
        return ("float", float(node.text))

    def visit_identifier(self, node, _):
        return ("id", node.text)

    def generic_visit(self, node, visited_children):
        """The generic visit method."""
        return visited_children or node


KEY_PARENT = "$parent"


class ImperivmExecutor:
    def __init__(self, ast):
        self.subroutines = {}
        self.stack = []
        for _, (_, identifier), block in ast:
            self.subroutines[identifier] = block

    def execute_block(self, block, bindings):
        for instruction in block:
            if instruction[0] == "stop":
                break
            self.execute_instruction(instruction, bindings)

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

            bindings[target] /= current
        elif operation == "if":
            print(operation)
        elif operation == "while":
            condition, block = rest
            while self.resolve_value(condition, bindings):
                child_bindings = self.inherit_bindings(bindings)
                self.execute_block(block, child_bindings)
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
            self.execute_block(self.subroutines[subroutine], {})
        else:
            print("error", operation)

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

    def run(self):
        self.execute_block(self.subroutines["main"], {})


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("filename", nargs=1)
    args = parser.parse_args()
    data = None
    with open(args.filename[0], "r") as f:
        data = f.read()
    tree = grammar.parse(data)

    iv = ImperivmVisitor()
    ast = iv.visit(tree)
    ImperivmExecutor(ast).run()


class UnknownNameException(Exception):
    pass
