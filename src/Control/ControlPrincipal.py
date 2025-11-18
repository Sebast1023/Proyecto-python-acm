from src.Control.ControlConexion import ControlConexion
from src.Control.ControlCorreo import ControlCorreo
from src.Vista.Menu import Menu
from src.Control.ControlFiltro import ControlFiltro
from src.Control.Opciones import Opciones
from src.Control.Utilidades import Utilidades
from email.utils import parseaddr

class ControlPrincipal:
    def __init__(self):
        self.control_conexion = ControlConexion()
        self.control_filtro = ControlFiltro()
        self.menu = Menu()
        self.ejecutar()

    def ejecutar(self):
        while True:
            opcion = self.menu.mostrar_menu()
            
            if opcion == Opciones.CAMBIAR_CREDENCIALES:
                self.cambiar_credenciales()

            elif opcion == Opciones.MODIFICAR_CRITERIOS:                
                self.menu.ir_a_filtros()

            elif opcion == Opciones.AGREGAR_PALABRA:
                palabra = input("Ingrese la palabra/frase a agregar a los filtros: ")
                filtros = self.control_filtro.obtener_filtros()
                if palabra.strip() == "":
                    print("La palabra/frase no puede estar vacía.")
                    continue
                if not (palabra in filtros["palabras_clave"]):
                    filtros["palabras_clave"].append(palabra)                  
                self.control_filtro.guardar_filtros(filtros["palabras_clave"], filtros["remitentes"])
                print("Palabras actuales en los filtros:", filtros["palabras_clave"]) 

            elif opcion == Opciones.ELIMINAR_PALABRA:
                filtros = self.control_filtro.obtener_filtros()
                print("Palabras/frases actuales en los filtros:", filtros["palabras_clave"])                    
                palabra = input("Ingrese la palabra/frase a eliminar de los filtros: ")  
                              
                if palabra in filtros["palabras_clave"]:
                    filtros["palabras_clave"].remove(palabra)
                    self.control_filtro.guardar_filtros(filtros["palabras_clave"], filtros["remitentes"])
                else:
                    print("La palabra/frase no está en los filtros.")

            elif opcion == Opciones.AGREGAR_REMITENTE:
                remitente = input("Ingrese el remitente a agregar a los filtros: ").lower()
                if remitente.strip() == "":
                    print("El remitente no puede estar vacío.")
                    continue
                if Utilidades.validar_email(remitente) is False:
                    print("Formato de correo no valido")
                    continue
                filtros = self.control_filtro.obtener_filtros()
                if not (remitente in filtros["remitentes"]):
                    filtros["remitentes"].append(remitente)
                self.control_filtro.guardar_filtros(filtros["palabras_clave"], filtros["remitentes"])
                print("Remitentes actuales en los filtros:", filtros["remitentes"])

            elif opcion == Opciones.ELIMINAR_REMITENTE:
                remitente = input("Ingrese el remitente a eliminar de los filtros: ")
                filtros = self.control_filtro.obtener_filtros()
                if remitente in filtros["remitentes"]:
                    filtros["remitentes"].remove(remitente)
                    self.control_filtro.guardar_filtros(filtros["palabras_clave"], filtros["remitentes"])
                else:
                    print("El remitente no está en los filtros.")

            elif opcion == Opciones.ELIMINAR_TODOS_FILTROS:
                if self.menu.continuar("¿Está seguro de que desea eliminar todos los filtros?"):
                    self.control_filtro.guardar_filtros([], [])
                    print("Todos los filtros han sido eliminados.")                        

            elif opcion == Opciones.ELIMINAR_CORREOS:        
                filtros = self.control_filtro.obtener_filtros()
                print("Filtros actuales:", filtros["palabras_clave"], filtros["remitentes"])    
                if self.menu.continuar("¿Desea continuar?"):                    
                    self.eliminar_correos()                

            elif opcion == Opciones.MARCAR_COMO_SPAM:
                print("Filtros actuales:", filtros["palabras_clave"], filtros["remitentes"])    
                if self.menu.continuar("¿Desea continuar?"):                    
                    self.marcar_correos()                  

            elif opcion == Opciones.ATRAS: 
                self.menu.ir_atras()        

            elif opcion == Opciones.SALIR: 
                print("Saliendo de la aplicación")
                break            
            else:
                print("Opción no válida. Intente de nuevo")        

    def cambiar_credenciales(self):
        email_account = input("Ingrese el nuevo correo electrónico: ")
        if email_account.strip() == ":q":
            return
        if Utilidades.validar_email(email_account) is False:
            print("Formato de correo no valido")
            return
        password = input("Ingrese la nueva contraseña: ")
        if password.strip() == ":q":
            return        
        if email_account == "" or password == "":
            print("El correo y la contraseña no pueden estar vacíos.")
            return
        try:
            self.control_conexion.guardar_credenciales(email_account, password)            
            print("Credenciales actualizadas correctamente. ")
        except Exception as e:
            print("Error al guardar las credenciales:", e)
        

    def eliminar_correos(self):
        try:
            email_account, password = self.control_conexion.obtener_credenciales()
            self.procesar_correos(email_account, password)
        except Exception as e:
            print("Error al borrar correo:", e)

    def marcar_correos(self):
        try:
            email_account, password = self.control_conexion.obtener_credenciales()
            self.procesar_correos(email_account, password, "marcar")
        except Exception as e:
            print("Error al marcar correos:", e)

    def procesar_correos(self, email_account, password, opcion="eliminar"):
        print("📬 Leyendo correos...")
        correo_control = ControlCorreo(email_account, password)
        correos = correo_control.leer_todos()
        filtros = self.control_filtro.obtener_filtros()

        if opcion == "eliminar":        
            eliminados = 0

            for c in correos:
                asunto = c["asunto"].lower()
                nombre, remitente = parseaddr(c["remitente"].lower())
                if asunto in filtros["palabras_clave"] or remitente in filtros["remitentes"]:
                    print(f"🗑️ Eliminando correo con asunto: {c['asunto']}")
                    correo_control.eliminar_correo(c["id"])
                    eliminados += 1
                else:
                    print(f"✅ Correo válido: {c['asunto']}")

            correo_control.cerrar()
            print(f"\n🔹 Proceso finalizado. Correos eliminados: {eliminados}")

        elif opcion == "marcar":
            marcados = 0
            for c in correos:
                asunto = c["asunto"].lower()
                if "spam" in asunto or "promocion" in asunto:
                    print(f"Marcado como spam correo con asunto: {c['asunto']}")
                    correo_control.marcar_correo(c["id"])
                    marcados += 1
                else:
                    print(f"✅ Correo válido: {c['asunto']}")
            correo_control.cerrar()
            print(f"\n🔹 Proceso finalizado. Correos marcados como spam: {marcados}")

