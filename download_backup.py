"""Backup generator and downloader"""
import subprocess

class BackupDownloader:
    """
    Class to generate a backup of Database
    """
    def __init__(self, config):
        """
        Initializes the BackupDownloader object.

        Args:
            config (dict): Configuration for database connection.
                Requires 'password', 'mysql_host', and 'mysql_user'.
        """
        self.mysql_host = config.get("mysql_host")
        self.mysql_user = config.get("mysql_user")
        self.password = config.get("password")

    def create_backup(self, db_name):
        """
        Creates a backup for the specified database.

        Args:
            db_name (str): Name of the database.
        """
        backup_file = f'backup_{db_name}.sql'

        try:
            dump_command = (
                f"mysqldump -h {self.mysql_host} -u {self.mysql_user} "
                f"-p{self.password} --databases {db_name} --events --routines "
                f"--no-create-db --skip-add-locks --complete-insert --tables > "
                f"backups/{backup_file}"
            )
            subprocess.run(dump_command, shell=True, check=True)
        except subprocess.CalledProcessError as e:
            print(f"Error trying create copy'{db_name}': {e}")
        else:
            print(f"Security copy '{db_name}' created successful")
