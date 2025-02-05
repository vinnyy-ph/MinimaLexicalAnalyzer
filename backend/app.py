from flask import Flask, request, jsonify
from flask_cors import CORS
from lexer import Lexer 

app = Flask(__name__)
CORS(app)  

@app.route('/analyze', methods=['POST'])
def analyze():
    data = request.get_json()
    code = data.get('code', '')
    lexer = Lexer(code)
    
    tokens = []
    while True:
        token = lexer.process_code_input()
        if token is None:
            break
        else:
            tokens.append({
                'type': token.type,
                'value': token.value,
                'line': token.line,
                'column': token.column
            })
    # Retrieve errors from the lexer
    errors = [error.to_dict() for error in lexer.errors]
    
    response = {
        'tokens': tokens,
        'errors': errors
    }
    return jsonify(response)

if __name__ == '__main__':
    app.run(debug=True)
