"""Module to migrate all grants"""
from mysql.connector.errors import ProgrammingError

class GrantManager:
    """Class to manage grants migration between MySQL databases."""
    def __init__(self, conn_origen, conn_destino, cursor_origen, cursor_destino):
        self.conn_origen = conn_origen
        self.conn_destino = conn_destino
        self.cursor_origen = cursor_origen
        self.cursor_destino = cursor_destino
        
    def migrate_grants(self, db_name):
        """Migrates grants from source to destination databases."""
        if not self.conn_origen or not self.cursor_origen or not self.conn_destino or not self.cursor_destino:
            print("Error: Connections not established.")
            return
        print(f"Database: {db_name}")

        self.cursor_origen.execute(f"SELECT DISTINCT User FROM mysql.db WHERE Db='{db_name}' AND User NOT LIKE 'mysql.%'")
        usuarios = self.cursor_origen.fetchall()

        if usuarios:
            for usuario in usuarios:
                usuario = usuario[0]
                print(f"Grants for user {usuario}:")
                self.cursor_origen.execute(f"SHOW GRANTS FOR '{usuario}'@'%'")
                grants = self.cursor_origen.fetchall()

                if grants:
                    for grant in grants:
                        print(grant[0])

                        try:
                            self.cursor_destino.execute(grant[0])
                        except ProgrammingError as e:
                            print(f"Error executing grant for {usuario}: {e}")
                            continue
        else:
            print(f"No users found in database {db_name}")

        self.conn_destino.commit()
        print("Grants migration completed")