import json

SPECIAL_CHAR_LOOKUP = {
    '\\\\': '\\',
    '\\n': '\n',
    '\\t': '\t',
    '\\r': '\r',
    '\\"': '"',
    '\\\'': '\'',  # noqa Q003
}


class Terminal:
    def __init__(self, name: str, is_optional: bool) -> None:
        self.name = name
        self.is_optional = is_optional

    def __repr__(self) -> str:
        return f'<Terminal {self.name}>'

    def to_jsonable(self) -> str:
        return {'type': 'terminal', 'text': self.name, 'optional': self.is_optional}


class Literal:
    def __init__(self, text: str, is_optional: bool) -> None:
        self.text = text
        self.is_optional = is_optional

    def __repr__(self) -> str:
        return f'<Literal {self.text}>'

    def to_jsonable(self) -> str:
        return {'type': 'literal', 'text': self.text, 'optional': self.is_optional}


Sequence = list[Terminal | Literal]
Expression = list[Sequence]


def _sequence_to_jsonable(sequence: Sequence) -> list:
    '''converts a sequence to a jsonable object'''
    return [item.to_jsonable() for item in sequence]


def _expression_to_jsonable(expression: Expression) -> list:
    '''converts an expression to a jsonable object'''
    return [_sequence_to_jsonable(sequence) for sequence in expression]


class Rule:
    '''represents a rule in a grammar'''

    def __init__(self, name: str, expression: Expression) -> None:
        self.name = name
        self.expression = expression

    def __repr__(self) -> str:
        return f'<Rule {self.name} ::= {self.expression}>'

    def to_jsonable(self) -> dict:
        return {
            'rule-name': self.name,
            'expression': _expression_to_jsonable(self.expression),
        }


class Grammar:
    def __init__(self) -> None:
        self._rules = []

    def add_rule(self, rule: Rule) -> None:
        self._rules.append(rule)

    def __repr__(self) -> str:
        return f'<Grammar {self._rules}>'

    def to_jsonable(self) -> list:
        return [rule.to_jsonable() for rule in self._rules]


def _get_name_expression(line: str) -> tuple[str, str]:
    '''splits a line into rule-name and expression'''
    # find the first instance of ::= and split by that
    index = line.find('::=')
    if index == -1:
        raise ValueError('no ::= found in line')
    rule_name = line[:index]
    expression = line[index + 3:]
    return rule_name.strip(), expression.strip()


def _get_sequences(expression: str) -> list[Sequence]:
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
                sequences[sqi].append(Literal(current_token, is_optional))
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
            if char == '?':
                sequences[sqi].append(Terminal(current_token, True))
                current_token = ''
                index += 1
            elif char == '"':
                in_string = True
                string_end_char = '"'
                if current_token:
                    sequences[sqi].append(Terminal(current_token, False))
                    current_token = ''
                index += 1
            elif char == "'":
                in_string = True
                string_end_char = "'"
                if current_token:
                    sequences[sqi].append(Terminal(current_token, False))
                    current_token = ''
                index += 1
            elif char == ' ':
                if current_token:
                    sequences[sqi].append(Terminal(current_token, False))
                    current_token = ''
                index += 1
            elif char == '|':
                if current_token:
                    sequences[sqi].append(Terminal(current_token, False))
                    current_token = ''
                sequences.append([])
                sqi += 1
                index += 1
            else:
                current_token += char
                index += 1
    if current_token:
        sequences[sqi].append(Terminal(current_token, False))
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


def bnf_to_rules(source: str) -> Grammar:
    '''converts a bnf source to a grammar'''
    grammar = Grammar()
    lines = source.split('\n')
    # trim each line
    lines = _trim_lines(lines)
    # remove blank lines
    lines = _remove_blank_lines(lines)
    # remove comments
    lines = _remove_comments(lines)
    # each line is a rule
    for line in lines:
        # split line into rule-name and expression
        rule_name, expression = _get_name_expression(line)
        # split the expression into sequences
        sequences = _get_sequences(expression)
        grammar.add_rule(Rule(rule_name, sequences))
    return grammar


if __name__ == '__main__':
    with open('tests/bnf_grammar.bnf', 'r') as f:
        source = f.read()
    grammar = bnf_to_rules(source)
    # print(grammar)
    with(open('tests/bnf_grammar.json', 'w')) as f:
        json.dump(grammar.to_jsonable(), f, indent=4)
