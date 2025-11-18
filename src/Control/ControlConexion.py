from src.Modelo.ConexionJson import ConexionJSON


class ControlConexion:
    def __init__(self):
        self.conexion_json = ConexionJSON()

    def obtener_credenciales(self):
        """Lee las credenciales del JSON y valida su contenido."""
        datos = self.conexion_json.leer_datos()

        if datos is None:
            raise FileNotFoundError("❌ No se pudo leer el archivo de credenciales.")

        if "email" not in datos or "password" not in datos:
            raise KeyError("⚠️ El JSON debe tener las claves 'email' y 'password'.")

        correo = datos["email"]
        contrasena = datos["password"]

        if not correo or not contrasena:
            raise ValueError("⚠️ Las credenciales están vacías o incompletas.")

        print("✅ Credenciales cargadas correctamente.")
        return correo, contrasena
    
    def guardar_credenciales(self, email, password):
        """Guarda las credenciales en el archivo JSON."""
        datos = {
            "email": email,
            "password": password
        }
        self.conexion_json.escribir_datos(datos)
