from bnf_parser import Grammar


def test_grammar_bnf() -> None:
    grammar_str = "digit ::= '0' | '1'\n"
    grammar = Grammar.from_bnf(grammar_str)
    assert grammar.to_bnf() == grammar_str


def test_grammar_json() -> None:
    grammar_str = '{"syntax-name": "", "rules": [{"rule-name": "digit", "expression": [[{"type": "literal", "text": "0", "optional": false}], [{"type": "literal", "text": "1", "optional": false}]]}]}'
    grammar = Grammar.from_json(grammar_str)
    assert grammar.to_json() == grammar_str
