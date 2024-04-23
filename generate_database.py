import mysql.connector
from list_name_databases import list_databases_to_migrate

class MySQLMigration:
    def __init__(self, config):
        self.config = config
        self.conn = None
        self.cursor = None

    def connect(self):
        try:
            self.conn = mysql.connector.connect(**self.config)
            self.cursor = self.conn.cursor()
            print("Connection to MySQL successful")
        except mysql.connector.Error as err:
            print("Houston, we have a error: {}".format(err))

    def create_schemas(self):
        if not self.conn or not self.cursor:
            print("Error: Don't have connection.")
            return

        for schema_name in list_databases_to_migrate:
            try:
                self.cursor.execute("CREATE SCHEMA `{}`".format(schema_name))
                print("Schema '{}' created successful".format(schema_name))
            except mysql.connector.Error as err:
                print("Error creating schema '{}': {}".format(schema_name, err))

    def close_connection(self):
        if self.cursor:
            self.cursor.close()
        if self.conn:
            self.conn.close()
            print("Connection closed")
