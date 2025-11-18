from src.Control.Opciones import Opciones as opciones


class Menu:
    """
    Clase que representa el menú principal de la aplicación.
    """
    def __init__(self):        
        self.menu_history = ["principal"]

    def ir_a_filtros(self):
        self.menu_history.append("filtros")

    def mostrar_menu(self):        
        if self.menu_history[-1] == "principal":
            return self.mostrar_principal()
        elif self.menu_history[-1] == "filtros":
            return self.mostrar_filtros()

    def ir_atras(self):
        if len(self.menu_history) > 1:
            self.menu_history.pop()        

    def mostrar_principal(self):        
        print("\n=== Menú Principal ===")
        print("1. Cambiar usuario y contraseña")
        print("2. Modificar criterios de filtrado")
        print("3. Eliminar correos")
        print("4. Marcar correos como Spam")
        print("0. Salir")
        opcion = input("Seleccione una opción: ")
        #return self.menu_options.get(opcion, None)
        if opcion == "1":
            opcion = opciones.CAMBIAR_CREDENCIALES
        elif opcion == "2":
            opcion = opciones.MODIFICAR_CRITERIOS
        elif opcion == "3":
            opcion = opciones.ELIMINAR_CORREOS
        elif opcion == "4":
            opcion = opciones.MARCAR_COMO_SPAM
        elif opcion == "0":
            opcion = opciones.SALIR
        return opcion
    
    def mostrar_filtros(self):        
        print("\n=== Menú Filtros ===")
        print("1. Agregar palabra/frase a los filtros")
        print("2. Quitar palabra/frase de los filtros")
        print("3. Agregar remitente a los filtros")
        print("4. Eliminar remitente de los filtros")
        print("5. Eliminar todos los filtros")
        print("0. Atrás")
        opcion = input("Seleccione una opción: ") 
        if opcion == "1":
            opcion = opciones.AGREGAR_PALABRA
        elif opcion == "2":
            opcion = opciones.ELIMINAR_PALABRA
        elif opcion == "3":
            opcion = opciones.AGREGAR_REMITENTE
        elif opcion == "4":
            opcion = opciones.ELIMINAR_REMITENTE
        elif opcion == "5":
            opcion = opciones.ELIMINAR_TODOS_FILTROS
        elif opcion == "0":
            opcion = opciones.ATRAS
        return opcion

    def continuar(self, mensaje):
        respuesta = input(f"{mensaje} (s/n): ").lower()
        return respuesta == 's'
        

