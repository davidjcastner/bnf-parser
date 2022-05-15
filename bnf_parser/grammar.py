# <syntax>         ::= <rule> | <rule> <syntax>
# <comment>        ::= <opt-whitespace> ";" <any-character-sequence> <line-end>
# <any-character-sequence>  ::= <any-character> | <any-character> <any-character>
# <any-character>  ::= <letter> | <digit> | <symbol> | <opt-whitespace>
# <rule>           ::= <opt-whitespace> "<" <rule-name> ">" <opt-whitespace> "::=" <opt-whitespace> <expression> <line-end>
# <opt-whitespace> ::= " " <opt-whitespace> | ""
# <expression>     ::= <list> | <list> <opt-whitespace> "|" <opt-whitespace> <expression>
# <line-end>       ::= <opt-whitespace> <end-of-line> | <line-end> <line-end>
# <list>           ::= <term> | <term> <opt-whitespace> <list>
# <term>           ::= <literal> | "<" <rule-name> ">"
# <literal>        ::= '"' <text1> '"' | "'" <text2> "'"
# <text1>          ::= "" | <character1> <text1>
# <text2>          ::= '' | <character2> <text2>
# <character>      ::= <letter> | <digit> | <symbol>
# <letter>         ::= "A" | "B" | "C" | "D" | "E" | "F" | "G" | "H" | "I" | "J" | "K" | "L" | "M" | "N" | "O" | "P" | "Q" | "R" | "S" | "T" | "U" | "V" | "W" | "X" | "Y" | "Z" | "a" | "b" | "c" | "d" | "e" | "f" | "g" | "h" | "i" | "j" | "k" | "l" | "m" | "n" | "o" | "p" | "q" | "r" | "s" | "t" | "u" | "v" | "w" | "x" | "y" | "z"
# <digit>          ::= "0" | "1" | "2" | "3" | "4" | "5" | "6" | "7" | "8" | "9"
# <end-of-line>    ::= "\n" | "\r"
# <character1>     ::= <character> | "'"
# <character2>     ::= <character> | '"'
# <rule-name>      ::= <letter> | <rule-name> <rule-char>
# <rule-char>      ::= <letter> | <digit> | "-"
# <symbol>         ::=  "|" | " " | "!" | "#" | "$" | "%" | "&" | "(" | ")" | "*" | "+" | "," | "-" | "." | "/" | ":" | ";" | ">" | "=" | "<" | "?" | "@" | "[" | "]" | "^" | "_" | "`" | "{" | "}" | "~" | "\"

from bnf_parser.lexer import Lexer
from enum import Enum


class BnfToken(Enum):
    '''all token types for the bnf grammar'''
    SYNTAX = 'syntax',
    COMMENT = 'comment',
    ANY_CHARACTER_SEQUENCE = 'any_character_sequence',
    ANY_CHARACTER = 'any_character',
    RULE = 'rule',
    OPT_WHITESPACE = 'opt_whitespace',
    EXPRESSION = 'expression',
    LINE_END = 'line_end',
    LIST = 'list',
    TERM = 'term',
    LITERAL = 'literal',
    TEXT1 = 'text1',
    TEXT2 = 'text2',
    CHARACTER = 'character',
    LETTER = 'letter',
    DIGIT = 'digit',
    END_OF_LINE = 'end_of_line',
    CHARACTER1 = 'character1',
    CHARACTER2 = 'character2',
    RULE_NAME = 'rule_name',
    RULE_CHAR = 'rule_char',
    SYMBOL = 'symbol',


class GrammarRuleName: ...


GrammarSequence = list[GrammarRuleName | str]
GrammarExpression = list[GrammarSequence]
class GrammarRule: ...


BT = BnfToken
GR = GrammarRule
GN = GrammarRuleName

