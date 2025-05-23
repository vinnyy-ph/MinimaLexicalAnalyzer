from lark import Transformer

class SemanticAnalyzer(Transformer):
    def __init__(self):
        super().__init__()
        # This symbol table is a dictionary that can hold variable, fixed, and function declarations.
        self.symbol_table = {}

    def varlist_declaration(self, items):
        # items[0] is the "var" token, items[1] is the identifier.
        var_name = items[1]
        # For demonstration, we set a dummy value.
        self.symbol_table[str(var_name)] = {"type": "var", "value": None}
        # If there's initialization, update the value.
        if len(items) > 2:
            self.symbol_table[str(var_name)]["value"] = items[2]
        return items

    def fixed_declaration(self, items):
        fixed_name = items[1]
        self.symbol_table[str(fixed_name)] = {"type": "fixed", "value": items[2]}
        return items

    def func_definition(self, items):
        func_name = items[1]
        # Simplified extraction of parameters and body.
        params = items[3] if len(items) > 3 else []
        body = items[5] if len(items) > 5 else None
        self.symbol_table[str(func_name)] = {"type": "func", "params": params, "body": body}
        return items

    def analyze(self, parse_tree):
        # Perform semantic analysis via transformation.
        # Modify this to detect semantic errors if needed.
        self.transform(parse_tree)
        return []  # Return a list of semantic error objects if any.