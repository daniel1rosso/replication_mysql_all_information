"""Module to restore db"""
import mysql.connector
from mysql.connector import errorcode

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
        
        # Try to connect to the database
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
                print(f"Database '{db_name}' does not exist. Creating...")
                try:
                    conn = mysql.connector.connect(
                        host=self.mysql_host,
                        user=self.mysql_user,
                        password=self.password
                    )
                    cursor = conn.cursor()
                    cursor.execute(f"CREATE DATABASE `{db_name}`")
                    conn.close()
                except mysql.connector.Error as err:
                    print(f"Failed to create database: {err}")
                    return
            else:
                print(f"Error: {err}")
                return

        # Restore the database
        try:
            conn = mysql.connector.connect(
                host=self.mysql_host,
                user=self.mysql_user,
                password=self.password,
                database=db_name
            )
            cursor = conn.cursor()
            with open(f'backups/{backup_file}', 'r') as file:
                sql_commands = file.read().split(';')
                for command in sql_commands:
                    if command.strip():
                        cursor.execute(command)
            conn.commit()
            cursor.close()
            conn.close()
            print(f"Database '{db_name}' restored successfully.")
        except mysql.connector.Error as err:
            print(f"Error: {err}")
        except FileNotFoundError:
            print(f"Backup file '{backup_file}' not found.")
