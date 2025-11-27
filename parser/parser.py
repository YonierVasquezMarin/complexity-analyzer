from lark import Lark, Transformer, v_args

# Cargar gramática
with open("grammar.lark", "r", encoding="utf-8") as f:
    GRAMMAR = f.read()

parser = Lark(GRAMMAR, start="start", parser="lalr")


# ───────────────────────────────────────
# TRANSFORMER → Convierte parse tree → AST
# ───────────────────────────────────────
class PseudoCodeTransformer(Transformer):

    # ───────────────────────────────
    # PROGRAMA Y SENTENCIAS
    # ───────────────────────────────
    def start(self, items):
        return {"type": "program", "body": items}

    def program(self, items):
        return items

    def statement(self, items):
        return items[0]

    # ───────────────────────────────
    # ASIGNACIONES
    # ───────────────────────────────
    def assignment(self, items):
        return {
            "type": "assignment",
            "target": items[0],
            "value": items[1]
        }

    # variable → NAME / NAME.NAME / NAME[index]
    def variable(self, items):
        # NAME
        if len(items) == 1:
            return {"type": "var", "name": str(items[0])}

        # NAME . NAME
        if len(items) == 2 and isinstance(items[1], str):
            return {
                "type": "field_access",
                "object": str(items[0]),
                "field": str(items[1])
            }

        # NAME array_index
        if len(items) == 2:
            return {
                "type": "array_access",
                "array": str(items[0]),
                "index": items[1]
            }

    def array_index(self, items):
        return items[0]

    def index_range(self, items):
        if len(items) == 1:
            return {"type": "index", "value": items[0]}
        return {
            "type": "range",
            "start": items[0],
            "end": items[1]
        }

    # ───────────────────────────────
    # CICLO FOR
    # ───────────────────────────────
    def for_loop(self, items):
        return {
            "type": "for",
            "var": str(items[0]),
            "start": items[1],
            "end": items[2],
            "body": items[3]
        }

    # ───────────────────────────────
    # CICLO WHILE
    # ───────────────────────────────
    def while_loop(self, items):
        return {
            "type": "while",
            "condition": items[0],
            "body": items[1]
        }

    # ───────────────────────────────
    # REPEAT UNTIL
    # ───────────────────────────────
    def repeat_loop(self, items):
        return {
            "type": "repeat",
            "body": items[0],
            "condition": items[1]
        }

    # ───────────────────────────────
    # IF / ELSE
    # ───────────────────────────────
    def if_statement(self, items):
        if len(items) == 2:
            return {
                "type": "if",
                "condition": items[0],
                "then": items[1],
                "else": None
            }
        return {
            "type": "if",
            "condition": items[0],
            "then": items[1],
            "else": items[2]
        }

    # ───────────────────────────────
    # BLOQUES BEGIN...END
    # ───────────────────────────────
    def block(self, items):
        return {"type": "block", "body": items}

    # ───────────────────────────────
    # CALL
    # ───────────────────────────────
    def call(self, items):
        name = str(items[0])
        args = items[1] if len(items) == 2 else []
        return {"type": "call", "name": name, "args": args}

    def arg_list(self, items):
        return items

    # ───────────────────────────────
    # CLASES
    # ───────────────────────────────
    def class_decl(self, items):
        name = str(items[0])
        attributes = items[1:]
        return {
            "type": "class_decl",
            "name": name,
            "attributes": [str(a) for a in attributes]
        }

    def class_attr(self, items):
        return items[0]

    # ───────────────────────────────
    # OBJETOS: Clase Nombre
    # ───────────────────────────────
    def object_decl(self, items):
        return {
            "type": "object_decl",
            "class": str(items[0]),
            "name": str(items[1])
        }

    # ───────────────────────────────
    # SUBRUTINAS
    # ───────────────────────────────
    def subroutine_decl(self, items):
        name = str(items[0])
        params = items[1] if len(items) == 3 else []
        body = items[-1]
        return {
            "type": "subroutine",
            "name": name,
            "params": params,
            "body": body
        }

    def param_list(self, items):
        return items

    def param(self, items):
        if len(items) == 1:
            return {"type": "param", "name": str(items[0])}
        if len(items) == 2 and isinstance(items[1], list):
            return {"type": "param_array", "name": str(items[0]), "dims": items[1]}
        return {"type": "param_object", "class": str(items[0]), "name": str(items[1])}

    def array_dims(self, items):
        return [{"dim": x} for x in items]

    # ───────────────────────────────
    # EXPRESIONES Y CONDICIONES
    # ───────────────────────────────
    def condition(self, items):
        return items[0]

    def or_expr(self, items):
        if len(items) == 1:
            return items[0]
        return {"type": "or", "left": items[0], "right": items[1]}

    def and_expr(self, items):
        if len(items) == 1:
            return items[0]
        return {"type": "and", "left": items[0], "right": items[1]}

    def not_expr(self, items):
        if len(items) == 1:
            return items[0]
        return {"type": "not", "value": items[0]}

    def comparison(self, items):
        if len(items) == 1:
            return items[0]
        return {
            "type": "comparison",
            "left": items[0],
            "op": items[1].value,
            "right": items[2]
        }

    def expr(self, items):
        # Uno solo
        if len(items) == 1:
            return items[0]
        # expr op term
        return {
            "type": "binary_op",
            "left": items[0],
            "op": items[1].value,
            "right": items[2]
        }

    def term(self, items):
        if len(items) == 1:
            return items[0]
        return {
            "type": "binary_op",
            "left": items[0],
            "op": items[1].value,
            "right": items[2]
        }

    def factor(self, items):
        return items[0]

    # ───────────────────────────────
    # TOKENS
    # ───────────────────────────────
    def NAME(self, token):
        return str(token)

    def NUMBER(self, token):
        return int(token)

    def REL_OP(self, token):
        return token


# ───────────────────────────────────────
# FUNCIÓN DE PARSEO
# ───────────────────────────────────────
def parse(code: str):
    tree = parser.parse(code)
    return PseudoCodeTransformer().transform(tree)
