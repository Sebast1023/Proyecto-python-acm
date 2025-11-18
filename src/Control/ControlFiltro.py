from src.Modelo.ConexionJson import ConexionJSON

class ControlFiltro:
    def __init__(self):
        self.conexion_json = ConexionJSON("specs/filtros.json")

    def obtener_filtros(self):
        datos = self.conexion_json.leer_datos()
        if datos is None:
            raise FileNotFoundError("❌ No se pudo leer el archivo de filtros.")
        if datos.get("palabras_clave") is None or datos.get("remitentes") is None:
            raise KeyError("El JSON debe tener las claves 'palabras_clave' y 'remitentes'.")
        return datos
    
    def guardar_filtros(self, palabras_clave, remitentes):
        datos = {
            "palabras_clave": palabras_clave,
            "remitentes": remitentes
        }
        self.conexion_json.escribir_datos(datos)
        print("✅ Filtros guardados correctamente.")
        

