from lark import Lark, Transformer, Token

class PseudocodeParser:
    def __init__(self):
        self.lark = Lark.open("syntax/grammar.lark", start="program", parser="lalr")

    def parse(self, text):
        tree = self.lark.parse(text)
        return PseudocodeTransformer().transform(tree)


class PseudocodeTransformer(Transformer):
    """
    AST limpio sin conversiones prematuras.
    Lark devuelve Tokens y listas. NO convertimos NUMBER a int aquí.
    """

    def program(self, items):
        return {"type": "program", "body": items}

    def assignment(self, items):
        return {"type": "assignment", "var": items[0], "expr": items[1]}

    def for_loop(self, items):
        return {
            "type": "for",
            "var": items[0],
            "start": items[1],
            "end": items[2],
            "body": items[3],
        }

    def while_loop(self, items):
        return {
            "type": "while",
            "condition": items[0],
            "body": items[1],
        }

    def repeat_loop(self, items):
        return {
            "type": "repeat",
            "body": items[0],
            "condition": items[1],
        }

    def if_statement(self, items):
        if len(items) == 2:
            return {"type": "if", "condition": items[0], "then": items[1], "else": None}
        return {"type": "if", "condition": items[0], "then": items[1], "else": items[2]}

    def block(self, items):
        return {"type": "block", "body": items}

    def call(self, items):
        name = items[0]
        args = items[1] if len(items) > 1 else []
        return {"type": "call", "name": name, "args": args}

    # NO convertir NUMBER → int
    def factor(self, items):
        return items[0]