"""Module to restore db"""
import subprocess
##TODO: We should refactor that class because we need to use mysel.connector
class DatabaseRestorer:
    """Class to restore databases."""
    def __init__(self, config):
        self.mysql_host = config.get("mysql_host")
        self.password = config.get("mysql_password")
        self.mysql_user = config.get("mysql_user")

    def restore_databases(self, db_name):
        """Function to restore backup."""
        backup_file = f'backup_{db_name}.sql'
        print("db_name", db_name)

        check_db_command = (
            f"mysql -h {self.mysql_host} -u {self.mysql_user} "
            f"-p{self.password} -e \"USE `{db_name}`\""
        )
        try:
            subprocess.run(check_db_command, shell=True, check=True)
        except subprocess.CalledProcessError:
            print(f"Database '{db_name}' does not exist. Skipping...")

        create_db_command = (
            f"mysql -h {self.mysql_host} -u {self.mysql_user} "
            f"-p{self.password} -e \"CREATE DATABASE IF NOT EXISTS `{db_name}`\""
        )

        subprocess.run(create_db_command, shell=True, check=True)

        restore_command = (
            f"mysql -h {self.mysql_host} -u {self.mysql_user} "
            f"-p{self.password} {db_name} < backups/{backup_file}"
        )
        subprocess.run(restore_command, shell=True, check=True)
