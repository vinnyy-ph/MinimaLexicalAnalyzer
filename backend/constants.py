ATOMS = {
    # single characters only
    # 'ascii': {chr(i) for i in range(128) if chr(i) != '\0'},
    'ascii': {chr(i) for i in range(128)},
    'ascii_263': {chr(i) for i in range(128) if chr(i) not in ['"', '\\', '\0']},
    'ascii_272': {chr(i) for i in range(128) if chr(i) not in ['^', '\0']},
    'ascii_273': {chr(i) for i in range(128) if chr(i) not in ['/', '\0']},
    'alphabet': {
        'a', 'b', 'c', 'd', 'e', 'f', 'g', 'h', 'i', 'j', 'k', 'l', 'm', 'n', 'o', 'p', 'q', 'r', 's', 't', 'u', 'v', 'w', 'x', 'y', 'z',
        'A', 'B', 'C', 'D', 'E', 'F', 'G', 'H', 'I', 'J', 'K', 'L', 'M', 'N', 'O', 'P', 'Q', 'R', 'S', 'T', 'U', 'V', 'W', 'X', 'Y', 'Z',
    },
    'digit': {'0','1','2','3','4','5','6','7','8','9'},
    'alphanumeric': {
        'a', 'b', 'c', 'd', 'e', 'f', 'g', 'h', 'i', 'j', 'k', 'l', 'm', 'n', 'o', 'p', 'q', 'r', 's', 't', 'u', 'v', 'w', 'x', 'y', 'z',
        'A', 'B', 'C', 'D', 'E', 'F', 'G', 'H', 'I', 'J', 'K', 'L', 'M', 'N', 'O', 'P', 'Q', 'R', 'S', 'T', 'U', 'V', 'W', 'X', 'Y', 'Z',
        '0','1','2','3','4','5','6','7','8','9',
    },
}

def ascii_except(chars: list[chr] = []):
    chars = list(chars) if type(chars) is str else chars
    ascii = ATOMS['ascii'].copy()
    for char in chars:
        ascii.remove(char)
    return ascii

if __name__ == '__main__':
    print('/' not in ATOMS["ascii_string"])