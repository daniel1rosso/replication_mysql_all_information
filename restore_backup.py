from list_name_databases import list_databases_to_migrate
import subprocess

password = ""
mysql_host = ""
mysql_user = ""

for db_name in list_databases_to_migrate:
    backup_file = f'backup_{db_name}.sql'
    print("db_name", db_name)
    
    # Verificar si la base de datos existe
    check_db_command = f"mysql -h {mysql_host} -u {mysql_user} -p{password} -e \"USE `{db_name}`\""
    try:
        subprocess.run(check_db_command, shell=True, check=True)
    except subprocess.CalledProcessError as e:
        print(f"Database '{db_name}' does not exist. Skipping...")
        continue
    
    # Crear la base de datos si no existe
    create_db_command = f"mysql -h {mysql_host} -u {mysql_user} -p{password} -e \"CREATE DATABASE IF NOT EXISTS `{db_name}`\""
    subprocess.run(create_db_command, shell=True, check=True)
    
    # Restaurar la base de datos
    restore_command = f"mysql -h {mysql_host} -u {mysql_user} -p{password} {db_name} < backups/{backup_file}"
    subprocess.run(restore_command, shell=True)
