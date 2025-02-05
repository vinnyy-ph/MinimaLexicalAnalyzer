// monacoConfig/languageDefinition.js

export const MINIMA = 'MINIMA';

export const tokenizer = {
  tokenizer: {
    root: [
      //single line comment with #
    [/#[^\n]*/, 'comment'],
    [/[a-z_$][\w$]*/, {
    cases: {
          'get|show|integer|point|state|texts|group|checkif|recheck|otherwise|switch|each|repeat|do|exit|next|fixed|func|throw|case|default|YES|NO|empty': 'keyword',
          '@default': 'identifier'
        }
      }],
      [/[{}()\[\]]/, '@brackets'],
      [/[<>](?!@symbols)/, '@brackets'],
      [/(@symbols)/, {
        cases: {
          '@operators': 'operator',
          '@default': ''
        }
      }],
      [/\d+/, 'number'],
      [/[;,.]/, 'delimiter'],
    ],
  },
  keywords: ['get', 'show', 'integer', 'point', 'state', 'texts', 'group', 'checkif', 'recheck', 'otherwise', 'switch', 'each','repeat','do', 'exit','next','fixed','func','throw','case','default','YES','NO', 'empty'],
  operators: ['=', '>', '<', '!', '~', '?', ':', '==', '!=', '<=', '>=', '&&', '||', '++', '--', '+', '-', '*', '/', '&', '|', '^', '%', '<<', '>>', '>>>'],
  symbols: /[=><!~?:&|+\-*\/\^%]+/,
};

export const languageConfiguration = {
  comments: {
    lineComment: '//',
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