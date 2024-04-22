from list_name_databases import list_databases_to_migrate
import mysql.connector

config = {
  'user': '',
  'password': '',
  'host': '',
  'raise_on_warnings': True
}

try:
  conn = mysql.connector.connect(**config)
  cursor = conn.cursor()
  print("Conexión exitosa a MySQL")

  # Crear cada esquema en la lista
  for schema_name in list_databases_to_migrate:
      try:
          cursor.execute("CREATE SCHEMA `{}`".format(schema_name))
          print("Esquema '{}' creado exitosamente".format(schema_name))
      except mysql.connector.Error as err:
          print("Error al crear el esquema '{}': {}".format(schema_name, err))

  cursor.close()
  conn.close()
  print("Conexión cerrada")
except mysql.connector.Error as err:
    print("Error de conexión a MySQL: {}".format(err))
