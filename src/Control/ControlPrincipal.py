from ControlConexion import ControlConexion
from ControlCorreo import ControlCorreo


class ControlPrincipal:
    def __init__(self):
        self.control_conexion = ControlConexion()
        self.ejecutar()

    def ejecutar(self):
        try:
            email_account, password = self.control_conexion.obtener_credenciales()
            self.procesar_correos(email_account, password)
        except Exception as e:
            print("❌ Error al iniciar la aplicación:", e)

    def procesar_correos(self, email_account, password):
        print("📬 Leyendo correos...")
        correo_control = ControlCorreo(email_account, password)
        correos = correo_control.leer_todos()
        eliminados = 0

        for c in correos:
            asunto = c["asunto"].lower()
            if "spam" in asunto or "promocion" in asunto:
                print(f"🗑️ Eliminando correo con asunto: {c['asunto']}")
                correo_control.eliminar_correo(c["id"])
                eliminados += 1
            else:
                print(f"✅ Correo válido: {c['asunto']}")

        correo_control.cerrar()
        print(f"\n🔹 Proceso finalizado. Correos eliminados: {eliminados}")
