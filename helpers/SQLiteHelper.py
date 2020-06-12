import sqlite3
from sqlite3 import Error

class SQLiteHelper():
    def __init__(self, connection_path: str):
        self.__connection_path = connection_path
        self.__connection = None

    def create_connection(self):
        try:
            if(self.__connection == None):
                self.__connection = sqlite3.connect(self.__connection_path)
            print("Connection to SQLite DB successful")
        except Error as e:
            print(f"The error '{e}' occurred")

    def execute_query(self, query):
        if(self.__connection == None):
            print("Connection has not been created")
        
        cursor = self.__connection.cursor()
        try:
            cursor.execute(query)
            self.__connection.commit()
            print("Query executed successfully")
            return True
        except Error as e:
            print(f"The error '{e.with_traceback}' occurred")
            return False

    def create_table(self, table_name: str, table_format: str):
        '''
        example_usage -->

        ex_table_name = "users"

        ex_table_format = "(
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT NULL,
            age INTEGER,
            gender TEXT,
            nationality TEXT
        )"

        ~~~

        CREATE TABLE IF NOT EXISTS users (

            id INTEGER PRIMARY KEY AUTOINCREMENT,

            name TEXT NOT NULL,

            age INTEGER,

            gender TEXT,

            nationality TEXT

        );
        '''
        table_query = f"""
        CREATE TABLE IF NOT EXISTS {table_name} {table_format};
        """
        return self.execute_query(table_query)


    def insert_records(self, table_name: str, column_list: str, values: list):
        '''
        example usage -->
        
        ex_table_name = "users",
        
        ex_column_list = "(name, age, gender, nationality)",
        
        ex_values = ["('James', 25, 'male', 'USA')", "('Leila', 32, 'female', 'France')"]

        ~~~

        INSERT INTO users (name, age, gender, nationality)

        VALUES
        
            ('James', 25, 'male', 'USA'),
            
            ('Leila', 32, 'female', 'France');
        '''
        value_str = ",".join(values)
        table_query = f"""
        INSERT INTO
            {table_name} {column_list}
        VALUES
            {value_str};
        """

        return self.execute_query(table_query)

    def execute_read_query(self, query):
        cursor = self.__connection.cursor()
        result = None
        try:
            cursor.execute(query)
            result = cursor.fetchall()
            return result
        except Error as e:
            print(f"Problem reading - the error '{e}' occurred")

    def execute_delete_query(self, table_name: str, conditions: str):
        delete_query = f"DELETE FROM {table_name} WHERE {conditions}"
        return self.execute_query(delete_query)

    def execute_update_query(self, table_name: str, new_column_data: str, conditions: str):
        update_query = f"""
        UPDATE
            {table_name}
        SET
            {new_column_data}
        WHERE
            {conditions}
        """
        return self.execute_query(update_query)