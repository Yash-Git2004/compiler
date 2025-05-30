import re    # Regular expressions module for pattern matching

KEYWORDS = {'if', 'else', 'while', 'for', 'def', 'return', 'int', 'float', 'void'}
OPERATORS = {'+', '-', '*', '/', '=', '==', '!=', '<', '>', '<=', '>='}
SYMBOLS = {'(', ')', '{', '}', ';', ','}

def tokenize(code):
    tokens = []
    lines = code.split('\n')
    
    for line_no, line in enumerate(lines, start=1):
        words = re.findall(r'\w+|==|!=|<=|>=|[^\s\w]', line)
        
        for word in words:
            if word in KEYWORDS:
                token_type = 'KEYWORD'
            elif word in OPERATORS:
                token_type = 'OPERATOR'
            elif word in SYMBOLS:
                token_type = 'SYMBOL'
            elif re.match(r'^[0-9]+$', word):
                token_type = 'NUMBER'
            elif re.match(r'^[a-zA-Z_][a-zA-Z0-9_]*$', word):
                token_type = 'IDENTIFIER'
            else:
                token_type = 'UNKNOWN'
            
            tokens.append((token_type, word, line_no))
    
    return tokens
