import subprocess

# Función para ejecutar un script y esperar a que termine
def ejecutar_script(script):
    subprocess.run(["python", script], check=True)

# Ejecutar los scripts en orden
scripts = ["download_backup.py", "create_database.py", "delete_parameters_backups.py", "restore_backup.py"]

for script in scripts:
    print(f"Ejecutando {script}...")
    ejecutar_script(script)
    print(f"{script} ha terminado.")

print("Proceso completado.")
