import fileinput
from typing import NamedTuple
import re
import operator

class Token(NamedTuple):
    type: str
    value: str

def tokenize(code):
    token_specification = [
        ('NUMBER', r'\d+(\.\d*)?'),  # Integer
        ('OP', r'[+\-*/]'),  # Arithmetic operators
        ('PAREN', r'[()]'),  # Parenthesis
        ('SKIP', r'\s+'),  # Whitespace
        ('MISMATCH', r'.'),  # Any other character
    ]
    tok_regex = '|'.join('(?P<%s>%s)' % pair for pair in token_specification)
    for mo in re.finditer(tok_regex, code):
        kind = mo.lastgroup
        value = mo.group()
        if kind == 'NUMBER':
            value = int(value)
        elif kind == 'OP':
            value = OperatorLookup[value]
        elif kind == 'PAREN':
            pass
        elif kind == 'SKIP':
            continue
        elif kind == 'MISMATCH':
            raise RuntimeError(f'{value!r} unexpected')
        yield Token(kind, value)


OperatorLookup = {
    '+': operator.add,
    '*': operator.mul,
}

OperatorPrecedencePart1 = {
    operator.mul: 1,
    operator.add: 1,
    '(': 0
}

OperatorPrecedencePart2 = {
    operator.mul: 1,
    operator.add: 2,
    '(': 0
}


def infix_eval(expression_tokens, OperatorPrecedence):
    value_stack = []
    operator_stack = []

    for token in expression_tokens:
        if token.type == 'NUMBER':
            value_stack.append(token.value)

        elif token.type == 'PAREN':
            if token.value == '(':
                operator_stack.append(token.value)
            else:
                while len(operator_stack) > 0 and operator_stack[-1] is not '(':
                    a, b = value_stack.pop(), value_stack.pop()
                    op = operator_stack.pop()
                    value_stack.append(op(a, b))
                operator_stack.pop()

        elif token.type == 'OP':
            while len(operator_stack) > 0 and OperatorPrecedence[operator_stack[-1]] >= OperatorPrecedence[token.value]:
                a, b = value_stack.pop(), value_stack.pop()
                op = operator_stack.pop()
                value_stack.append(op(a, b))

            operator_stack.append(token.value)
        else:
            raise ValueError(f'error on token type: {token.type}, token value: {token.value}')

    while len(operator_stack) > 0:
        a, b = value_stack.pop(), value_stack.pop()
        op = operator_stack.pop()
        value_stack.append(op(a, b))

    return value_stack[0]


print(sum(infix_eval(tokenize(line), OperatorPrecedencePart1) for line in fileinput.input()))
print(sum(infix_eval(tokenize(line), OperatorPrecedencePart2) for line in fileinput.input()))
