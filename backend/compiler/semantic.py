def semantic_check(tokens):
    declared_vars = {}
    used_vars = set()
    assigned_vars = set()
    types = {}

    i = 0
    while i < len(tokens):
        token_type, token_value, line_no = tokens[i]

        # Variable Declaration
        if token_type == 'KEYWORD' and token_value in ['int', 'float', 'string']:
            var_type = token_value

            if i+1 < len(tokens) and tokens[i+1][0] == 'IDENTIFIER':
                var_name = tokens[i+1][1]
                if var_name in declared_vars:
                    raise SyntaxError(f"Variable '{var_name}' redeclared at line {line_no}")
                declared_vars[var_name] = line_no
                types[var_name] = var_type
                i += 1  # Skip identifier
            else:
                raise SyntaxError(f"Expected variable name after type '{var_type}' at line {line_no}")

        # Assignment related Check kar raha hai
        elif token_type == 'IDENTIFIER':
            var_name = token_value
            used_vars.add(var_name)

            if var_name not in declared_vars:
                raise NameError(f"Variable '{var_name}' used without declaration at line {line_no}")

            if i+1 < len(tokens) and tokens[i+1][1] == '=':
                assigned_vars.add(var_name)
                if i+2 < len(tokens):
                    next_token = tokens[i+2]
                    rhs_type = get_type_of_token(next_token)

                    # Type Mismatch Check
                    if types[var_name] != rhs_type and not (types[var_name] == 'float' and rhs_type == 'int'):
                        raise TypeError(f"Type mismatch: Cannot assign '{rhs_type}' to '{types[var_name]}' variable '{var_name}' at line {line_no}")

                    # Division by zero check
                    if next_token[1] == '/' and i+3 < len(tokens) and tokens[i+3][1] == '0':
                        raise ZeroDivisionError(f"Division by zero at line {tokens[i+3][2]}")

        i += 1

    # Unused Variables
    for var in declared_vars:
        if var not in used_vars:
            print(f"Warning: Variable '{var}' declared at line {declared_vars[var]} but never used.")

    return "Semantic Check OK"

def get_type_of_token(token):
    token_type, token_value, _ = token

    if token_type == 'NUMBER':
        return 'int' if token_value.isdigit() else 'float'
    elif token_type == 'STRING':
        return 'string'
    elif token_type == 'IDENTIFIER':
        # Type will be resolved by context; return None
        return 'unknown'
    return 'unknown'
