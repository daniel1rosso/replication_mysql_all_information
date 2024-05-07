import mysql.connector 

class ConnectionManager():
    def __init__(self, config) -> None:
        self.config = config
        self.conn = None
        self.cursor = None
    def connect(self):
        
        """Establishes connection to the database."""
        try:
            self.conn = mysql.connector.connect(**self.config)
            self.cursor = self.conn.cursor()
            print("Connection to MySQL successful")
            return self.conn, self.cursor
        except mysql.connector.Error as err:
            print(f"Houston, we have a error: {err}")

    def close_connection(self):
        """Closes connection to the database."""
        if self.cursor:
            self.cursor.close()
        if self.conn:
            self.conn.close()
            print("Connection closed")