# compiler/intermediate.py

def generate_intermediate_code(tokens):
    ir = []
    temp_var_count = 0
    
    for i, (token_type, token_value, line_no) in enumerate(tokens):
        if token_type == 'OPERATOR' and token_value == '=':
            # e.g., x = a + b;
            lhs = tokens[i-1][1]
            rhs1 = tokens[i+1][1]
            op = tokens[i+2][1]
            rhs2 = tokens[i+3][1]
            temp_var = f"t{temp_var_count}"
            ir.append(f"{temp_var} = {rhs1} {op} {rhs2}")
            ir.append(f"{lhs} = {temp_var}")
            temp_var_count += 1
    
    return ir
