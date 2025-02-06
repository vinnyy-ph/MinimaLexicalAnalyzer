// monacoConfig/languageDefinition.js

export const MINIMA = 'MINIMA';

export const tokenizer = {
  tokenizer: {
    root: [
      // single line comment with #
      [/#[^\n]*/, 'comment'],

      // keywords & identifiers
      [/[a-z_$][\w$]*/, {
        cases: {
          'get|show|integer|point|state|texts|group|checkif|recheck|otherwise|switch|each|repeat|do|exit|next|fixed|func|throw|case|default|YES|NO|empty': 'keyword',
          '@default': 'identifier'
        }
      }],

      // match brackets
      [/[{}()\[\]]/, '@brackets'],

      // operators
      [/@symbols/, {
        cases: {
          '@operators': 'operator',
          '@default': ''
        }
      }],

      // numbers
      [/\d+/, 'number'],

      // delimiters
      [/[;,.]/, 'delimiter'],

      // strings (single- or double-quoted)
      [/"([^"\\]|\\.)*"/, 'string'],
      [/'([^'\\]|\\.)*'/, 'string'],
    ],
  },
  keywords: [
    'get', 'show', 'integer', 'point', 'state', 'texts', 'group',
    'checkif', 'recheck', 'otherwise', 'switch', 'each', 'repeat',
    'do', 'exit', 'next', 'fixed', 'func', 'throw', 'case', 'default',
    'YES', 'NO', 'empty'
  ],
  operators: [
    '=', '>', '<', '!', '~', '?', ':', '==', '!=', '<=', '>=',
    '&&', '||', '++', '--', '+', '-', '*', '/', '&', '|', '^',
    '%', '<<', '>>', '>>>'
  ],
  symbols: /[=><!~?:&|+\-*\/\^%]+/,
};


export const languageConfiguration = {
  comments: {
    lineComment: '#',
  },
  brackets: [
    ['{', '}'],
    ['[', ']'],
    ['(', ')'],
  ],
  autoClosingPairs: [
    { open: '{', close: '}' },
    { open: '[', close: ']' },
    { open: '(', close: ')' },
    { open: '"', close: '"' },
    { open: "'", close: "'" },
  ],
};