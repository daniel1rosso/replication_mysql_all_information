"""Backup generator and downloader"""
import subprocess
import os
import tempfile
import mysql.connector
from mysql.connector import errorcode

class BackupDownloader:
    """
    Class to generate a backup of Database.
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

        # Verify the connection to the database
        try:
            conn = mysql.connector.connect(
                host=self.mysql_host,
                user=self.mysql_user,
                password=self.password,
                database=db_name
            )
            conn.close()
        except mysql.connector.Error as err:
            if err.errno == errorcode.ER_BAD_DB_ERROR:
                print(f"Database '{db_name}' does not exist. Cannot create backup.")
            else:
                print(f"Error: {err}")
            return

        # Create a temporary my.cnf file
        with tempfile.NamedTemporaryFile(delete=False, mode='w') as cnf_file:
            cnf_file.write(f"[client]\nuser={self.mysql_user}\npassword={self.password}\nhost={self.mysql_host}\n")
            cnf_file_path = cnf_file.name

        try:
            dump_command = (
                f"mysqldump --defaults-extra-file={cnf_file_path} "
                f"--databases {db_name} --events --routines "
                f"--no-create-db --skip-add-locks --complete-insert --tables > "
                f"backups/{backup_file}"
            )
            subprocess.run(dump_command, shell=True, check=True)
        except subprocess.CalledProcessError as e:
            print(f"Error trying to create backup for '{db_name}': {e}")
        else:
            print(f"Backup for '{db_name}' created successfully.")
        finally:
            os.remove(cnf_file_path)
            