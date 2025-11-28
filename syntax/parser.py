from lark import Lark, Transformer, Token, Tree
import os

class PseudocodeParser:
    def __init__(self):
        # Construir la ruta absoluta al archivo grammar.lark
        current_dir = os.path.dirname(os.path.abspath(__file__))
        grammar_path = os.path.join(current_dir, "grammar.lark")
        
        self.lark = Lark.open(grammar_path, start="program", parser="lalr")

    def parse(self, text):
        tree = self.lark.parse(text)
        transformed = PseudocodeTransformer().transform(tree)
        return transformed


class PseudocodeTransformer(Transformer):
    """
    Transformer robusto que maneja todos los casos de la gramática.
    """

    def program(self, items):
        return {"type": "program", "body": items}

    def statement(self, items):
        # statement solo tiene un hijo, devolvemos ese hijo directamente
        return items[0] if items else None

    def assignment(self, items):
        # variable ASSIGN expr
        # items[0] = variable
        # items[1] = ASSIGN (🡨) - lo ignoramos
        # items[2] = expr
        if len(items) >= 3:
            return {"type": "assignment", "var": items[0], "expr": items[2]}
        elif len(items) == 2:
            return {"type": "assignment", "var": items[0], "expr": items[1]}
        else:
            return {"type": "assignment", "var": items[0], "expr": {"type": "number", "value": "0"}}

    def for_loop(self, items):
        # for NAME ASSIGN expr to expr do block
        # Lark filtra keywords, pero mantiene ASSIGN
        # items[0] = NAME
        # items[1] = ASSIGN (🡨) - lo ignoramos
        # items[2] = expr (start)
        # items[3] = expr (end)
        # items[4] = block
        return {
            "type": "for",
            "var": self._extract_value(items[0]),
            "start": items[2],  # Saltamos ASSIGN
            "end": items[3],
            "body": items[4],
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
        name = self._extract_value(items[0])
        args = items[1] if len(items) > 1 else []
        return {"type": "call", "name": name, "args": args}

    def arg_list(self, items):
        return items

    def class_decl(self, items):
        return {"type": "class", "name": self._extract_value(items[0]), "attrs": items[1:]}

    def class_attr(self, items):
        return self._extract_value(items[0])

    def object_decl(self, items):
        return {
            "type": "object",
            "class": self._extract_value(items[0]),
            "name": self._extract_value(items[1])
        }

    def subroutine_decl(self, items):
        name = self._extract_value(items[0])
        if len(items) == 2:
            return {"type": "subroutine", "name": name, "params": [], "body": items[1]}
        else:
            return {"type": "subroutine", "name": name, "params": items[1], "body": items[2]}

    def param_list(self, items):
        return items

    def param(self, items):
        return items[0] if items else None

    def array_dims(self, items):
        return items

    # ---- Variables ----
    
    def variable(self, items):
        if not items:
            return {"type": "var", "name": "unknown"}
        
        if len(items) == 1:
            return {"type": "var", "name": self._extract_value(items[0])}
        else:
            # obj.field o arr[index]
            return {"type": "var", "name": self._extract_value(items[0]), "access": items[1]}

    def array_index(self, items):
        return {"type": "array_index", "range": items[0] if items else None}

    def index_range(self, items):
        return items

    # ---- Condiciones ----
    
    def condition(self, items):
        return items[0] if items else None

    def or_expr(self, items):
        if len(items) == 1:
            return items[0]
        elif len(items) == 3:
            return {"type": "or", "left": items[0], "right": items[2]}
        return items[0] if items else None

    def and_expr(self, items):
        if len(items) == 1:
            return items[0]
        elif len(items) == 3:
            return {"type": "and", "left": items[0], "right": items[2]}
        return items[0] if items else None

    def not_expr(self, items):
        if len(items) == 1:
            return items[0]
        elif len(items) == 2:
            return {"type": "not", "expr": items[1]}
        return items[0] if items else None

    def comparison(self, items):
        if len(items) == 1:
            return items[0]
        elif len(items) == 3:
            return {"type": "comparison", "left": items[0], "op": str(items[1]), "right": items[2]}
        return items[0] if items else None

    # ---- Expresiones matemáticas ----
    
    def expr(self, items):
        if not items:
            return {"type": "number", "value": "0"}
        if len(items) == 1:
            return items[0]
        elif len(items) == 3:
            return {"type": "binop", "left": items[0], "op": str(items[1]), "right": items[2]}
        # Si hay más o menos elementos, devolver el primero
        return items[0]

    def term(self, items):
        if not items:
            return {"type": "number", "value": "1"}
        if len(items) == 1:
            return items[0]
        elif len(items) == 3:
            return {"type": "binop", "left": items[0], "op": str(items[1]), "right": items[2]}
        return items[0]

    def factor(self, items):
        # factor siempre devuelve un solo elemento
        return items[0] if items else {"type": "number", "value": "0"}

    # ---- Tokens básicos ----
    
    def NUMBER(self, token):
        return {"type": "number", "value": str(token)}

    def NAME(self, token):
        return {"type": "name", "value": str(token)}

    def REL_OP(self, token):
        return str(token)
    
    def ADD_OP(self, token):
        return str(token)
    
    def MUL_OP(self, token):
        return str(token)

    # ---- Utilidades ----
    
    def _extract_value(self, item):
        """Extrae el valor string de diferentes tipos de elementos."""
        if item is None:
            return "unknown"
        if isinstance(item, Token):
            return str(item)
        if isinstance(item, str):
            return item
        if isinstance(item, dict):
            if "value" in item:
                return item["value"]
            if "name" in item:
                return item["name"]
        return str(item)