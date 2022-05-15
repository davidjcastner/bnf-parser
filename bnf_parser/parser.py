from bnf_parser.grammar import Grammar
from bnf_parser.parse_tree import ParseTree


class Parser:
    '''uses a bnf grammar to create parse trees'''

    def __init__(self, grammar: Grammar) -> None:
        self._grammar = grammar

    def parse(self, text: str) -> ParseTree:
        '''creates a parse tree from the text'''
