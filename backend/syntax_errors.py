#syntax_errors.py
def process_syntax_error(
    error_msg: str,
    line: int = 0,
    column: int = 0,
    expected_tokens=None,
    unexpected_token=None,
    code=""
) -> dict:
    if expected_tokens is None:
        expected_tokens = []

    # Helper: checks if there's an unmatched bracket of a certain kind
    def has_unmatched(opening, closing):
        stack_count = 0
        for ch in code[:column]:
            if ch == opening:
                stack_count += 1
            elif ch == closing and stack_count > 0:
                stack_count -= 1
        return stack_count > 0

    # If we detect unmatched parentheses/brackets/braces, report them.
    # Otherwise, just return the full expected tokens list.
    if "RSQB" in expected_tokens:
        # Check if there's an unmatched '[' in the code before this point
        if has_unmatched('[', ']'):
            return {
                "message": "Missing closing square bracket ']'",
                "rawMessage": error_msg,
                "expected": expected_tokens,
                "unexpected": unexpected_token,
                "line": line,
                "column": column,
                "value": ""
            }

    if "RBRACE" in expected_tokens:
        # Check if there's an unmatched '{'
        if has_unmatched('{', '}'):
            return {
                "message": "Missing closing brace '}'",
                "rawMessage": error_msg,
                "expected": expected_tokens,
                "unexpected": unexpected_token,
                "line": line,
                "column": column,
                "value": ""
            }

    if "RPAREN" in expected_tokens:
        # Check if there's an unmatched '('
        if has_unmatched('(', ')'):
            return {
                "message": "Missing closing parenthesis ')'",
                "rawMessage": error_msg,
                "expected": expected_tokens,
                "unexpected": unexpected_token,
                "line": line,
                "column": column,
                "value": ""
            }

    # If no real unmatched bracket was found, or there's no other special case,
    # just list all of the expected tokens.
    return {
        "message": "Expected tokens: " + ", ".join(expected_tokens),
        "rawMessage": error_msg,
        "expected": expected_tokens,
        "unexpected": unexpected_token,
        "line": line,
        "column": column,
        "value": ""
    }
