from list_name_databases import list_databases_to_migrate
import subprocess

password = ""
mysql_host = ""
mysql_user = ""

for db_name in list_databases_to_migrate:
    backup_file = f'backup_{db_name}.sql'

    # Check if MariaDB version supports --grants
    try:
        # Attempt using --grants if possible
        dump_command = f"mysqldump -h {mysql_host} -u {mysql_user} -p{password} --databases {db_name} --events --routines --no-create-db --skip-add-locks --complete-insert --tables > backups/{backup_file}"
        subprocess.run(dump_command, shell=True)
    except subprocess.CalledProcessError as e:
        print(f"Error using --grants: {e}")
        # Fallback: Export schema without grants
        dump_command = f"mysqldump -h {mysql_host} -u {mysql_user} -p{password} --databases {db_name} --events --routines --no-create-db --skip-add-lock --skip-disable-innodb-engines --complete-insert --tables > backups/{backup_file}"
        subprocess.run(dump_command, shell=True)
