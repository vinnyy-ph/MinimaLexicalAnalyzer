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

    messages = []

    # Helper: check for unmatched bracket up to the error column.
    def has_unmatched(opening, closing):
        stack_count = 0
        for ch in code:  # use full code instead of code[:max(column-1, 0)]
            if ch == opening:
                stack_count += 1
            elif ch == closing and stack_count > 0:
                stack_count -= 1
        return stack_count > 0

    # # Here we assume that if SEMICOLON (or ";" token) is in expected_tokens, then a semicolon might be missing.
    # if ("SEMICOLON" in expected_tokens or ";" in expected_tokens):
    #     # A simple heuristic: if the trimmed code does not end with a semicolon.
    #     if not code.rstrip().endswith(";"):
    #         messages.append("Missing semicolon ';'")

    # Filter expected tokens: only include a closing token if its corresponding opening appears in the code
    def has_left(opening):
        return opening in code[:max(column-1, 0)]

    filtered_expected = []
    for token in expected_tokens:
        if token in {"RSQB", "]"} and not has_unmatched('[', ']'):
            continue
        if token in {"RBRACE", "}"} and not has_unmatched('{', '}'):
            continue
        if token in {"RPAREN", ")"} and not has_unmatched('(', ')'):
            continue
        filtered_expected.append(token)

    # Always include the full expected tokens for context (filtered)
    messages.append("Expected tokens: " + ", ".join(filtered_expected))
    
    final_message = " ".join(messages)
    return {
        "message": final_message,
        "rawMessage": error_msg,
        "expected": filtered_expected,
        "unexpected": unexpected_token,
        "line": line,
        "column": column,
        "value": ""
    }