from lark import Transformer, Token
from semantic_errors import UndefinedIdentifierError, SemanticError, TypeMismatchError
from symbol_table import SymbolTable

class SemanticAnalyzer(Transformer):
    def __init__(self):
        super().__init__()
        self.symbol_table = SymbolTable()
        self.errors = []

    # ---------------
    # Helper methods
    # ---------------
    def is_numeric(self, t):
        return t in ["integer", "point"]

    def add_error(self, error):
        """Add a semantic error to the analyzer's list of errors."""
        self.errors.append(error)

    def _get_value(self, item):
        """Recursively unwraps an item to return a tuple (type, value)
           If item is already a tuple, return it.
        """
        if isinstance(item, tuple):
            return item
        elif hasattr(item, "children") and item.children:
            return self._get_value(item.children[0])
        else:
            return item  # fallback
    
    def report_error(self, error_class, *args, token=None):
        """
        Helper method to instantiate an error with line/column info and add it.
        If token is provided, its 'line' and 'column' attributes are used.
        Otherwise, the error is created without them.
        """
        line = getattr(token, 'line', None) if token else None
        column = getattr(token, 'column', None) if token else None
        error = error_class(*args, line, column)
        self.add_error(error)
           
    # -----------------------
    # Literal / basic tokens
    # -----------------------
    def INTEGERLITERAL(self, token):
        return ("integer", int(token.value))

    def FLOATLITERAL(self, token):
        return ("point", float(token.value))

    def NEGINTEGERLITERAL(self, token):
        # e.g., "~123"
        return ("integer", -int(token.value[1:]))

    def NEGFLOATLITERAL(self, token):
        # e.g., "~123.456"
        return ("point", -float(token.value[1:]))

    def STRINGLITERAL(self, token):
        # e.g. "hello world"
        return ("text", token.value.strip('"'))

    def STATELITERAL(self, token):
        # e.g. YES or NO
        return ("state", token.value)

    def EMPTY(self, token):
        return ("empty", None)

    # -----------------------
    # Declarations
    # -----------------------
    # varlist_declaration: VAR IDENTIFIER var_init? var_list_declaration_tail* SEMICOLON
    def varlist_declaration(self, items):
        """
        Example parse:
          items might look like:
            [ Token(VAR, 'var'),
              Token(IDENTIFIER, 'x'),
              ('integer', 5),
              Token(COMMA, ','),
              Token(IDENTIFIER, 'y'),
              ('point', 3.14),
              ...
            ]
        We store each declared var in the symbol table.
        """
        declarations = []
        idx = 0
        # Skip the 'var' token if present
        if isinstance(items[idx], Token) and items[idx].type == "VAR":
            idx += 1

        while idx < len(items):
            if isinstance(items[idx], Token) and items[idx].type == "IDENTIFIER":
                identifier = items[idx].value
                idx += 1
                # Optional initializer (a tuple) may appear next
                if idx < len(items) and isinstance(items[idx], tuple):
                    var_type = items[idx][0]
                    idx += 1
                else:
                    var_type = "unknown"
                self.symbol_table.add(identifier, {
                    "type": "variable",
                    "fixed": False,
                    "var_type": var_type
                })
                declarations.append((identifier, var_type))
            else:
                idx += 1

        return declarations

    # var_init: ASSIGN variable_value
    def var_init(self, items):
        if len(items) == 2:
            return items[1]
        else:
            self.report_error(SemanticError, "Missing initializer in variable declaration")
            return ("error", None)

    # fixed_declaration: FIXED IDENTIFIER ASSIGN variable_value fixed_declaration_tail* SEMICOLON
    def fixed_declaration(self, items):
        if len(items) >= 4:
            if isinstance(items[1], Token) and items[1].type == "IDENTIFIER":
                identifier = items[1].value
                if isinstance(items[3], tuple):
                    var_type = items[3][0]
                else:
                    var_type = "error"
                    self.report_error(SemanticError, "Missing or invalid initializer for fixed variable.", token=items[1])
                self.symbol_table.add(identifier, {
                    "type": "variable",
                    "fixed": True,
                    "var_type": var_type
                })
        else:
            self.report_error(SemanticError, "Invalid fixed declaration structure")
        return items

    # group_declaration: GROUP IDENTIFIER LBRACE group_members RBRACE SEMICOLON?
    def group_declaration(self, items):
        if len(items) < 5:
            self.report_error(SemanticError, "Invalid group declaration", token=items[0] if items else None)
            return items
        if isinstance(items[1], Token) and items[1].type == "IDENTIFIER":
            group_name = items[1].value
        else:
            self.report_error(SemanticError, "Missing group name in group declaration", token=items[1] if len(items)>1 else None)
            return items
        group_members = {}
        if isinstance(items[3], dict):
            group_members = items[3]

        self.symbol_table.add(group_name, {
            "type": "group",
            "members": group_members
        })
        return items

    def group_members(self, items):
        member_dict = {}
        for m in items:
            if isinstance(m, tuple) and len(m) == 2:
                key, val_info = m
                if key[0] == "text":
                    key_str = str(key[1])
                else:
                    key_str = str(key[1])
                member_dict[key_str] = val_info
        return member_dict

    def member(self, items):
        if len(items) == 2:
            return (items[0], items[1])
        return items

    # -----------------------
    # Assignments
    # -----------------------
    # var_assign: IDENTIFIER group_or_list? assign_op variable_value SEMICOLON
    def var_assign(self, items):
        if not items:
            return items

        identifier_token = items[0]
        identifier = identifier_token.value
        variable_info = self.symbol_table.get(identifier)
        if variable_info is None:
            self.report_error(UndefinedIdentifierError, identifier, token=identifier_token)
            return items

        if variable_info.get("fixed", False):
            self.report_error(SemanticError, f"Cannot reassign fixed variable '{identifier}'", token=identifier_token)

        new_value_type, _ = items[-1]
        declared_type = variable_info.get("var_type", "unknown")

        if len(items) > 1 and isinstance(items[1], tuple):
            usage_type = items[1][0]
            if usage_type == "list_index":
                if declared_type != "list":
                    self.report_error(TypeMismatchError, "list", declared_type, token=identifier_token)
                index_type = items[1][1]
                if index_type != "integer":
                    self.report_error(TypeMismatchError, "integer", index_type, token=identifier_token)
            elif usage_type == "group_access":
                if variable_info.get("type") != "group":
                    self.report_error(SemanticError, f"Variable '{identifier}' is not a group; cannot use '{{}}' syntax", token=identifier_token)
                else:
                    group_members = variable_info.get("members", {})
                    key_type = items[1][1]
                    key_val = items[1][2]
                    if key_type != "text":
                        self.report_error(SemanticError, f"Group field must be a string key, found {key_type}", token=identifier_token)
                    else:
                        key_str = str(key_val)
                        if key_str not in group_members:
                            self.report_error(SemanticError, f"Group '{identifier}' has no field '{key_str}'", token=identifier_token)
        else:
            if declared_type != "unknown" and new_value_type != "error":
                if declared_type != new_value_type:
                    self.report_error(TypeMismatchError, declared_type, new_value_type, token=identifier_token)
                if declared_type == "unknown":
                    variable_info["var_type"] = new_value_type

        return items

    # var_assign_each: IDENTIFIER assign_op expression
    def var_assign_each(self, items):
        return self.var_assign(items)

    # -----------------------
    # Group or List usage
    # -----------------------
    # group_or_list: (LSQB expression RSQB) | (LBRACE expression RBRACE)
    def group_or_list(self, items):
        if len(items) == 3:
            bracket_open = items[0]
            expr = items[1]
            if isinstance(bracket_open, Token) and bracket_open.type == "LSQB":
                return ("list_index", expr[0], expr[1])
            elif isinstance(bracket_open, Token) and bracket_open.type == "LBRACE":
                return ("group_access", expr[0], expr[1])
        return ("error", None)

    # variable_value: get_expr | (LSQB list_value RSQB) | expression
    def list_value(self, items):
        return [ (t, v) for (t, v) in items ]

    def list_creation(self, items):
        if len(items) == 1 and isinstance(items[0], list):
            return ("list", items[0])
        return ("list", [])  # fallback

    # -----------------------
    # Functions
    # -----------------------
    # func_definition: FUNC IDENTIFIER LPAREN param_list? RPAREN LBRACE function_program throw_statement? RBRACE SEMICOLON?
    def func_definition(self, items):
        func_name = None
        param_list_items = []
        idx = 0
        while idx < len(items):
            if isinstance(items[idx], Token) and items[idx].type == "IDENTIFIER":
                func_name = items[idx].value
                break
            idx += 1

        if any(isinstance(x, list) and all(isinstance(e, Token) for e in x) for x in items):
            for x in items:
                if isinstance(x, list) and all(isinstance(e, Token) for e in x):
                    param_list_items = x
                    break

        param_count = len(param_list_items)

        self.symbol_table.add(func_name, {
            "type": "function",
            "param_count": param_count
        })

        self.symbol_table.enter_scope()

        for p in param_list_items:
            param_name = p.value
            self.symbol_table.add(param_name, {
                "type": "variable",
                "fixed": False,
                "var_type": "unknown"
            })

        self.symbol_table.exit_scope()
        return items

    # param_list: IDENTIFIER (COMMA IDENTIFIER)*
    def param_list(self, items):
        return items

    # statement_func_call: IDENTIFIER func_call SEMICOLON
    def statement_func_call(self, items):
        if len(items) < 2:
            return items
        func_token = items[0]
        func_name = func_token.value
        call_args = items[1]
        info = self.symbol_table.get(func_name)
        if not info:
            self.report_error(UndefinedIdentifierError, func_name, token=func_token)
            return items
        if info.get("type") != "function":
            self.report_error(SemanticError, f"'{func_name}' is not a function", token=func_token)
            return items

        declared_count = info.get("param_count", 0)
        actual_count = len(call_args) if isinstance(call_args, list) else 0
        if actual_count != declared_count:
            self.report_error(SemanticError,
                f"Function '{func_name}' expects {declared_count} argument(s), but got {actual_count}",
                token=func_token
            )

        return items

    # func_call: LPAREN args? RPAREN
    def func_call(self, items):
        if not items:
            return []
        elif len(items) == 1 and isinstance(items[0], list):
            return items[0]
        return []

    # args: (expression (COMMA expression)*)?
    def args(self, items):
        return items

    # ---------------
    # Expressions
    # ---------------
    # expression: logical_or_expr
    def expression(self, items):
        return items[-1] if items else ("empty", None)

    def additive_expr(self, items):
        if len(items) == 1:
            return self._get_value(items[0])
        result = self._get_value(items[0])
        result_type = result[0]
        i = 1
        while i < len(items):
            right = self._get_value(items[i+1])
            right_type = right[0]
            if self.is_numeric(result_type) and self.is_numeric(right_type):
                pass
            else:
                self.report_error(TypeMismatchError, result_type, right_type)
                result_type = "error"
            i += 2
        return (result_type, None)

    def multiplicative_expr(self, items):
        if len(items) == 1:
            return items[0]
        result_type = items[0][0]
        i = 1
        while i < len(items):
            right_type = items[i+1][0]
            if self.is_numeric(result_type) and self.is_numeric(right_type):
                pass
            else:
                self.report_error(TypeMismatchError, result_type, right_type)
                result_type = "error"
            i += 2
        return (result_type, None)

    def relational_expr(self, items):
        if len(items) == 1:
            return items[0]
        left_type = items[0][0]
        i = 1
        while i < len(items):
            right_type = items[i+1][0]
            if self.is_numeric(left_type) and self.is_numeric(right_type):
                left_type = "state"
            else:
                self.report_error(TypeMismatchError, "numeric", f"{left_type} and {right_type}")
                left_type = "error"
            i += 2
        return (left_type, None)

    def equality_expr(self, items):
        if len(items) == 1:
            return items[0]
        left_type = items[0][0]
        i = 1
        while i < len(items):
            right_type = items[i+1][0]
            if left_type == right_type:
                left_type = "state"
            else:
                self.report_error(TypeMismatchError, left_type, right_type)
                left_type = "error"
            i += 2
        return (left_type, None)

    def logical_and_expr(self, items):
        if len(items) == 1:
            return items[0]
        for it in items:
            if it[0] != "state":
                self.report_error(TypeMismatchError, "state", it[0])
                return ("error", None)
        return ("state", None)

    def logical_or_expr(self, items):
        if len(items) == 1:
            return items[0]
        for it in items:
            if it[0] != "state":
                self.report_error(TypeMismatchError, "state", it[0])
                return ("error", None)
        return ("state", None)

    def pre_expr(self, items):
        if len(items) == 1:
            return items[0]
        op_token = items[0]
        expr = items[1]
        if op_token.type == "BANG":
            if expr[0] != "state":
                self.report_error(TypeMismatchError, "state", expr[0], token=op_token)
                return ("error", None)
            return ("state", None)
        elif op_token.type == "TILDE":
            if expr[0] != "integer":
                self.report_error(TypeMismatchError, "integer", expr[0], token=op_token)
                return ("error", None)
            return ("integer", None)
        return expr

    def typecast_expression(self, items):
        if len(items) < 2:
            return ("error", None)
        target_type_token = items[0]
        expr = items[1]
        target_type = target_type_token.value.lower()
        return (target_type, None)

    # ---------------
    # get_expr
    # ---------------
    def get_expr(self, items):
        if not items:
            return ("unknown", None)
        else:
            return ("unknown", None)

    # ---------------
    # Statement forms
    # ---------------
    def statement(self, items):
        return items

    def show_statement(self, items):
        return items

    # ---------------
    # Program & pass-through
    # ---------------
    def program(self, items):
        return items

    def function_program(self, items):
        return items

    def declaration(self, items):
        return items

    # ---------------
    # Control flow expansions
    # ---------------
    def control_flow(self, items):
        return items