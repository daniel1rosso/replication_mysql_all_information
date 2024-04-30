"""Orchester of all modules"""
from download_backup import BackupDownloader
from generate_database import MySQLMigration
from delete_parameters_backups import SQLFileProcessor
from restore_backup import DatabaseRestorer
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

    downloader = BackupDownloader(config=config_extract)

    generator = MySQLMigration(config=config_extract)

    restore = DatabaseRestorer(config= config_restore)
    processor = SQLFileProcessor(directory="backups")
    generator.connect()
    print("Classes initializer")
    for db in list_databases_to_migrate:
        print(f"Start database {db} ")
        downloader.create_backup(db_name=db)

        generator.create_schemas(db_name = db)
        restore.restore_databases(db_name=db)
        processor.process_sql_files()
        print(f"Finish process {db}")
    generator.close_connection()
    
