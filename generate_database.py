"""Creator of databases"""
import mysql.connector
from list_name_databases import list_databases_to_migrate

class MySQLMigration:
    """Class responsable of connect and create schemas"""
    def __init__(self, config):
        """
        Initializes the MySQLMigration object.

        Args:
            config (dict): Configuration for database connection.
                Requires 'password', 'mysql_host', and 'mysql_user'.
        """
        self.config = config
        self.conn = None
        self.cursor = None

    def connect(self):
        """Establishes connection to the database."""
        try:
            self.conn = mysql.connector.connect(**self.config)
            self.cursor = self.conn.cursor()
            print("Connection to MySQL successful")
        except mysql.connector.Error as err:
            print(f"Houston, we have a error: {err}")

    def create_schemas(self,db_name):
        """Creates schemas in the database."""
        if not self.conn or not self.cursor:
            print("Error: Don't have connection.")
            return

        try:
            self.cursor.execute(f"CREATE SCHEMA {db_name}")
            print(f"Schema '{db_name}' created successful")
        except mysql.connector.Error as err:
            print(f"Error creating schema '{db_name}': {err}")

    def close_connection(self):
        """Closes connection to the database."""
        if self.cursor:
            self.cursor.close()
        if self.conn:
            self.conn.close()
            print("Connection closed")
