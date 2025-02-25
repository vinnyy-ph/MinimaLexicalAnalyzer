from lark import Lark, UnexpectedToken, UnexpectedCharacters, UnexpectedInput, LarkError
from syntax_errors import process_syntax_error  

TOKEN_MAP = {
    "LPAREN": "(",
    "RPAREN": ")",
    "LSQB": "[",
    "RSQB": "]",
    "LBRACE": "{",
    "RBRACE": "}",
    "SEMICOLON": ";",
    "BANG": "!",
    "TILDE": "~",
    "EQUAL": "=",
    "NOTEQUAL": "!=",
    "EQEQUAL": "==",
    "LESSEQUAL": "<=",
    "GREATEREQUAL": ">=",
    "VAR": "var",
    "FIXED": "fixed",
    "GROUP": "group",
    "GET": "get",
    "THROW": "throw",
    "SHOW": "show",
    "CHECKIF": "checkif",
    "RECHECK": "recheck",
    "OTHERWISE": "otherwise",
    "SWITCH": "switch",
    "CASE": "case",
    "DEFAULT": "default",
    "EXIT": "exit",
    "NEXT": "next",
    "EACH": "each",
    "REPEAT": "repeat",
    "DO": "do",
    "EMPTY": "empty",
    "FUNC": "func",
    "OR_OP": "||",
    "AND_OP": "&&",
    "EQ_OP": "==",
    "NEQ_OP": "!=",
    "LT": "<",
    "LE": "<=",
    "GT": ">",
    "GE": ">=",
    "PLUS": "+",
    "MINUS": "-",
    "STAR": "*",
    "SLASH": "/",
    "PERCENT": "%",
    "INC_OP": "++",
    "DEC_OP": "--",
    "ASSIGN": "=",
    "ADD_ASSIGN": "+=",
    "SUB_ASSIGN": "-=",
    "MUL_ASSIGN": "*=",
    "DIV_ASSIGN": "/=",
    "MOD_ASSIGN": "%=",
    "COMMA": ",",
    "COLON": ":",
    # The token for semicolon appears twice in your map; that’s fine.
}

parser = Lark.open("grammar.lark", start="start", parser="lalr")

def analyze_syntax(code):
    try:
        parse_tree = parser.parse(code)
        return (True, None)
    except UnexpectedToken as ut:
        line = ut.line
        column = ut.column

        literals = []
        keywords = []
        symbols = []
        others = []

        # Define sets for classification
        literal_tokens = {"INTEGER", "POINT", "STATE", "TEXT"}
        keyword_tokens = {
            "VAR", "FIXED", "GROUP", "GET", "THROW", "SHOW", "CHECKIF",
            "RECHECK", "OTHERWISE", "SWITCH", "CASE", "DEFAULT", "EXIT",
            "NEXT", "EACH", "REPEAT", "DO", "EMPTY", "FUNC"
        }
        symbol_tokens = {
            "LPAREN", "RPAREN", "LSQB", "RSQB", "LBRACE", "RBRACE",
            "SEMICOLON", "BANG", "TILDE", "EQUAL", "NOTEQUAL", "EQEQUAL",
            "LESSEQUAL", "GREATEREQUAL", "OR_OP", "AND_OP", "LT", "LE",
            "GT", "GE", "PLUS", "MINUS", "STAR", "SLASH", "PERCENT",
            "INC_OP", "DEC_OP", "ASSIGN", "ADD_ASSIGN", "SUB_ASSIGN", "MUL_ASSIGN",
            "DIV_ASSIGN", "COMMA", "COLON"
        }

        for token in ut.expected:
            if token in TOKEN_MAP:
                token_str = TOKEN_MAP[token]
                if token in literal_tokens:
                    literals.append(token_str)
                elif token in keyword_tokens:
                    keywords.append(token_str)
                elif token in symbol_tokens:
                    symbols.append(token_str)
                else:
                    others.append(token_str)
            else:
                others.append(token)

        expected_all = literals + keywords + symbols + others
        raw_msg = (
            f"Syntax error at line {line}, column {column}.\n"
            "Expected tokens:\n"
            f"  Literals: {literals}\n"
            f"  Keywords: {keywords}\n"
            f"  Symbols: {symbols}\n"
            f"  Others: {others}"
        )
        processed_error = process_syntax_error(
            raw_msg,
            line,
            column,
            expected_all,
            ut.token,
            code
        )
        return (False, processed_error)
