from lexer import Lexer

def main():
    code = """# TEST CODE
    x = 10; # Inline comment
    _a = 20; # Invvalid identifier
    """
    lexer = Lexer(code)
    token = lexer.process_code_input()
    while token:
        print(token)
        token = lexer.process_code_input()

if __name__ == "__main__":
    main()