from pycparser import c_parser, c_ast
from pycparser.c_generator import CGenerator
import re

class CCodeVisitor(c_ast.NodeVisitor):
    def __init__(self):
        self.pseudo = []
        self.indent_level = 0

    def indent(self):
        return "    " * self.indent_level

    def visit_FuncDef(self, node):
        name = node.decl.name
        args = []
        if isinstance(node.decl.type.args, c_ast.ParamList):
            for param in node.decl.type.args.params:
                args.append(param.name)
        self.pseudo.append(f"{self.indent()}Define function {name}({', '.join(args)}) Begin")
        self.indent_level += 1
        self.visit(node.body)
        self.indent_level -= 1
        self.pseudo.append(f"{self.indent()}End")

    def visit_Compound(self, node):
        for stmt in node.block_items or []:
            self.visit(stmt)


    def visit_Decl(self, node):
        if isinstance(node.type, c_ast.TypeDecl):
            if node.init:
                self.pseudo.append(f"{self.indent()}Declare {node.name} ← {self._expr(node.init)}")
            else:
                self.pseudo.append(f"{self.indent()}Declare {node.name}")
        self.generic_visit(node)

    def visit_Assignment(self, node):
        lval = self._expr(node.lvalue)
        rval = self._expr(node.rvalue)
        self.pseudo.append(f"{self.indent()}{lval} ← {rval}")

    def visit_If(self, node):
        cond = self._expr(node.cond)
        self.pseudo.append(f"{self.indent()}If ({cond}) then Begin")
        self.indent_level += 1
        self.visit(node.iftrue)
        self.indent_level -= 1
        if node.iffalse:
            self.pseudo.append(f"{self.indent()}Else Begin")
            self.indent_level += 1
            self.visit(node.iffalse)
            self.indent_level -= 1
        self.pseudo.append(f"{self.indent()}End If")

    def visit_For(self, node):
        try:
            init = self._expr(node.init)
            cond = self._expr(node.cond)
            next_ = self._expr(node.next)
            match_init = re.match(r'(int\s+)?(\w+)\s*=\s*(.+)', init)
            var = match_init.group(2) if match_init else "i"
            start = match_init.group(3) if match_init else "0"
            match_cond = re.match(rf'{var}\s*<=\s*(.+)', cond)
            end = match_cond.group(1) if match_cond else "?"

            # Check step size
            step = "1"
            match_step = re.match(rf'{var}\s*=\s*{var}\s*\+\s*(\d+)', next_)
            if match_step:
                step = match_step.group(1)

            if step == "1":
                self.pseudo.append(f"{self.indent()}For {var} ← {start} to {end} do\n Begin")
            else:
                self.pseudo.append(f"{self.indent()}For {var} ← {start} to {end}, step {step} do\n Begin")
        except:
            self.pseudo.append(f"{self.indent()}For ({init}; {cond}; {next_}) do\n Begin")

        self.indent_level += 1
        self.visit(node.stmt)
        self.indent_level -= 1
        self.pseudo.append(f"{self.indent()}End For")


    def visit_While(self, node):
        cond = self._expr(node.cond)
        self.pseudo.append(f"{self.indent()}While ({cond}) Begin")
        self.indent_level += 1
        self.visit(node.stmt)
        self.indent_level -= 1
        self.pseudo.append(f"{self.indent()}End While")

    def visit_Return(self, node):
        expr = self._expr(node.expr) if node.expr else ""
        self.pseudo.append(f"{self.indent()}Return {expr}")

    def visit_FuncCall(self, node):
        if isinstance(node.name, c_ast.ID) and node.name.name == 'printf':
            if node.args:
            
                args = node.args.exprs[1:] if len(node.args.exprs) > 1 else []
                clean_args = []
                for arg in args:
                    code = CGenerator().visit(arg)
                    clean = code.replace('&', '').replace('*', '').strip()
                    clean_args.append(clean)
                joined = ", ".join(clean_args)
                self.pseudo.append(f"{self.indent()}Print {joined}")
            else:
                self.pseudo.append(f"{self.indent()}Print")
        else:
            self.pseudo.append(f"{self.indent()}Call {self._expr(node)}")



    def _expr(self, node):
        if node is None:
            return ""
        try:
            return CGenerator().visit(node)
        except Exception:
            return str(node)

def clean_c_code(code: str) -> str:
    return re.sub(r'^\s*#.*$', '', code, flags=re.MULTILINE)

def convert_c_to_pseudocode(code: str) -> str:
    try:
        cleaned_code = clean_c_code(code)
        parser = c_parser.CParser()
        ast_tree = parser.parse(cleaned_code)
        visitor = CCodeVisitor()
        visitor.visit(ast_tree)
        return '\n'.join(visitor.pseudo)
    except Exception as e:
        return f"Error parsing C code: {str(e)}"
