import ast
import math

def calcular_expressao(expressao: str) -> float:
    """
    Avalia uma expressão matemática de forma segura e determinística.
    Permite números, constantes de engenharia (pi, e), funções matemáticas básicas (sqrt, abs, round)
    e operadores aritméticos (+, -, *, /, **, //, %).
    """
    try:
        # Substitui vírgulas por pontos caso a IA tenha enviado padrão brasileiro
        expressao_limpa = str(expressao).replace(',', '.')
        
        # Cria uma AST (Abstract Syntax Tree) e avalia apenas nós seguros
        node = ast.parse(expressao_limpa, mode='eval')
        valid_nodes = (
            ast.Expression, ast.BinOp, ast.UnaryOp, ast.Constant, 
            ast.operator, ast.unaryop, ast.Name, ast.Call, 
            ast.Load, ast.expr_context
        )
        
        allowed_names = {'pi', 'e', 'sqrt', 'abs', 'round'}
        
        for n in ast.walk(node):
            if not isinstance(n, valid_nodes):
                raise ValueError(f"Operação não permitida na expressão: {expressao}")
            if isinstance(n, ast.Name):
                if n.id.lower() not in allowed_names:
                    raise ValueError(f"Identificador não permitido: '{n.id}'")
            if isinstance(n, ast.Call):
                if not (isinstance(n.func, ast.Name) and n.func.id.lower() in {'sqrt', 'abs', 'round'}):
                    raise ValueError(f"Função não permitida na expressão: '{ast.dump(n.func)}'")
                
        # Contexto matemático seguro (zero builtins)
        math_context = {
            "pi": math.pi,
            "PI": math.pi,
            "Pi": math.pi,
            "e": math.e,
            "sqrt": math.sqrt,
            "abs": abs,
            "round": round
        }
        
        resultado = eval(compile(node, '<string>', 'eval'), {"__builtins__": None}, math_context)
        return round(float(resultado), 4)
    except Exception as e:
        raise ValueError(f"Expressão inválida ou não permitida: {expressao!r}: {e}") from e
