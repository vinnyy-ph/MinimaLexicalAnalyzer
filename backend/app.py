from flask import Flask, request, jsonify
from flask_cors import CORS
from lexer import Lexer  # Use FSMLexer here

app = Flask(__name__)
CORS(app)

@app.route('/analyze', methods=['POST'])
def analyze():
    data = request.get_json()
    code = data.get('code', '')
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

    errors = [error.to_dict() for error in lexer.errors]

    return jsonify({'tokens': tokens, 'errors': errors})

if __name__ == '__main__':
    app.run(debug=True)