"""Creator of databases"""
import mysql.connector

class MySQLMigration:
    """Class responsable of connect and create schemas"""
    def __init__(self, conn, cursor):
        """
        Initializes the MySQLMigration object.

        Args:
            config (dict): Configuration for database connection.
                Requires 'password', 'mysql_host', and 'mysql_user'.
        """
        self.conn = conn
        self.cursor = cursor

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


