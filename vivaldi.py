"""Orchester of all modules"""
from download_backup import BackupDownloader
from generate_database import MySQLMigration
from delete_parameters_backups import SQLFileProcessor
from list_name_databases import list_databases_to_migrate

config = {
"password" : "",
"mysql_host" : "",
"mysql_user" : ""
}

if __name__ == "__main__":
    print("Orchester running")

    downloader = BackupDownloader(config=config,)

    generator = MySQLMigration(config=config)

    processor = SQLFileProcessor(directory="backups")

    print("Classes initializer")
    for db in list_databases_to_migrate:
        print(f"Start database {db} ")
        downloader.create_backup(db_name=db)
        generator.connect()
        generator.create_schemas()
        generator.close_connection()
        processor.process_sql_files()

        print(f"Finish process {db}")