BNF_RULES = [
    GR(BT.SYNTAX, [[GN(BT.RULE)], [GN(BT.RULE), GN(BT.SYNTAX)]]),
    GR(BT.COMMENT, [[GN(BT.OPT_WHITESPACE), ';', GN(BT.ANY_CHARACTER_SEQUENCE), GN(BT.LINE_END)]]),
    GR(BT.ANY_CHARACTER_SEQUENCE, [[GN(BT.ANY_CHARACTER)], [GN(BT.ANY_CHARACTER), GN(BT.ANY_CHARACTER)]]),
    GR(BT.ANY_CHARACTER, [[GN(BT.LETTER)], [GN(BT.DIGIT)], [GN(BT.SYMBOL)], [GN(BT.OPT_WHITESPACE)]]),
    GR(BT.RULE, [[GN(BT.OPT_WHITESPACE), '<', GN(BT.RULE_NAME), '>', GN(BT.OPT_WHITESPACE), '::=', GN(BT.OPT_WHITESPACE), GN(BT.EXPRESSION), GN(BT.LINE_END)]]),
    GR(BT.OPT_WHITESPACE, [[' ', GN(BT.OPT_WHITESPACE)], ['']]),
    GR(BT.EXPRESSION, [[GN(BT.LIST)], [GN(BT.LIST), GN(BT.OPT_WHITESPACE), '|', GN(BT.OPT_WHITESPACE), GN(BT.EXPRESSION)]]),
    GR(BT.LINE_END, [[GN(BT.OPT_WHITESPACE), GN(BT.EOL)], [GN(BT.LINE_END), GN(BT.LINE_END)]]),
    GR(BT.LIST, [[GN(BT.TERM)], [GN(BT.TERM), GN(BT.OPT_WHITESPACE), GN(BT.LIST)]]),
    GR(BT.TERM, [[GN(BT.LITERAL)], ['<', GN(BT.RULE_NAME), '>']]),
    GR(BT.LITERAL, [['"', GN(BT.TEXT1), '"'], ["'", GN(BT.TEXT2), "'"]]),
    GR(BT.TEXT1, [[''], [GN(BT.CHARACTER1), GN(BT.TEXT1)]]),
    GR(BT.TEXT2, [[''], [GN(BT.CHARACTER2), GN(BT.TEXT2)]]),
    GR(BT.CHARACTER, [[GN(BT.LETTER)], [GN(BT.DIGIT)], [GN(BT.SYMBOL)]]),
    GR(BT.LETTER, [['A'], ['B'], ['C'], ['D'], ['E'], ['F'], ['G'], ['H'], ['I'], ['J'], ['K'], ['L'], ['M'], ['N'], ['O'], ['P'], ['Q'], ['R'], ['S'], ['T'], ['U'], ['V'], ['W'], ['X'], ['Y'], ['Z'], ['a'], ['b'], ['c'], ['d'], ['e'], ['f'], ['g'], ['h'], ['i'], ['j'], ['k'], ['l'], ['m'], ['n'], ['o'], ['p'], ['q'], ['r'], ['s'], ['t'], ['u'], ['v'], ['w'], ['x'], ['y'], ['z']]),
    GR(BT.DIGIT, [['0'], ['1'], ['2'], ['3'], ['4'], ['5'], ['6'], ['7'], ['8'], ['9']]),
    GR(BT.END_OF_LINE, [['\n'], ['\r']]),
    GR(BT.CHARACTER1, [[GN(BT.CHARACTER)], ["'"]]),
    GR(BT.CHARACTER2, [[GN(BT.CHARACTER)], ['"']]),
    GR(BT.RULE_NAME, [[GN(BT.LETTER)], [GN(BT.RULE_NAME), GN(BT.RULE_CHAR)]]),
    GR(BT.RULE_CHAR, [[GN(BT.LETTER)], [GN(BT.DIGIT)], ['-', GN(BT.RULE_CHAR)]]),
    GR(BT.SYMBOL, [['|'], [' '], ['!'], ['#'], ['$'], ['%'], ['&'], ['('], [')'], ['*'], ['+'], [','], ['-'], ['.'], ['/'], [':'], [';'], ['>'], ['='], ['<'], ['?'], ['@'], ['['], [']'], ['^'], ['_'], ['`'], ['{'], ['}'], ['~'], ['\\']])
]


class Grammar:
    '''a ruleset for a grammar created from text in bnf format'''

    def __init__(self, bnf: str) -> None:
        self._bnf_string = bnf

    def _parse_bnf(self) -> None:
        '''parses the bnf string into a list of rules,
        cannot use the parser from this library
        because it is dependant on the grammar'''
        # use a lexer to tokenize the bnf string
        lexer = Lexer(BNF_RULES)
        tokens = lexer.tokenize(self._bnf_string)
        # create a rule list from the tokens
