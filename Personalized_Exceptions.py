class SimplexError(Exception):
    """Classe base para exceções neste módulo Simplex."""
    pass

class InfeasibleProblemError(SimplexError):
    """Levantada quando o problema é considerado inviável."""
    pass

class UnboundedProblemError(SimplexError):
    """Levantada quando o problema é considerado ilimitado."""
    pass

class InvalidInputError(SimplexError):
    """Levantada para entradas inválidas específicas da lógica do Simplex."""
    pass