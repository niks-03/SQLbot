from mysql import connector

class DBconnection:
    def __init__(self):
        self.conn = None
        self.host = None
        self.user = None
        self.password = None

    def initialize_credentials(self, password: str, host: str, user: str):
        self.host = host
        self.user = user
        self.password = password
        
        return self.connect()

    def connect(self):
        try:
            self.conn = connector.connect(
                host=self.host,
                user=self.user,
                password=self.password
            )
            self.cursor = self.conn.cursor()
            print("\nDatabase connected\n")
            return True
        except Exception as e:
            print(f"\nConnection error: {e}\n")
            return False
        
    def disconnect(self):
        if self.conn:
            try:
                self.conn.close()
                self.conn = None
                print("\nDatabase disconnected\n")
                return True
            except Exception as e:
                print(f"\nDisconnection error: {e}\n")
                return False
        else:
            return False
        
    def create_schema(self, schema_name: str):
        if schema_name:
            if self.conn:
                try:
                    self.cursor.execute(f"CREATE DATABASE {schema_name};")
                    self.conn.commit()
                    print(f"\n schema {schema_name} created\n")
                    return True
                except Exception as e:
                    print(f"\nerror creating schema: {e}\n")
                    return False
            else:
                print("no active database conection")
                return False
        
    def get_schemas(self):
        if self.conn:
            self.cursor.execute("SHOW DATABASES;")
            raw_results = self.cursor.fetchall()
            schemas = [result[0] for result in raw_results]

            return schemas
        else:
            print("no active database connection")
            return False
        
    def create_table(self, columns, data_types, schema, table_name):
        print(f"\ncolumns: {columns}\n types: {data_types}\n schema: {schema}\n tablename: {table_name}\n")
        if self.conn:
            if self.cursor:
                query_columns = ", ".join([i+" "+j for i, j in zip(columns[1:], data_types[1:])])
                print(f"*****\nCREATE TABLE if not exists {table_name} ({query_columns});*******\n")
                self.cursor.execute(f"CREATE TABLE if not exists {table_name} ({query_columns});")
                self.conn.commit()
                print("table created successfully")
                return True
            else:
                print("no active database connection")
                return False
        else:
            print("no active database connection")
            return False
        
    def get_tables(self, schema: str):
        if self.conn:
            if schema:
                self.cursor.execute(f"USE {schema};")
                self.cursor.execute("SHOW TABLES;")
                raw_results = self.cursor.fetchall()
                tables = [result[0] for result in raw_results]

                return tables
        else:
            print("no active database connection")
            return False
        
    def get_table_schema(self, schema, table):
        table_info = {}
        if self.conn:
            if self.cursor:
                self.cursor.execute(f"USE {schema};")
                self.cursor.execute(f"DESCRIBE {table};")
                result = self.cursor.fetchall()

                for row in result:
                    table_info[row[0]] = row[1]
                print(f"table info: {table_info}")
                return table_info
            else:
                return False
        else:
            print("no active database connection")
            return False
        
    def execute_query(self, query):
        if self.conn:
            try:
                self.cursor.execute(query)
                # self.conn.commit()
                result = self.cursor.fetchall()

                return result
            except Exception as e:
                print(f"Error executing query: {e}")
                return False
        else:
            print("no active database connection")
            return False
        
    def insert_data(self, insert_query, values):
        if self.conn:
            try:
                self.cursor.executemany(insert_query, values)
                self.conn.commit()
                print("Data inserted successfully")

                return True
            except Exception as e:
                print(f"Error while inserting data: {e}")
                return False
        else:
            print("no active database connection")
            return False