# semantic_analyzer.py

from lark import Tree
from symbol_table import SymbolTable
from semantic_errors import RedeclarationError, UndefinedError

class SemanticAnalyzer:
    def __init__(self):
        self.symbol_table = SymbolTable()

    def analyze(self, tree: Tree):
        # Start at the global scope.
        self.symbol_table.enter_scope()
        self.visit(tree)
        self.symbol_table.exit_scope()
        return True

    def visit(self, node):
        # If the node is a Tree, dispatch to the appropriate method.
        if isinstance(node, Tree):
            method_name = f'visit_{node.data}'
            visitor = getattr(self, method_name, self.generic_visit)
            return visitor(node)
        # Tokens do not need visiting, but if it's an identifier token we can check its declaration.
        if hasattr(node, 'type') and node.type == "IDENTIFIER":
            self.check_identifier(node)
        return node

    def generic_visit(self, node):
        # Default: visit all children.
        for child in node.children:
            self.visit(child)

    def visit_program(self, node):
        # 'program' can contain many declarations/statements.
        for child in node.children:
            self.visit(child)

    def visit_varlist_declaration(self, node):
        # Grammar: VAR IDENTIFIER var_init? var_list_declaration_tail* SEMICOLON
        # The first identifier is always at position 1.
        var_token = node.children[1]
        var_name = var_token.value
        # Attempt to declare the variable.
        self.symbol_table.declare(var_name, {"kind": "var"})
        # Visit the optional initializer if present.
        for child in node.children[2:]:
            self.visit(child)
        
        # Handle any additional identifiers in the tail.
        # Assuming each tail is a tree with structure: COMMA, IDENTIFIER, (var_init)?
        for child in node.children:
            if hasattr(child, 'data') and child.data == 'var_list_declaration_tail':
                # The identifier should be the second child.
                tail_identifier = child.children[1]
                tail_name = tail_identifier.value
                self.symbol_table.declare(tail_name, {"kind": "var"})
                # Visit initializer if exists.
                for subchild in child.children[2:]:
                    self.visit(subchild)

    def visit_fixed_declaration(self, node):
        # Grammar: FIXED IDENTIFIER ASSIGN variable_value fixed_declaration_tail* SEMICOLON
        fixed_token = node.children[1]
        fixed_name = fixed_token.value
        self.symbol_table.declare(fixed_name, {"kind": "fixed"})
        # Visit variable_value and any tail declarations.
        for child in node.children[2:]:
            self.visit(child)

        # fixed_declaration_tail: COMMA IDENTIFIER ASSIGN variable_value
        for child in node.children:
            if hasattr(child, 'data') and child.data == 'fixed_declaration_tail':
                tail_identifier = child.children[1]
                tail_name = tail_identifier.value
                self.symbol_table.declare(tail_name, {"kind": "fixed"})
                # Visit the initializer.
                for subchild in child.children[2:]:
                    self.visit(subchild)

    def visit_group_declaration(self, node):
        # Grammar: GROUP IDENTIFIER LBRACE group_members RBRACE SEMICOLON?
        group_token = node.children[1]
        group_name = group_token.value
        self.symbol_table.declare(group_name, {"kind": "group"})
        # You can choose to analyze group members further if needed.
        for child in node.children[2:]:
            self.visit(child)

    def visit_func_definition(self, node):
        # Grammar: FUNC IDENTIFIER LPAREN param_list? RPAREN LBRACE function_program throw_statement? RBRACE SEMICOLON?
        func_token = node.children[1]
        func_name = func_token.value
        self.symbol_table.declare(func_name, {"kind": "function"})
        
        # Create a new scope for the function body.
        self.symbol_table.enter_scope()
        # Process parameters if they exist.
        for child in node.children:
            if hasattr(child, 'data') and child.data == 'param_list':
                # For each parameter (IDENTIFIER), declare it in the function scope.
                for param in child.children:
                    if param.type == "IDENTIFIER":
                        self.symbol_table.declare(param.value, {"kind": "parameter"})
        # Visit the function body.
        for child in node.children:
            self.visit(child)
        self.symbol_table.exit_scope()

    def check_identifier(self, token):
        """
        Check if an identifier is declared.
        If not, raise an UndefinedError.
        """
        if self.symbol_table.lookup(token.value) is None:
            raise UndefinedError(token.value, getattr(token, 'line', None), getattr(token, 'column', None))

    def visit_identifier_usage(self, node):
        """
        Visitor for identifier usage nodes.
        Assumes the identifier token is the first child.
        """
        identifier_token = node.children[0]
        self.check_identifier(identifier_token)
        # Continue processing any additional children if needed.
        for child in node.children[1:]:
            self.visit(child)