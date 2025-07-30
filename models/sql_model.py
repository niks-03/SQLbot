from langchain_google_genai import GoogleGenerativeAI
from .db_connection import DBconnection
from langchain.prompts import PromptTemplate

class SQLModel:
    def __init__(self):
        self.gemini_model = None
        self.api_key = None
        self.llm = None

    def initialize_llm(self, api_key: str):
        self.gemini_model = "gemini-2.5-flash-lite"
        self.api_key = api_key

        return self.get_llm()

    def get_llm(self):
        try:
            self.llm = GoogleGenerativeAI(
                model = self.gemini_model,
                api_key = self.api_key
            )

            if self.llm:
                print("llm model initialized")
                return True
            else:
                print("Error initializing llm model")
                return False
        except Exception as e:
            print(f"Error initializing model: {e}")
            return False
        
    def get_response(self, query, schema, table, table_info):
        base_template = """You are a helpful AI assistant. Your job is to write the SQL queries. 
                    User will provide the question or statement related to database table in plain English and your job is to understand the user question and create proper "SQL" queries. 
                    The schema and Table names are provided below.
                    "schema-name" : {schema}
                    "table-name" : {table}
                    You should always use the `schema-name.table-name` to reference the correct schema and table in the query.

                    Following is the information about the table columns and their data types.

                    {table_info}

                    Instructions :
                    1. Make sure to keep in mind the column names and it's data type as per above given information.
                    2. Focus on what user want in it's question and try to implement the correct query.

                    Important:
                    ALAWAYS RETURN ONLY `SQL` STATEMENT IN SINGLE BLOCK FORMAT: ```SQL_STATEMENT```

                    Question: {query}
                    """
        # conn = DBconnection()
        # table_info = conn.get_table_schema(schema, table)
        if not table_info:
            print("Error fetching table schema")
            return "Error fetching table schema"
        
        template = PromptTemplate(template=base_template, partial_variables={"schema":schema, "table": table, "table_info":table_info})
        # print("template:", template, "\n")
        chain = template | self.llm
        try:
            response = chain.invoke({"query": query})
            print("response: ", response, "\n\n")
            sql_query = response.split("```sql")[1].replace("```", "").strip()
            print(f"SQL: {sql_query}\n\n")
            return sql_query
        except Exception as e:
            return f"Error generating response: {e}"

        
    def disconnect(self):
        if self.llm:
            self.llm = None
            print("\nllm disconnected\n")
            return True