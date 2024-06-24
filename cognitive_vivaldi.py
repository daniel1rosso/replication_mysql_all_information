# Importar las clases necesarias
from download_backup import BackupDownloader
from generate_database import MySQLMigration
from delete_parameters_backups import SQLFileProcessor
from restore_backup import DatabaseRestorer
from connection_manager import ConnectionManager
from grants_db import GrantManager
from list_name_databases import list_databases_to_migrate

config_extract = {
    "password": "",
    "mysql_host": "",
    "mysql_user": ""
}

config_restore = {
    "password": "",
    "mysql_host": "",
    "mysql_user": ""
}

class Orchestrator:
    def __init__(self, config_extract, config_restore):
        self.config_extract = config_extract
        self.config_restore = config_restore
        self.connect_origin = ConnectionManager(config_extract)
        self.connect_restore = ConnectionManager(config_restore)
        self.conn_origin, self.cursor_origin = self.connect_origin.connect()
        self.conn_restore, self.cursor_restore = self.connect_restore.connect()
        self.downloader = BackupDownloader(config=config_extract)
        self.generator = MySQLMigration(cursor=self.cursor_origin, conn=self.conn_origin)
        self.restore = DatabaseRestorer(config=config_restore)
        self.processor = SQLFileProcessor(directory="backups")
        self.grants = GrantManager(conn_origen=self.conn_origin, conn_destino=self.conn_restore, cursor_origen=self.cursor_origin, cursor_destino=self.cursor_restore)

    def bind_tools(self, tools):
        self.tools = tools

    def invoke(self, task_name, **kwargs):
        task = self.tools.get(task_name)
        if not task:
            raise ValueError(f"Task {task_name} not found.")
        
        method_name = task.get('method')
        if not method_name:
            raise ValueError(f"Method not defined for task {task_name}.")
        
        method = getattr(self, method_name, None)
        if not method:
            raise ValueError(f"Method {method_name} not found in Orchestrator.")
        
        return method(**kwargs)

    def create_backup(self, db_name):
        self.downloader.create_backup(db_name=db_name)
    
    def create_schemas(self, db_name):
        self.generator.create_schemas(db_name=db_name)
    
    def restore_databases(self, db_name):
        self.restore.restore_databases(db_name=db_name)
    
    def process_sql_files(self):
        self.processor.process_sql_files()
    
    def full_migration(self):
        for db in list_databases_to_migrate:
            print(f"Start processing database {db}")
            self.create_backup(db_name=db)
            self.create_schemas(db_name=db)
            self.restore_databases(db_name=db)
            self.process_sql_files()
            print(f"Finish processing {db}")

# Configuración de herramientas
tools = {
    "create_backup": {
        "method": "create_backup",
        "description": "Create a backup for each databases into list_databases_to_migrate",
        "parameters": {
            "db_name": "string"
        }
    },
    "create_schemas": {
        "method": "create_schemas",
        "description": "Create a schema for each databases into list_databases_to_migrate",
        "parameters": {
            "db_name": "string"
        }
    },
    "restore_databases": {
        "method": "restore_databases",
        "description": "Restore databases for each databases into list_databases_to_migrate",
        "parameters": {
            "db_name": "string"
        }
    },
    "process_sql_files": {
        "method": "process_sql_files",
        "description": "Delete ROW_FORMAT=FIXED in all databases",
        "parameters": {}
    },
    "full_migration": {
        "method": "full_migration",
        "description":"Run all steps to migrate database, from download backup to generate backup",
        "parameters": {}
    }
}

if __name__ == "__main__":
    orchestrator = Orchestrator(config_extract=config_extract, config_restore=config_restore)
    orchestrator.bind_tools(tools)

    orchestrator.invoke("full_migration")
