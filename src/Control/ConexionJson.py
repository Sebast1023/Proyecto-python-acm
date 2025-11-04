import json
from pathlib import Path


class ConexionJSON:
    def __init__(self, ruta="specs/credentials.json"):
        self.ruta = Path(ruta)

    def leer_datos(self):
        """Lee y devuelve el contenido crudo del archivo JSON."""
        if not self.ruta.exists():
            return None
        try:
            with self.ruta.open("r", encoding="utf-8") as f:
                return json.load(f)
        except Exception:
            return None
