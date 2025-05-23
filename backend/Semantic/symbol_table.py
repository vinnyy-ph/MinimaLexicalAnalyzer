# symbol_table.py

class SymbolTable:
    def __init__(self):
        # Each element in the list represents a scope (a dictionary mapping names to symbol info)
        self.scopes = []

    def enter_scope(self):
        self.scopes.append({})

    def exit_scope(self):
        if self.scopes:
            self.scopes.pop()

    def declare(self, name, info):
        """Declare a symbol in the current scope. If it already exists, raise a redeclaration error."""
        current_scope = self.scopes[-1] if self.scopes else {}
        if name in current_scope:
            from semantic_errors import RedeclarationError
            raise RedeclarationError(name)
        current_scope[name] = info

    def lookup(self, name):
        """Search for a symbol from innermost to outermost scope."""
        for scope in reversed(self.scopes):
            if name in scope:
                return scope[name]
        return None
