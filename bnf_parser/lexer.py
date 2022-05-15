from __future__ import annotations


class Token:
    def __init__(self, tag: str, parent: Token = None) -> None:
        self._tag = tag
        self._parent = None
        self._children = []

    def _stringify_child(self, child: str | Token) -> str:
        '''converts a child to string'''
        return child if type(child) == str else child.text()

    def text(self) -> str:
        '''returns all text part of the token and its child tokens'''
        strings = map(self._stringify_child, self._children)
        return ''.join(strings)

    def add_child(self, child: str | Token) -> None:
        '''adds a child to the token'''
        self._children.append(child)
        child._parent = self


# class Parser:

def parse(text: str) -> list[Token]:
    '''parses a text and returns a list of tokens'''
    tokens = []
    active_token = None
    for character in text:
        # each single character is a token
        pass

# GR(BT.SYNTAX, [[GN(BT.RULE)], [GN(BT.RULE), GN(BT.SYNTAX)]]),


def match(rule: str, text: str) -> Token:
    '''matches a rule to a text and returns the matched text'''
    for sequence in expression:
