import re

class Utilidades:
    """Clase de utilidades con métodos estáticos"""

    @staticmethod
    def validar_email(email: str) -> bool:
        """Valida que un email tenga formato correcto"""
        patron = r"^[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$"
        return re.match(patron, email) is not None