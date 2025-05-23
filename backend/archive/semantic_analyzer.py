from lark import Transformer

class SemanticError(Exception):
    pass

class SemanticAnalyzer(Transformer):
    def __init__(self):
        super().__init__()
        # This symbol table is a dictionary that can hold variable, fixed, and function declarations.
        self.symbol_table = {}

    def varlist_declaration(self, items):
        var_name = str(items[1])
        if var_name in self.symbol_table:
            raise SemanticError(f"Duplicate declaration of variable '{var_name}'.")
        self.symbol_table[var_name] = {"declared": True}
        return items

    def fixed_declaration(self, items):
        fixed_name = items[1]
        self.symbol_table[str(fixed_name)] = {"type": "fixed", "value": items[2]}
        return items

    def func_definition(self, items):
        func_name = str(items[1])
        if func_name in self.symbol_table:
            raise SemanticError(f"Duplicate definition of function '{func_name}'.")
        params = items[3] if len(items) > 3 else []
        body = items[5] if len(items) > 5 else None
        self.symbol_table[func_name] = {"type": "func", "params": params, "body": body}
        return items

    # --- New methods for type checking ---

    def additive_expr(self, items):
        """
        Handles additive expressions: a multiplicative_expr followed by
        zero or more pairs of (PLUS | MINUS) and multiplicative_expr.
        
        If the operator is '+', then if either operand is TEXT then both must be TEXT (concatenation).
        Numeric addition requires both operands to be of the same numeric type.
        The '-' operator is only allowed for numeric types.
        """
        # items[0] is the left-most operand, which should be a dict with a "type" key.
        result = items[0]
        index = 1
        while index < len(items):
            op = items[index]
            right = items[index + 1]
            if op == '+':
                # If either operand is TEXT, then both must be TEXT.
                if result.get("type") == "TEXT" or right.get("type") == "TEXT":
                    if result.get("type") != "TEXT" or right.get("type") != "TEXT":
                        raise SemanticError("Type error: '+' used for concatenation requires both operands to be TEXT.")
                    result = {"type": "TEXT"}
                else:
                    # Both operands should be numeric and of the same type.
                    if result.get("type") != right.get("type"):
                        raise SemanticError("Type error: '+' operator applied to numeric operands of different types.")
                    result = {"type": result.get("type")}
            elif op == '-':
                # Subtraction: only allowed for numeric types.
                if result.get("type") == "TEXT" or right.get("type") == "TEXT":
                    raise SemanticError("Type error: '-' operator is not defined for TEXT operands.")
                if result.get("type") != right.get("type"):
                    raise SemanticError("Type error: '-' operator applied to numeric operands of different types.")
                result = {"type": result.get("type")}
            index += 2
        return result

    # Example literal handlers that attach type information.
    def INTEGERLITERAL(self, token):
        return {"type": "INTEGER", "value": int(token)}

    def FLOATLITERAL(self, token):
        # Assuming FLOATLITERAL should result in a numeric type (you may want to distinguish FLOAT from INTEGER)
        return {"type": "FLOAT", "value": float(token)}

    def STRINGLITERAL(self, token):
        return {"type": "TEXT", "value": str(token)}

    def STATELITERAL(self, token):
        # Assuming state literals (YES/NO) result in type STATE.
        return {"type": "STATE", "value": str(token)}

    # You can add similar methods for other expressions and literals as needed.