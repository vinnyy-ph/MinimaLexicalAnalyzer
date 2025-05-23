# test.py

from syntax_analyzer import analyze_syntax, parser
from semantic_analyzer import SemanticAnalyzer
import sys

def main():
    code = """
    var a = "hello" + b;
    """

    # First, perform syntax analysis.
    valid, error = analyze_syntax(code)
    if not valid:
        print("Syntax error:", error)
        sys.exit(1)
    
    # Get the parse tree from the parser.
    try:
        tree = parser.parse(code)
        print("Syntax Analysis succeeded!")
        print("Parse Tree:")
        print(tree.pretty())
        
    except Exception as e:
        print("Parsing failed:", e)
        sys.exit(1)

    # Run semantic analysis.
    analyzer = SemanticAnalyzer()
    try:
        analyzer.analyze(tree)
        print("Semantic analysis passed. No redeclaration errors found.")
    except Exception as e:
        print("Semantic error detected:", e)

if __name__ == '__main__':
    main()