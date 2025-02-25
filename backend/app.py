from flask import Flask, request, jsonify
from flask_cors import CORS
from minima_lexer import Lexer
from syntax_analyzer import analyze_syntax

app = Flask(__name__)
CORS(app)

@app.route('/analyzeFull', methods=['POST'])
def analyze_full():
    data = request.get_json()
    code = data.get('code', '')

    # Lexical pass
    lexer = Lexer(code)
    tokens = []
    while True:
        token = lexer.get_next_token()
        if token is None:
            break
        tokens.append({
            'type': token.type,
            'value': token.value,
            'line': token.line,
            'column': token.column
        })
    lexical_errors = [error.to_dict() for error in lexer.errors]

    # If there are lexical errors, do not run syntax analysis.
    if lexical_errors:
        syntax_errors = [{
            "message": "Lexical errors were detected. Please resolve them before running syntax analysis."
        }]
    else:
        success, syntax_error_msg = analyze_syntax(code)
        syntax_errors = [] if success else [syntax_error_msg]

    return jsonify({
        'tokens': tokens,
        'lexicalErrors': lexical_errors,
        'syntaxErrors': syntax_errors
    })

if __name__ == '__main__':
    app.run(debug=True)