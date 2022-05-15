import json
from bnf_parser.custom_types import ExpressionStruct
from bnf_parser.custom_types import RuleStruct
from bnf_parser.custom_types import TermStruct

SPECIAL_CHAR_LOOKUP = {
    '\\\\': '\\',
    '\\n': '\n',
    '\\t': '\t',
    '\\r': '\r',
    '\\"': '"',
    '\\\'': '\'',  # noqa Q003
}


def _to_literal(text: str, is_optional: bool) -> TermStruct:
    '''creates a term struct for the literal'''
    return {'type': 'literal', 'text': text, 'optional': is_optional}


def _to_terminal(text: str, is_optional: bool) -> TermStruct:
    '''creates a term struct for the terminal'''
    return {'type': 'terminal', 'text': text, 'optional': is_optional}


def _get_name_expression(line: str) -> tuple[str, str]:
    '''splits a line into rule-name and expression'''
    # find the first instance of ::= and split by that
    index = line.find('::=')
    if index == -1:
        raise ValueError('no ::= found in line')
    rule_name = line[:index]
    expression = line[index + 3:]
    return rule_name.strip(), expression.strip()


def _get_sequences(expression: str) -> ExpressionStruct:
    '''splits an expression into sequences'''
    sequences = [[]]
    sqi = 0  # sequence index
    index = 0
    current_token = ''
    in_string = False
    string_end_char = ''
    while index < len(expression):
        char = expression[index]
        if in_string:
            if char == string_end_char:
                is_optional = index + 1 < len(expression) and expression[index + 1] == '?'
                sequences[sqi].append(_to_literal(current_token, is_optional))
                in_string = False
                current_token = ''
                string_end_char = ''
                index += 2 if is_optional else 1
            elif char == '\\':
                special_char = expression[index: index + 2]
                special_char = SPECIAL_CHAR_LOOKUP[special_char]
                current_token += special_char
                index += 2
            else:
                current_token += char
                index += 1
        else:
            if char == '#':
                # single line comment also suffices as end of a rule
                break
            elif char == '?':
                sequences[sqi].append(_to_terminal(current_token, True))
                current_token = ''
                index += 1
            elif char == '"':
                in_string = True
                string_end_char = '"'
                if current_token:
                    sequences[sqi].append(_to_terminal(current_token, False))
                    current_token = ''
                index += 1
            elif char == "'":
                in_string = True
                string_end_char = "'"
                if current_token:
                    sequences[sqi].append(_to_terminal(current_token, False))
                    current_token = ''
                index += 1
            elif char == ' ':
                if current_token:
                    sequences[sqi].append(_to_terminal(current_token, False))
                    current_token = ''
                index += 1
            elif char == '|':
                if current_token:
                    sequences[sqi].append(_to_terminal(current_token, False))
                    current_token = ''
                sequences.append([])
                sqi += 1
                index += 1
            else:
                current_token += char
                index += 1
    if current_token:
        sequences[sqi].append(_to_terminal(current_token, False))
    return sequences


def _trim_lines(lines: list[str]) -> list[str]:
    '''trims each line'''
    lines = (line.strip() for line in lines)
    return lines


def _remove_blank_lines(lines: list[str]) -> list[str]:
    '''removes blank lines from the text'''
    lines = (line for line in lines if line.strip())
    return lines


def _remove_comments(lines: list[str], symbol: str = '#') -> list[str]:
    '''removes comments from the text'''
    lines = (line for line in lines if not line.startswith(symbol))
    return lines


def parse_bnf_rules(source: str) -> list[RuleStruct]:
    '''parses a bnf source and returns a list of rule structs'''
    # clean the source lines by trimming and removing blank lines and comments
    lines = source.split('\n')
    lines = _trim_lines(lines)
    lines = _remove_blank_lines(lines)
    lines = _remove_comments(lines)
    # now each line is a rule
    rules = []
    for line in lines:
        # split line into rule-name and expression
        rule_name, expression = _get_name_expression(line)
        # split the expression into sequences
        sequences = _get_sequences(expression)
        rules.append({'rule-name': rule_name, 'expression': sequences})
    return rules


if __name__ == '__main__':
    with open('tests/bnf_grammar.bnf', 'r') as f:
        source = f.read()
    grammar = parse_bnf_rules(source)
    print(grammar)
    with(open('tests/bnf_grammar.json', 'w')) as f:
        json.dump(grammar, f, indent=4)
