from parsimonious.nodes import NodeVisitor


class ImperivmVisitor(NodeVisitor):
    def visit_program(self, _, visited_children):
        _, first, rest, _ = visited_children
        subroutines = [first]
        for *_, subroutine in rest:
            subroutines.append(subroutine)

        return tuple(subroutines)

    def visit_subroutine(self, _, visited_children):
        identifier, _, block = visited_children
        return "subroutine", identifier, block

    def visit_store(self, _, __):
        return ("store",)

    def visit_load(self, _, __):
        return ("load",)

    def visit_block(self, _, visited_children):
        _, _, instructions, _, _ = visited_children
        [child] = instructions
        [first], rest = child
        result = list(map(lambda instruction: instruction[3][0], rest))
        result.insert(0, first)
        return tuple(result)

    def visit_instruction(self, node, visited_children):
        if visited_children[0][0] == "id":
            return [("invocation", visited_children[0])]
        return visited_children

    def visit_assignment(self, _, visited_children):
        instruction, _, value, _, target = visited_children
        return instruction.text, value, target

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
        return operation.text, condition, block

    def visit_stack_op(self, _, visited_children):
        [child] = visited_children
        operation, _, target = child
        return operation.text, target

    def visit_arithmetic_op(self, _, visited_children):
        [operation], _, value, _, target = visited_children
        return operation.text, value, target

    def visit_io_op(self, _, visited_children):
        operation, _, target = visited_children
        return operation.text, target

    def visit_stop(self, _, __):
        return ("stop",)

    def visit_halt(self, node, visited_children):
        operation, _, status_code = visited_children
        return operation.text, status_code

    def visit_value(self, _, visited_children):
        return visited_children[0]

    def visit_literal(self, _, visited_children):
        return visited_children[0]

    def visit_string(self, _, visited_children):
        _, content, _ = visited_children
        return "string", content.text

    def visit_integer(self, node, _):
        return "integer", int(node.text)

    def visit_float(self, node, _):
        return "float", float(node.text)

    def visit_identifier(self, node, _):
        return "id", node.text

    def generic_visit(self, node, visited_children):
        """The generic visit method."""
        return visited_children or node
