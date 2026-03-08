import ast
import operator
import math

OPERATORS = {
    ast.Add: operator.add,
    ast.Sub: operator.sub,
    ast.Mult: operator.mul,
    ast.Div: operator.truediv,
    ast.Pow: operator.pow,
    ast.Mod: operator.mod
}

FUNCTIONS = {
    "sqrt": math.sqrt,
    "sin": math.sin,
    "cos": math.cos,
    "tan": math.tan,
    "log": math.log,
    "log10": math.log10,
    "factorial": math.factorial,
    "abs": abs
}

CONSTANTS = {
    "pi": math.pi,
    "e": math.e
}


def calcular(expr: str):

    node = ast.parse(expr, mode="eval").body

    def avaliar(n):

        if isinstance(n, ast.Constant):
            return n.value

        elif isinstance(n, ast.BinOp):
            return OPERATORS[type(n.op)](
                avaliar(n.left),
                avaliar(n.right)
            )

        elif isinstance(n, ast.UnaryOp):
            if isinstance(n.op, ast.USub):
                return -avaliar(n.operand)
            if isinstance(n.op, ast.UAdd):
                return avaliar(n.operand)

        elif isinstance(n, ast.Name):
            if n.id in CONSTANTS:
                return CONSTANTS[n.id]
            raise ValueError("Constante inválida")

        elif isinstance(n, ast.Call):

            if not isinstance(n.func, ast.Name):
                raise ValueError("Função inválida")

            nome = n.func.id

            if nome not in FUNCTIONS:
                raise ValueError("Função não permitida")

            args = [avaliar(arg) for arg in n.args]

            return FUNCTIONS[nome](*args)

        raise ValueError("Expressão inválida")

    return avaliar(node)