import os

# Directorio que contiene los archivos .sql
directorio = "backups"

# Función para escanear los archivos .sql en el directorio y eliminar la línea que contiene ROW_FORMAT=FIXED
def eliminar_row_format_fixed(filename):
    with open(filename, 'r', encoding='utf-8') as file:
        lines = file.readlines()

    with open(filename, 'w', encoding='utf-8') as file:
        for line in lines:
            if "ROW_FORMAT=FIXED" not in line:
                file.write(line)

# Escanea todos los archivos .sql en el directorio
for filename in os.listdir(directorio):
    if filename.endswith(".sql"):
        file_path = os.path.join(directorio, filename)
        eliminar_row_format_fixed(file_path)
        print(f"Se ha eliminado la línea 'ROW_FORMAT=FIXED' en el archivo {filename}")

print("Proceso completado.")