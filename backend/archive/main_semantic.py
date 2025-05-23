from syntax_analyzer import analyze_syntax, parser
from semantic_analyzer import SemanticAnalyzer

def main():
    # Sample source code to test your language.
    code = '''\
var a = b / 2;
var a; 

    '''

    # --- Syntax Analysis ---
    success, error_msg = analyze_syntax(code)
    if not success:
        print("Syntax Error:")
        print(error_msg)
        return

    # Parsing to obtain the AST (parse tree)
    tree = parser.parse(code)
    print("Syntax Analysis succeeded!")
    print("Parse Tree:")
    print(tree.pretty())

    # --- Semantic Analysis ---
    semantic_analyzer = SemanticAnalyzer()
    try:
        # Transform the tree (this walk will update the symbol table)
        annotated_tree = semantic_analyzer.transform(tree)
        print("Semantic Analysis succeeded!")
        print("Annotated Tree:")
        if isinstance(annotated_tree, list):
            for t in annotated_tree:
                try:
                    print(t.pretty())
                except AttributeError:
                    print(t)
        else:
            try:
                print(annotated_tree.pretty())
            except AttributeError:
                print(annotated_tree)

        # Optionally, print out the symbol table
        print("\nSymbol Table:")
        for name, info in semantic_analyzer.symbol_table.items():
            print(f"  {name}: {info}")

    except Exception as e:
        print("Semantic Analysis Error:")
        print(e)

if __name__ == '__main__':
    main()