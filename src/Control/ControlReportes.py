import pandas as pd
from pathlib import Path
from datetime import datetime

class ControlReportes:

    def __init__(self):
        Path("reportes").mkdir(exist_ok=True)  # Crea carpeta para reportes

    def generar_reporte_completo(self, correos):
        """Genera un CSV con todos los correos revisados."""
        if not correos:
            print("⚠️ No hay correos para generar reporte.")
            return
        
        df = pd.DataFrame(correos)
        fecha = datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
        ruta = f"reportes/reporte_completo_{fecha}.csv"
        df.to_csv(ruta, index=False, encoding="utf-8")
        print(f"📄 Reporte completo generado en: {ruta}")

    def generar_reporte_acciones(self, eliminados, marcados):
        """Genera un CSV con los correos eliminados y marcados como spam."""
        fecha = datetime.now().strftime("%Y-%m-%d_%H-%M-%S")

        # Eliminados
        if eliminados:
            df_e = pd.DataFrame(eliminados)
            df_e.to_csv(f"reportes/correos_eliminados_{fecha}.csv",
                        index=False, encoding="utf-8")
            print("🗑️ Reporte de eliminados generado.")

        # Marcados
        if marcados:
            df_m = pd.DataFrame(marcados)
            df_m.to_csv(f"reportes/correos_marcados_{fecha}.csv",
                        index=False, encoding="utf-8")
            print("🚩 Reporte de marcados generado.")

    def generar_resumen(self, total, eliminados, marcados):
        """Genera un archivo con conteo de acciones."""
        fecha = datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
        ruta = f"reportes/resumen_{fecha}.txt"

        with open(ruta, "w", encoding="utf-8") as f:
            f.write("📊 RESUMEN DE PROCESAMIENTO DE CORREOS\n\n")
            f.write(f"Total revisados: {total}\n")
            f.write(f"Eliminados: {len(eliminados)}\n")
            f.write(f"Marcados como spam: {len(marcados)}\n")

        print(f"📊 Resumen generado en: {ruta}")
