import os
import re

# Directorio que contiene los archivos .sql
directorio = "backups"

# Función para escanear los archivos .sql en el directorio y eliminar la parte de la línea que contiene ROW_FORMAT=FIXED
def eliminar_row_format_fixed(filename):
    with open(filename, 'r', encoding='utf-8') as file:
        lines = file.readlines()

    with open(filename, 'w', encoding='utf-8') as file:
        for line in lines:
            # Utilizamos expresión regular para encontrar y reemplazar ROW_FORMAT=FIXED
            line = re.sub(r'ROW_FORMAT=FIXED', '', line)
            file.write(line)

# Escanea todos los archivos .sql en el directorio
for filename in os.listdir(directorio):
    if filename.endswith(".sql"):
        file_path = os.path.join(directorio, filename)
        try:
            eliminar_row_format_fixed(file_path)
            print(f"Se ha eliminado 'ROW_FORMAT=FIXED' en el archivo {filename}")
        except Exception as e:
            print(f"Error eliminando 'ROW_FORMAT=FIXED' en el archivo {filename}: {e}")

print("Proceso completado.")