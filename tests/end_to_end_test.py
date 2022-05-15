# the bnf parser should be able to take the bnf of bnf itself and parse it correctly

import pytest

from bnf_parser import Grammar
from bnf_parser import Parser


def _remove_blank_lines(text: str) -> str:
    '''removes blank lines from the text'''
    lines = text.split('\n')
    lines = (line for line in lines if line.strip())
    return '\n'.join(lines)


def _remove_comments(text: str, symbol: str = '#') -> str:
    '''removes comments from the text'''
    lines = text.split('\n')
    lines = (line for line in lines if not line.startswith(symbol))
    return '\n'.join(lines)


def _load_bnf_grammar() -> str:
    '''loads the bnf grammer file and removes any blank lines'''
    with open('tests/bnf_grammar.bnf', 'r') as f:
        bnf = f.read()
    return bnf


def test_end_to_end_success() -> None:
    '''tests if the parser can parse the bnf grammar without failing'''
    bnf = _load_bnf_grammar()
    grammar = Grammar(bnf)
    parser = Parser(grammar)
    parser.parse(bnf)


def _remove_line(text: str, line_index: int) -> str:
    '''removes a line from the text'''
    lines = text.split('\n')
    lines = lines[:line_index] + lines[line_index + 1:]
    return '\n'.join(lines)


def test_end_to_end_failure() -> None:
    '''tests if the parser fails to parse bnf grammar
    when any single line from the grammer file'''
    bnf = _load_bnf_grammar()
    bnf = _remove_blank_lines(bnf)
    bnf = _remove_comments(bnf)
    bnf_line_count = len(bnf.split('\n'))
    for line_index in range(bnf_line_count):
        grammar_source = _remove_line(bnf, line_index)
        grammar = Grammar(grammar_source)
        parser = Parser(grammar)
        with pytest.raises(SyntaxError):
            parser.parse(grammar_source)
