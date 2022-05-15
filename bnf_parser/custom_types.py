TermStruct = {'type': str, 'text': str, 'optional': bool}
SequenceStruct = list[TermStruct]
ExpressionStruct = list[SequenceStruct]
RuleStruct = {'rule-name': str, 'expression': ExpressionStruct}
GrammarStruct = {'syntax-name': str, 'rules': list[RuleStruct]}
