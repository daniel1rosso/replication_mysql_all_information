import os
import re

class SQLFileProcessor:
    def __init__(self, directory):
        self.directory = directory

    def eliminar_row_format_fixed(self, filename):
        try:
            with open(filename, 'r', encoding='utf-8') as file:
                lines = file.readlines()

            with open(filename, 'w', encoding='utf-8') as file:
                for line in lines:
                    line = re.sub(r'ROW_FORMAT=FIXED', '', line)
                    file.write(line)

            print(f"Deleted 'ROW_FORMAT=FIXED' into the file {filename}")
        except Exception as e:
            print(f"Error trying delete 'ROW_FORMAT=FIXED' into the file {filename}: {e}")

    def process_sql_files(self):
        for filename in os.listdir(self.directory):
            if filename.endswith(".sql"):
                file_path = os.path.join(self.directory, filename)
                self.eliminar_row_format_fixed(file_path)
