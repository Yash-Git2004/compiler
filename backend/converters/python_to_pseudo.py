import ast

class PseudoCodeGenerator(ast.NodeVisitor):
    def __init__(self):
        self.pseudo = []
        self.indent_level = 0

    def indent(self):
        return "    " * self.indent_level

    def visit_FunctionDef(self, node):
        args = ", ".join([arg.arg for arg in node.args.args])
        self.pseudo.append(f"{self.indent()}Function {node.name}({args})")
        self.pseudo.append(f"{self.indent()}Begin")
        self.indent_level += 1
        for stmt in node.body:
            self.visit(stmt)
        self.indent_level -= 1
        self.pseudo.append(f"{self.indent()}End Function")

    def visit_Assign(self, node):
        targets = [ast.unparse(t) for t in node.targets]
        value = ast.unparse(node.value)
        self.pseudo.append(f"{self.indent()}Set {' = '.join(targets)} to {value}")

    def visit_If(self, node):
        test = ast.unparse(node.test)
        self.pseudo.append(f"{self.indent()}If {test} Then")
        self.pseudo.append(f"{self.indent()}Begin")
        self.indent_level += 1
        for stmt in node.body:
            self.visit(stmt)
        self.indent_level -= 1
        self.pseudo.append(f"{self.indent()}End If")
        if node.orelse:
            self.pseudo.append(f"{self.indent()}Else")
            self.pseudo.append(f"{self.indent()}Begin")
            self.indent_level += 1
            for stmt in node.orelse:
                self.visit(stmt)
            self.indent_level -= 1
            self.pseudo.append(f"{self.indent()}End Else")

    def visit_For(self, node):
        if isinstance(node.iter, ast.Call) and isinstance(node.iter.func, ast.Name) and node.iter.func.id == "range":
            args = node.iter.args
            if len(args) == 1:
                start = "0"
                end = ast.unparse(args[0])
            elif len(args) == 2:
                start = ast.unparse(args[0])
                end = ast.unparse(args[1])
            else:
                start = ast.unparse(args[0])
                end = ast.unparse(args[1])
            target = ast.unparse(node.target)
            self.pseudo.append(f"{self.indent()}For {target} from {start} to {end}")
        else:
            target = ast.unparse(node.target)
            iter_ = ast.unparse(node.iter)
            self.pseudo.append(f"{self.indent()}For each {target} in {iter_}")
        self.pseudo.append(f"{self.indent()}Begin")
        self.indent_level += 1
        for stmt in node.body:
            self.visit(stmt)
        self.indent_level -= 1
        self.pseudo.append(f"{self.indent()}End For")

    def visit_While(self, node):
        test = ast.unparse(node.test)
        self.pseudo.append(f"{self.indent()}While {test}")
        self.pseudo.append(f"{self.indent()}Begin")
        self.indent_level += 1
        for stmt in node.body:
            self.visit(stmt)
        self.indent_level -= 1
        self.pseudo.append(f"{self.indent()}End While")

    def visit_Return(self, node):
        value = ast.unparse(node.value) if node.value else ""
        self.pseudo.append(f"{self.indent()}Return {value}")

    def visit_Expr(self, node):
        if isinstance(node.value, ast.Call):
            self.visit_Call(node.value)

    def visit_Call(self, node):
        func = ast.unparse(node.func)
        args = ", ".join([ast.unparse(arg) for arg in node.args])
        if func == "print":
            self.pseudo.append(f"{self.indent()}Display {args}")
        elif func == "input":
            self.pseudo.append(f"{self.indent()}Get input")
        else:
            self.pseudo.append(f"{self.indent()}Call {func}({args})")


def convert_python_to_pseudocode(code: str) -> str:
    try:
        tree = ast.parse(code)
        generator = PseudoCodeGenerator()
        generator.visit(tree)
        return "\n".join(generator.pseudo)
    except Exception as e:
        return f"Error parsing Python code: {str(e)}"

