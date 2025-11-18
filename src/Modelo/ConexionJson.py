import json
from pathlib import Path


class ConexionJSON:
    def __init__(self, ruta):
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
                
    def escribir_datos(self, datos):
        """Escribe datos en el archivo JSON."""
        try:
            with self.ruta.open("w", encoding="utf-8") as f:
                json.dump(datos, f, indent=4)
        except Exception as e:
            print(f"Error al escribir en el archivo JSON: {e}")

    def cambiar_ruta(self, nueva_ruta):
        """Cambia la ruta del archivo JSON."""
        self.ruta = Path(nueva_ruta)

    def existe_archivo(self):
        """Verifica si el archivo JSON existe."""
        return self.ruta.exists()