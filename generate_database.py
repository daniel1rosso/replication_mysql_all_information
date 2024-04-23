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
            print("Conexión exitosa a MySQL")
        except mysql.connector.Error as err:
            print("Error de conexión a MySQL: {}".format(err))

    def create_schemas(self):
        if not self.conn or not self.cursor:
            print("Error: No hay conexión establecida.")
            return

        for schema_name in list_databases_to_migrate:
            try:
                self.cursor.execute("CREATE SCHEMA `{}`".format(schema_name))
                print("Esquema '{}' creado exitosamente".format(schema_name))
            except mysql.connector.Error as err:
                print("Error al crear el esquema '{}': {}".format(schema_name, err))

    def close_connection(self):
        if self.cursor:
            self.cursor.close()
        if self.conn:
            self.conn.close()
            print("Conexión cerrada")
