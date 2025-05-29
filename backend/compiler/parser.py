# compiler/parser.py

def parse_tokens(tokens):
    i = 0
    while i < len(tokens):
        token_type, token_value, line_no = tokens[i]
        
        if token_value == 'def':
            # Function definition: def <name> ( )
            if i+1 >= len(tokens) or tokens[i+1][0] != 'IDENTIFIER':
                raise SyntaxError(f"Expected function name at line {line_no}")
            if i+2 >= len(tokens) or tokens[i+2][1] != '(':
                raise SyntaxError(f"Expected '(' at line {line_no}")
            if i+3 >= len(tokens) or tokens[i+3][1] != ')':
                raise SyntaxError(f"Expected ')' at line {line_no}")
        
        elif token_value == 'if':
            # Check if condition follows
            if i+1 >= len(tokens) or tokens[i+1][1] != '(':
                raise SyntaxError(f"Expected '(' after if at line {line_no}")
        
        i += 1
    
    return "Syntax OK"
