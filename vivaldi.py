"""Orchester of all modules"""
from download_backup import BackupDownloader
from generate_database import MySQLMigration
from delete_parameters_backups import SQLFileProcessor
from restore_backup import DatabaseRestorer
from connection_manager import ConnectionManager
from grants_db import GrantManager
from list_name_databases import list_databases_to_migrate

config_extract = {
    "password" : "",
    "mysql_host" : "",
    "mysql_user" : ""
}

config_restore = {
    "password" : "",
    "mysql_host" : "",
    "mysql_user" : ""
}

if __name__ == "__main__":
    print("Orchester running")

    connect_origin = ConnectionManager(config_extract)
    connect_restore = ConnectionManager(config_restore)

    conn_origin , cursor_origin = connect_origin.connect()
    conn_restore, cursor_restore = connect_restore.connect()

    downloader = BackupDownloader(config=config_extract)

    generator = MySQLMigration(cursor=cursor_origin, conn=conn_origin)

    restore = DatabaseRestorer(config= config_restore)
    processor = SQLFileProcessor(directory="backups")

    grants = GrantManager(conn_origen=conn_origin, conn_destino=conn_restore, cursor_origen=cursor_origin, cursor_destino=cursor_restore)

    print("Classes initializer")
    for db in list_databases_to_migrate:
        print(f"Start database {db} ")
        downloader.create_backup(db_name=db)

        generator.create_schemas(db_name=db)

        restore.restore_databases(db_name=db)

        processor.process_sql_files()
        print(f"Finish process {db}")


    connect_origin.close_connection()
    connect_restore.close_connection()
