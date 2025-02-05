from tokens import Token as T
from errors import InvalidIdentifierError, InvalidDelimiterError, LexerError, InvalidIntegerError, InvalidPointError, InvalidSymbolError

class Lexer:
    def __init__(self, input_code):
        self.code = input_code.replace('\r\n', '\n').replace('\r', '\n')
        self.position = 0  
        self.line = 1       
        self.column = 1     
        self.errors = []     # empty list to store errors
        self.symbols = ['+', '-', '*', '/', '%', '=', '!', '>', '<', '&', '|', '{', '}', '(', ')', '[', ']', ':', ',', ';']
        self.valid_delimiters_identifier = [' ', '\n', '\t', ';', ',', ')', '}', '(', '{', '[', ']', ':', '=', '+', '-', '*', '/', '%', '!', '>', '<', '&', '|']
        self.valid_delimiters_numeric = [' ', '\t', '+', '-', '*', '/', '%',  ',', '==', '!=', '<', '>', ')', ']', '}', ';', ':', '|', '&',]
        self.valid_delimiters_dict = {
            'get': [ ' ', '(' ],
            'show': [ ' ', '(' ],
            'integer': [ ' ', '(' ],
            'point': [ ' ', '(' ],
            'texts': [ ' ', '(' ],
            'state': [ ' ', '(' ],
            'group': [ ' ' ],
            'fixed': [ ' ' ],
            'checkif': [ ' ', '(' ],
            'recheck': [ ' ', '(' ],
            'otherwise': [ ' ', '\n', '\t', '{' ],
            'switch': [ ' ', '(' ],
            'case': [ ' ' ],
            'default': [ ' ', ':' ],
            'each': [ ' ', '(' ],
            'repeat': [ ' ', '(' ],
            'do': [ ' ', '{' ],
            'exit': [ ' ', ';' ],
            'next': [ ' ', ';' ],
            'func': [ ' ' ],
            'throw': [ ' ' ],
            'empty': [ ' ', ';',',',':' ],
            'STATELITERAL': [ ' ', ')', '&', ',', ';', '}', '|', '=', '!' ],
            # 'NO': [ ' ', ')', '&&', '!=', ',', ';', '}', '||', '==' ],
        }
        self.valid_delimiters_symbol_dict = {
            '=':  [' ', '"', '(', '{', '~', 'Y', 'N'] + list('abcdefghijklmnopqrstuvwxyz0123456789'), 
            '==': [' ', '(', '~', '"', 'Y', 'N'] + list('abcdefghijklmnopqrstuvwxyz0123456789'), 
            '+':  [' ', '(', '~', '"'] + list('abcdefghijklmnopqrstuvwxyz0123456789'), 
            '++': [' ', ')', ';', '}', ',', '<'], 
            '+=': [' ', '('] + list('abcdefghijklmnopqrstuvwxyz0123456789'), 
            '-':  [' ', '(', '~'] + list('abcdefghijklmnopqrstuvwxyz0123456789'), 
            '--': [' ', ')', ';', '}', ','], 
            '-=': [' ', '('] + list('abcdefghijklmnopqrstuvwxyz0123456789'), 
            '*':  [' ', '(', '~'] + list('abcdefghijklmnopqrstuvwxyz0123456789'), 
            '*=': [' ', '('] + list('abcdefghijklmnopqrstuvwxyz0123456789'), 
            '/':  [' ', '(', '~'] + list('abcdefghijklmnopqrstuvwxyz0123456789'), 
            '/=': [' ', '('] + list('abcdefghijklmnopqrstuvwxyz0123456789'), 
            '%':  [' ', '(', '~'] + list('abcdefghijklmnopqrstuvwxyz0123456789'), 
            '!':  [' ', '(', 'Y', 'N'] + list('abcdefghijklmnopqrstuvwxyz0123456789'), 
            '!=': [' ', '(', '~', '"', 'Y', 'N'] + list('abcdefghijklmnopqrstuvwxyz0123456789'), 
            '>':  [' ', '(', '~'] + list('abcdefghijklmnopqrstuvwxyz0123456789'), 
            '>=': [' ', '(', '~'] + list('abcdefghijklmnopqrstuvwxyz0123456789'), 
            '<':  [' ', '(', '~'] + list('abcdefghijklmnopqrstuvwxyz0123456789'), 
            '<=': [' ', '(', '~'] + list('abcdefghijklmnopqrstuvwxyz0123456789'), 
            '&&': [' ', '(', 'Y', 'N', '!'] + list('abcdefghijklmnopqrstuvwxyz0123456789'), 
            '||': [' ', '(', 'Y', 'N'] + list('abcdefghijklmnopqrstuvwxyz0123456789'), 
            '{':  [' ', '\n', '\t', '"', 'Y', 'N', '~', '(','{','}'] + list('abcdefghijklmnopqrstuvwxyz0123456789'), 
            '}':  [' ', '\n', '\t', '=', ';', 'checkif', 'recheck', 'otherwise', '{','}', ','], 
            '(':  [' ', '~', '"', '(', 'Y', 'N',')'] + list('abcdefghijklmnopqrstuvwxyz0123456789'), 
            ')':  [' ', '\n', '\t', ';', ')', '{', '+', '-', '*', '/', '%', '==', '!=', '<', '>', '<=', '>=', '&', '|', '!', ',', '}'], 
            '[':  [' ', '"'] + list('abcdefghijklmnopqrstuvwxyz0123456789'), 
            ']':  [' ', ')', ';', '+', '-', '*', '/', '%', '=', '+=', '-=', '/=', '*=', '==', '!=', '<', '>', '<=', '>='], 
            ':':  [' ', '\n', '\t', '{', '~', '"', 'Y', 'N'] + list('abcdefghijklmnopqrstuvwxyz0123456789'), 
            '~':  [' ', '('] + list('abcdefghijklmnopqrstuvwxyz0123456789'), 
            ',':  [' ', '\n', '\t', '"', '(', '~', 'Y', 'N'] + list('abcdefghijklmnopqrstuvwxyz0123456789'), 
            ';':  [' ', '\n', '\t', '#'] + list('abcdefghijklmnopqrstuvwxyz'),
        }
        self.current_char = self.code[self.position] if self.code else None
        
    # Method to move to the next character in the code
    def advance(self):
        # If the current character is a newline
        if self.current_char == '\n':
            self.line += 1      
            self.column = 0    

        self.position += 1      # Move to the next character in the code
        self.column += 1        # Move to the next column

        # If the position is within the bounds of the code, update current_char to the next character
        if self.position < len(self.code):
            self.current_char = self.code[self.position]
        else:
            # If we've reached the end of the code, set current_char to None
            self.current_char = None  # End of input

        # If current_char is None, it means we've reached the end of the input code
        if self.current_char is None:
            return None

    def tokenize_space(self):
        start_line = self.line                 
        start_column = self.column             
        space = ''                              
        count = 0                              

        # Loop to consume spaces (up to 4)
        while self.current_char == ' ' and count < 4:
            space += self.current_char          
            self.advance()                       
            count += 1                          

        # 4 spaces = 1 tab token
        if count == 4:
            return T('TAB', space, start_line, start_column)  
        else:
            return T('SPACE', space, start_line, start_column) 
        
    def tokenize_newline(self):
        start_line = self.line                 
        start_column = self.column            
        newline = "\\n"                         
        self.advance()                          
        return T('NEWLINE', newline, start_line, start_column)

    def tokenize_comment(self):
        start_line = self.line                 
        start_column = self.column             
        comment = ''                             # empty string to accumulate the comment text

        # Loop to collect characters until a newline or the end of the input
        while self.current_char is not None and self.current_char != '\n':
            comment += self.current_char         # Add the current character to the comment string
            self.advance()                       # Advance to the next character

        # Return a SINGLE_LINE_COMMENT token with the accumulated comment text
        return T('COMMENT', comment, start_line, start_column)

    def tokenize_keyword(self, value):

        if value[0] == 'c':
            if len(value) == 4 and value[1] == 'a' and value[2] == 's' and value[3] == 'e':
                return 'case'
            elif len(value) == 7 and value[1] == 'h' and value[2] == 'e' and value[3] == 'c' and value[4] == 'k' and value[5] == 'i' and value[6] == 'f':
                return 'checkif'

        elif value[0] == 'd':
            if len(value) == 7 and value[1] == 'e' and value[2] == 'f' and value[3] == 'a' and value[4] == 'u' and value[5] == 'l' and value[6] == 't':
                return 'default'
            elif len(value) == 2 and value[1] == 'o':
                return 'do'

        elif value[0] == 'e':
            if len(value) == 4 and value[1] == 'a' and value[2] == 'c' and value[3] == 'h':
                return 'each'
            elif len(value) == 5 and value[1] == 'm' and value[2] == 'p' and value[3] == 't' and value[4] == 'y':
                return 'empty'
            elif len(value) == 4 and value[1] == 'x' and value[2] == 'i' and value[3] == 't':
                return 'exit'

        elif value[0] == 'f':
            if len(value) == 5 and value[1] == 'i' and value[2] == 'x' and value[3] == 'e' and value[4] == 'd':
                return 'fixed'
            elif len(value) == 4 and value[1] == 'u' and value[2] == 'n' and value[3] == 'c':
                return 'func'

        elif value[0] == 'g':
            if len(value) == 3 and value[1] == 'e' and value[2] == 't':
                return 'get'
            elif len(value) == 5 and value[1] == 'r' and value[2] == 'o' and value[3] == 'u' and value[4] == 'p':
                return 'group'

        elif value[0] == 'i':
            if len(value) == 7 and value[1] == 'n' and value[2] == 't' and value[3] == 'e' and value[4] == 'g' and value[5] == 'e' and value[6] == 'r':
                return 'integer'

        elif value[0] == 'n':
            if len(value) == 4 and value[1] == 'e' and value[2] == 'x' and value[3] == 't':
                return 'next'

        elif value[0] == 'o':
            if len(value) == 9 and value[1] == 't' and value[2] == 'h' and value[3] == 'e' and value[4] == 'r' and value[5] == 'w' and value[6] == 'i' and value[7] == 's' and value[8] == 'e':
                return 'otherwise'

        elif value[0] == 'p':
            if len(value) == 5 and value[1] == 'o' and value[2] == 'i' and value[3] == 'n' and value[4] == 't':
                return 'point'

        elif value[0] == 'r':
            if len(value) == 7 and value[1] == 'e' and value[2] == 'c' and value[3] == 'h' and value[4] == 'e' and value[5] == 'c' and value[6] == 'k':
                return 'recheck'
            elif len(value) == 6 and value[1] == 'e' and value[2] == 'p' and value[3] == 'e' and value[4] == 'a' and value[5] == 't':
                return 'repeat'

        elif value[0] == 's':
            if len(value) == 4 and value[1] == 'h' and value[2] == 'o' and value[3] == 'w':
                return 'show'
            elif len(value) == 5 and value[1] == 't' and value[2] == 'a' and value[3] == 't' and value[4] == 'e':
                return 'state'
            elif len(value) == 6 and value[1] == 'w' and value[2] == 'i' and value[3] == 't' and value[4] == 'c' and value[5] == 'h':
                return 'switch'

        elif value[0] == 't':
            if len(value) == 5 and value[1] == 'e' and value[2] == 'x' and value[3] == 't' and value[4] == 's':
                return 'texts'
            elif len(value) == 5 and value[1] == 'h' and value[2] == 'r' and value[3] == 'o' and value[4] == 'w':
                return 'throw'

        elif value[0] == 'Y':
            if len(value) == 3 and value[1] == 'E' and value[2] == 'S':
                return 'STATELITERAL'

        elif value[0] == 'N':
            if len(value) == 2 and value[1] == 'O':
                return 'STATELITERAL'

        return None

    def invalid_identifier(self):
        start_line = self.line                   
        start_column = self.column               
        value = ''                               # Initialize an empty string to accumulate the identifier

        # Loop to collect characters that are part of a valid identifier
        while self.current_char is not None and (self.current_char.isalnum() or self.current_char == '_'):
            value += self.current_char           # Add the current character to the identifier string
            self.advance()                       # Advance to the next character

        # Create an error object for the invalid identifier
        error = InvalidIdentifierError( value, start_line, start_column, message=f"Invalid identifier '{value}' must start with a lowercase letter." )
        self.errors.append(error)             

        return T('INVALID', value, start_line, start_column)

    def tokenize_identifier(self):
        start_line = self.line                   
        start_column = self.column               
        value = ''                               

        if not self.current_char.islower():
            self.advance()                       # Move to the next character
            return T('INVALID', value, start_line, start_column)

        # Continue consuming valid identifier characters
        while self.current_char is not None and (self.current_char.isalnum() or self.current_char == '_'):
            value += self.current_char           # Add the current character to the identifier string
            self.advance()                       # Advance to the next character

        return T('IDENTIFIER', value, start_line, start_column)

    def tokenize_identifier_or_keyword(self):
        start_line = self.line
        start_column = self.column
        value = ''
    
        # Collect all alphanumeric characters and underscores
        while self.current_char is not None and (self.current_char.isalnum() or self.current_char == '_'):
            value += self.current_char
            self.advance()
    
        # Attempt to match the collected value against keywords
        token_type = self.tokenize_keyword(value)
        if token_type:
            valid_delimiters = self.valid_delimiters_dict.get(token_type, [])
            if self.current_char is not None and self.current_char not in valid_delimiters:
                error_message = f"Invalid delimiter after keyword '{value}': '{self.current_char}'"
                error = InvalidSymbolError(self.current_char, self.line, self.column)
                error.message = error_message
                self.errors.append(error)
                self.advance()  
                return None  
            return T(token_type, value, start_line, start_column)
        else:
            
            errors_in_identifier = []
    
            if not value[0].islower():
                errors_in_identifier.append("must start with a lowercase letter")
    
            if len(value) > 20:
                errors_in_identifier.append("cannot exceed 20 characters")
    
            if errors_in_identifier:
                # Combine error messages
                error_message = f"Invalid identifier '{value}': " + "; ".join(errors_in_identifier) + "."
                error = InvalidIdentifierError(value, start_line, start_column)
                error.message = error_message
                self.errors.append(error)
                return None  # Do not return the token
            else:
                # Valid identifier
                token = T('IDENTIFIER', value, start_line, start_column)
    
            # Check for invalid delimiter after identifier
            if self.current_char is not None and self.current_char not in self.valid_delimiters_identifier:
                error_message = f"Invalid delimiter after identifier '{value}': '{self.current_char}'"
                error = InvalidSymbolError(self.current_char, self.line, self.column)
                error.message = error_message
                self.errors.append(error)
                self.advance()  # Move past the invalid character
                return None  # Do not return the token
    
            return token

    def tokenize_integer_literal(self):
        start_line = self.line
        start_column = self.column
        value = ''

        while self.current_char is not None and self.current_char.isdigit():
            value += self.current_char
            self.advance()

        lexeme = value.lstrip('0') or '0'

        # Enforce maximum of 9 digits
        if len(lexeme) > 9:
            error_message = f"Integer literal '{value}' exceeds maximum of 9 digits after removing leading zeros."
            error = InvalidIntegerError(error_message, start_line, start_column)
            self.errors.append(error)
            return None  
        
        # Check for invalid delimiter after integer literal
        if self.current_char is not None and self.current_char not in self.valid_delimiters_numeric:
            error_message = f"Invalid delimiter after integer literal '{lexeme}': '{self.current_char}'"
            error = InvalidSymbolError(self.current_char, self.line, self.column)
            error.message = error_message
            self.errors.append(error)
            self.advance()  # Skip the invalid character
            return None

        return T('INTEGERLITERAL', lexeme, start_line, start_column)

    def tokenize_point_literal(self):
        start_line = self.line
        start_column = self.column
        value = ''
        has_decimal_point = False

        while self.current_char is not None and (self.current_char.isdigit() or self.current_char == '.'):
            if self.current_char == '.':
                if has_decimal_point:
                    value += self.current_char
                    self.advance()
                    while self.current_char is not None and (self.current_char.isdigit() or self.current_char == '.'):
                        value += self.current_char
                        self.advance()
                    error_message = f"Invalid point literal: Multiple decimal points in '{value}'."
                    error = InvalidPointError(error_message, start_line, start_column)
                    self.errors.append(error)
                    return None
                has_decimal_point = True
            value += self.current_char
            self.advance()

        integer_part, fractional_part = value.split('.')
        integer_part = integer_part.lstrip('0') or '0'
        fractional_part = fractional_part or '0'

        if len(integer_part) > 9 or len(fractional_part) > 9:
            error_message = f"Point literal '{value}' exceeds maximum of 9 digits before or after the decimal point."
            error = InvalidPointError(error_message, start_line, start_column)
            self.errors.append(error)
            return None

        lexeme = f"{integer_part}.{fractional_part}"

        if self.current_char is not None and self.current_char not in self.valid_delimiters_numeric:
            error_message = f"Invalid delimiter after point literal '{lexeme}': '{self.current_char}'"
            error = InvalidSymbolError(self.current_char, self.line, self.column)
            error.message = error_message
            self.errors.append(error)
            self.advance()
            return None

        return T('POINTLITERAL', lexeme, start_line, start_column)
    
    def tokenize_negative_integer_literal(self):
        start_line = self.line
        start_column = self.column
        self.advance()  # Skip the '~'
    
        if self.current_char is not None and self.current_char.isdigit():
            value = ''
            while self.current_char is not None and self.current_char.isdigit():
                value += self.current_char
                self.advance()
    
            if value == '':
                error_message = f"Invalid negative integer literal: No digits after '~'."
                error = InvalidIntegerError(error_message, start_line, start_column)
                self.errors.append(error)
                return None
    
            lexeme = value.lstrip('0') or '0'
    
            if len(lexeme) > 9:
                error_message = f"Negative integer literal '~{value}' exceeds maximum of 9 digits after removing leading zeros."
                error = InvalidIntegerError(error_message, start_line, start_column)
                self.errors.append(error)
                return None
    
            full_lexeme = '~' + lexeme
    
            if self.current_char is not None and self.current_char not in self.valid_delimiters_numeric:
                error_message = f"Invalid delimiter after negative integer literal '{full_lexeme}': '{self.current_char}'"
                error = InvalidSymbolError(self.current_char, self.line, self.column)
                error.message = error_message
                self.errors.append(error)
                self.advance()
                return None
    
            return T('NEGINTEGERLITERAL', full_lexeme, start_line, start_column)
        else:
            # Retrieve valid delimiters for '~' from the symbol dictionary
            valid_delimiters = self.valid_delimiters_symbol_dict.get('~', [])
            if self.current_char is not None and self.current_char in valid_delimiters:
                # Treat '~' as a separate symbol token
                return T('~', '~', start_line, start_column)
            else:
                # Invalid usage of '~'
                if self.current_char is None:
                    error_message = f"Invalid usage of '~': '~' must be followed by digits or a valid delimiter."
                else:
                    error_message = f"Invalid delimiter after '~': '{self.current_char}'"
                error = InvalidIntegerError(error_message, start_line, start_column)
                self.errors.append(error)
                return None
    
    def tokenize_negative_point_literal(self):
        start_line = self.line
        start_column = self.column
        self.advance()  # Skip the '~'
    
        if self.current_char is None:
            error_message = f"Invalid negative point literal: '~' not followed by any characters."
            error = InvalidPointError(error_message, start_line, start_column)
            self.errors.append(error)
            return None
    
        # Check if the next character starts a point literal
        if self.current_char.isdigit() or self.current_char == '.':
            value = ''
            has_decimal_point = False
    
            while self.current_char is not None and (self.current_char.isdigit() or self.current_char == '.'):
                if self.current_char == '.':
                    if has_decimal_point:
                        error_message = f"Invalid negative point literal: Multiple decimal points in '~{value}'."
                        error = InvalidPointError(error_message, start_line, start_column)
                        self.errors.append(error)
                        self.advance()
                        return None
                    has_decimal_point = True
                value += self.current_char
                self.advance()
    
            if not has_decimal_point:
                error_message = f"Invalid negative point literal: Missing decimal point in '~{value}'."
                error = InvalidPointError(error_message, start_line, start_column)
                self.errors.append(error)
                return None
    
            # Split into integer and fractional parts
            if value.startswith('.'):
                integer_part = '0'
                fractional_part = value[1:]
            else:
                integer_part, fractional_part = value.split('.', 1)
    
            integer_part = integer_part.lstrip('0') or '0'
            fractional_part = fractional_part.rstrip('0') or '0'
    
            if len(integer_part) > 9 or len(fractional_part) > 9:
                error_message = f"Negative point literal '~{value}' exceeds maximum of 9 digits before or after the decimal point."
                error = InvalidPointError(error_message, start_line, start_column)
                self.errors.append(error)
                return None
    
            lexeme = f"~{integer_part}.{fractional_part}"
    
            if self.current_char is not None and self.current_char not in self.valid_delimiters_numeric:
                error_message = f"Invalid delimiter after negative point literal '{lexeme}': '{self.current_char}'"
                error = InvalidSymbolError(self.current_char, self.line, self.column)
                error.message = error_message
                self.errors.append(error)
                self.advance()
                return None
    
            return T('NEGPOINTLITERAL', lexeme, start_line, start_column)
        else:
            # Retrieve valid delimiters for '~' from the symbol dictionary
            valid_delimiters = self.valid_delimiters_symbol_dict.get('~', [])
            if self.current_char is not None and self.current_char in valid_delimiters:
                # Treat '~' as a separate symbol token
                return T('~', '~', start_line, start_column)
            else:
                # Invalid usage of '~'
                if self.current_char is None:
                    error_message = f"Invalid usage of '~': '~' must be followed by a point literal or a valid delimiter."
                else:
                    error_message = f"Invalid delimiter after '~': '{self.current_char}'"
                error = InvalidPointError(error_message, start_line, start_column)
                self.errors.append(error)
                return None

    def tokenize_number(self):
        start_line = self.line
        start_column = self.column
    
        # Check if the number is followed by a decimal point
        if '.' in self.collect_number_peek(start=0):
            return self.tokenize_point_literal()
    
        value = ''
    
        while self.current_char is not None and self.current_char.isdigit():
            value += self.current_char
            self.advance()
    
        # Check if the number is followed by alphabetic characters
        if self.current_char is not None and self.current_char.isalpha():
            invalid_identifier = value
            while self.current_char is not None and (self.current_char.isalnum() or self.current_char == '_'):
                invalid_identifier += self.current_char
                self.advance()
            error_message = "Invalid identifier; cannot start with a number"
            error = InvalidIdentifierError(
                invalid_identifier,
                start_line,
                start_column,
                message=error_message
            )
            self.errors.append(error)
            return None
    
        lexeme = value.lstrip('0') or '0'
    
        # Enforce maximum of 9 digits
        if len(lexeme) > 9:
            error_message = f"Integer literal '{value}' exceeds maximum of 9 digits after removing leading zeros."
            error = InvalidIntegerError(error_message, start_line, start_column)
            self.errors.append(error)
            return None  
        
        # Check for invalid delimiter after integer literal
        if self.current_char is not None and self.current_char not in self.valid_delimiters_numeric:
            error_message = f"Invalid delimiter after integer literal '{lexeme}': '{self.current_char}'"
            error = InvalidSymbolError(self.current_char, self.line, self.column)
            error.message = error_message
            self.errors.append(error)
            self.advance()  # Skip the invalid character
            return None
    
        return T('INTEGERLITERAL', lexeme, start_line, start_column)

    def tokenize_negative_number(self):
        if '.' in self.collect_number_peek(start=1):
            return self.tokenize_negative_point_literal()
        else:
            return self.tokenize_negative_integer_literal()

    def collect_number_peek(self, start=0):
        # Collect number without advancing, to check if it contains a decimal point
        pos = self.position + start
        num_str = ''
        while pos < len(self.code) and (self.code[pos].isdigit() or self.code[pos] == '.'):
            num_str += self.code[pos]
            pos += 1
        return num_str

    def tokenize_string_literal(self):
        start_line = self.line
        start_column = self.column
        value = '"'
        self.advance()
        while self.current_char is not None and self.current_char != '"':
            if self.current_char == '\n':
                break
            value += self.current_char
            self.advance()
        if self.current_char == '"':
            value += self.current_char
            self.advance()
            return T('TEXTLITERAL', value, start_line, start_column)
        else:
            error = LexerError(
                f"Unterminated string literal: {value}",
                start_line,
                start_column,
                'Invalid String Literal'
            )
            self.errors.append(error)
            return T('INVALID', value, start_line, start_column)

    def tokenize_symbol(self):
        start_line = self.line
        start_column = self.column
        symbol = None
    
        if self.current_char == '+':
            self.advance()
            if self.current_char == '+':
                self.advance()
                symbol = '++'
            elif self.current_char == '=':
                self.advance()
                symbol = '+='
            else:
                symbol = '+'
        elif self.current_char == '-':
            self.advance()
            if self.current_char == '-':
                self.advance()
                symbol = '--'
            elif self.current_char == '=':
                self.advance()
                symbol = '-='
            else:
                symbol = '-'
        elif self.current_char == '*':
            self.advance()
            if self.current_char == '=':
                self.advance()
                symbol = '*='
            else:
                symbol = '*'
        elif self.current_char == '/':
            self.advance()
            if self.current_char == '=':
                self.advance()
                symbol = '/='
            else:
                symbol = '/'
        elif self.current_char == '%':
            self.advance()
            symbol = '%'
        elif self.current_char == '=':
            self.advance()
            if self.current_char == '=':
                self.advance()
                symbol = '=='
            else:
                symbol = '='
        elif self.current_char == '!':
            self.advance()
            if self.current_char == '=':
                self.advance()
                symbol = '!='
            else:
                symbol = '!'
        elif self.current_char == '>':
            self.advance()
            if self.current_char == '=':
                self.advance()
                symbol = '>='
            else:
                symbol = '>'
        elif self.current_char == '<':
            self.advance()
            if self.current_char == '=':
                self.advance()
                symbol = '<='
            else:
                symbol = '<'
        elif self.current_char == '&':
            self.advance()
            if self.current_char == '&':
                self.advance()
                symbol = '&&'
            else:
                error = InvalidSymbolError('&', start_line, start_column)
                self.errors.append(error)
                return None
        elif self.current_char == '|':
            self.advance()
            if self.current_char == '|':
                self.advance()
                symbol = '||'
            else:
                error = InvalidSymbolError('|', start_line, start_column)
                self.errors.append(error)
                return None
        elif self.current_char in ['{', '}', '(', ')', '[', ']', ':', ',', ';']:
            symbol = self.current_char
            self.advance()
        else:
            # Invalid symbol
            invalid_char = self.current_char
            self.advance()
            error = InvalidSymbolError(invalid_char, start_line, start_column)
            self.errors.append(error)
            return T('INVALID', invalid_char, start_line, start_column, error="Invalid symbol")
    
        if symbol:
            valid_delimiters = self.valid_delimiters_symbol_dict.get(symbol, [])
            if self.current_char is not None and self.current_char not in valid_delimiters:
                error_message = f"Invalid delimiter after symbol '{symbol}': '{self.current_char}"
                # error_message = f"Invalid delimiter after symbol '{symbol}': '{self.current_char}' 'Delimiters: {valid_delimiters}'"
                error = InvalidSymbolError(self.current_char, self.line, self.column)
                error.message = error_message
                self.errors.append(error)
                self.advance()  # Skip the invalid character
                return None  # Do not return the symbol token
            return T(symbol, symbol, start_line, start_column)
    
        return None


    def process_code_input(self):
        """Lexical analyzer (also known as scanner or tokenizer)"""
        while self.current_char is not None:
            if self.current_char.isspace():
                if self.current_char == ' ':
                    token = self.tokenize_space()
                    if token:
                        return token
                elif self.current_char == '\n':
                    token = self.tokenize_newline()
                    if token:
                        return token
                elif self.current_char == '\t':
                    token = self.tokenize_space()
                    if token:
                        return token
                else:
                    self.advance()
                continue

            # check for identifiers or possible keywords
            if self.current_char.isalpha() or self.current_char == '_':
                token = self.tokenize_identifier_or_keyword()
                if token:
                    return token
                continue
    
            # Numbers
            if self.current_char.isdigit():
                token = self.tokenize_number()
                if token:
                    return token
                else:
                    continue  # Error was handled; continue tokenization
    
            # Negative Numbers
            if self.current_char == '~':
                token = self.tokenize_negative_number()
                if token:
                    return token
                else:
                    continue  # Error was handled; continue tokenization
    
            # Strings
            if self.current_char == '"':
                token = self.tokenize_string_literal()
                if token:
                    return token
    
            if self.current_char == '#':
                token = self.tokenize_comment()
                if token:
                    return token
            
            if self.current_char in self.symbols:
                token = self.tokenize_symbol()
                if token:
                    return token
                else:
                    continue  # Skip invalid symbol and continue tokenization
    
            # Handle any other unexpected characters
            value = self.current_char
            self.advance()
            error = InvalidSymbolError(value, self.line, self.column)
            self.errors.append(error)
            continue  # Continue lexing after handling error
    
        return None  # End of input