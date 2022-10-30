from __future__ import annotations
import json
from bnf_parser.custom_types import ExpressionStruct
from bnf_parser.custom_types import GrammarStruct
from bnf_parser.custom_types import RuleStruct
from bnf_parser.custom_types import SequenceStruct
from bnf_parser.custom_types import TermStruct
from bnf_parser.utility import parse_bnf_rules


class Grammar:
    '''an ordered rule set for a language'''

    def __init__(self, name: str = '') -> None:
        self._name = name
        self._rule_order: list[str] = []
        self._expressions: dict[str, ExpressionStruct] = {}

    def __repr__(self) -> str:
        return self.to_bnf()

    def _add_rule(self, rule_name: str, expression: ExpressionStruct) -> None:
        '''adds a rule to the grammar'''
        self._rule_order.append(rule_name)
        self._expressions[rule_name] = expression

    @staticmethod
    def from_json(source: str) -> Grammar:
        '''
        creates a grammar from a json string

        format: { 'syntax-name': str, 'rules': list[list[TermStruct]] }
        TermStruct = {'type': str, 'text': str, 'optional': bool}
        '''
        raw: GrammarStruct = json.loads(source)
        grammar = Grammar(raw['syntax-name'])
        for rule in raw['rules']:
            grammar._add_rule(rule['rule-name'], rule['expression'])
        return grammar

    def _rule_to_json(self, rule: str) -> RuleStruct:
        '''returns a json string representing the rule'''
        return {
            'rule-name': rule,
            'expression': self._expressions[rule]
        }

    def to_json(self) -> str:
        '''
        returns a json string representing the grammar

        format: { 'syntax-name': str, 'rules': list[list[TermStruct]] }
        TermStruct = {'type': str, 'text': str, 'optional': bool}
        '''
        output = {
            'syntax-name': self._name,
            'rules': [self._rule_to_json(rule) for rule in self._rule_order]
        }
        return json.dumps(output)

    @staticmethod
    def from_bnf(source: str, syntax_name: str = '') -> Grammar:
        '''creates a grammar from a bnf string'''
        bnf_rules = parse_bnf_rules(source)
        json_data = {
            'syntax-name': syntax_name,
            'rules': bnf_rules
        }
        return Grammar.from_json(json.dumps(json_data))

    def _term_to_bnf(self, term: TermStruct) -> str:
        '''returns a bnf string representing the term'''
        suffix = '?' if term['optional'] else ''
        if term['type'] == 'literal':
            return repr(term['text']) + suffix
        return term['text'] + suffix

    def _sequence_to_bnf(self, sequence: SequenceStruct) -> str:
        '''returns a bnf string representing the sequence'''
        return ' '.join(self._term_to_bnf(term) for term in sequence)

    def _expression_to_bnf(self, rule: str) -> str:
        '''returns a bnf string representing the expression'''
        return ' | '.join(self._sequence_to_bnf(sequence) for sequence in self._expressions[rule])

    def to_bnf(self) -> str:
        '''returns a bnf string representing the grammar'''
        output = f'# {self._name}\n' if self._name else ''
        for rule in self._rule_order:
            output += f'{rule} ::= {self._expression_to_bnf(rule)}\n'
        return output


if __name__ == '__main__':
    GRAMMAR = '''
addition        ::= whitespace? number whitespace? '+' whitespace? number whitespace?
subtraction     ::= whitespace? number whitespace? '-' whitespace? number whitespace?
number          ::= negative? integer | negative? float
negative        ::= '-'
float           ::= integer '.' integer
integer         ::= digit | digit integer
digit           ::= '0' | '1' | '2' | '3' | '4' | '5' | '6' | '7' | '8' | '9'
whitespace      ::= whitespace-char | whitespace-char whitespace
whitespace-char ::= ' '
'''
    with open('tests/bnf_grammar.bnf') as f:
        grammar_str = f.read()
    grammar = Grammar.from_bnf(GRAMMAR)
    print(grammar.to_bnf()[:-1])
    print(grammar.to_json())
