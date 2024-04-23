import subprocess

class BackupDownloader:
    def __init__(self, config):
        self.mysql_host = config.get("mysql_host")
        self.mysql_user = config.get("mysql_user")
        self.password = config.get("password")

    def create_backup(self, db_name):
        backup_file = f'backup_{db_name}.sql'

        try:
            dump_command = f"mysqldump -h {self.mysql_host} -u {self.mysql_user} -p{self.password} --databases {db_name} --events --routines --no-create-db --skip-add-locks --complete-insert --tables > backups/{backup_file}"
            subprocess.run(dump_command, shell=True, check=True)
        except subprocess.CalledProcessError as e:
            print(f"Error trying create copy'{db_name}': {e}")
        else:
            print(f"Security copy '{db_name}' created successful")
