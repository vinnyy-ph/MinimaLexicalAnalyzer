# semantic_errors.py

class SemanticError(Exception):
    """Base class for semantic errors."""
    pass

class RedeclarationError(SemanticError):
    def __init__(self, name, line=None, column=None):
        msg = f"Redeclaration error: '{name}' is already declared."
        if line is not None and column is not None:
            msg += f" (Line {line}, Column {column})"
        super().__init__(msg)
        self.name = name
        self.line = line
        self.column = column

class UndefinedError(SemanticError):
    def __init__(self, name, line=None, column=None):
        msg = f"Undefined error: '{name}' is not declared."
        if line is not None and column is not None:
            msg += f" (Line {line}, Column {column})"
        super().__init__(msg)
        self.name = name
        self.line = line
        self.column = column
