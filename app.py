import streamlit as st
import streamlit.components.v1 as components
import pandas as pd
from models.db_connection import DBconnection
from models.sql_model import SQLModel

# -- app state configuration

if "DB_connection" not in st.session_state:
    st.session_state.DB_connection = None
if "llm_connection" not in st.session_state:
    st.session_state.llm_connection = None
if "messages" not in st.session_state:
    st.session_state.messages = []
if "schemas" not in st.session_state:
    st.session_state.schemas = None
if "selected_schema" not in st.session_state:
    st.session_state.selected_schema = None
if "tables" not in st.session_state:
    st.session_state.tables = None
if "selected_table" not in st.session_state:
    st.session_state.selected_table = None
if "table_info" not in st.session_state:
    st.session_state.table_info = None
if "new_table" not in st.session_state:
    st.session_state.new_table = [
        {"column_name": "dummy", "data_type": "dummy"},
    ]
if "data_upload_table" not in st.session_state:
    st.session_state.data_upload_table = None

# -- sidebar content

st.set_page_config(
    page_title="SQLbot",
    page_icon=":robot:",
    layout="centered",
    )

def ge_DB_llm_object():
    conn = DBconnection()
    llmConnect = SQLModel()

    return conn, llmConnect

with st.sidebar:
    st.logo("images/sql.png", size="large")

    # -- initialize credentials 

    with st.popover('Initialize credentials'):
        API_KEY = st.text_input("Enter Gemini API key: ", key="api_key", placeholder="API KEY")
        DB_password = st.text_input("Enter Database password: ", type="password", key="db_pasword", placeholder="DB Password")
        DB_host = st.text_input("Enter Database host: ", key="db_host", placeholder="DB host")
        DB_user = st.text_input("Enter Database user: ", key="db_user", placeholder="DB user")

        if st.button("Initialize credentials"):
            conn, llmConnect = ge_DB_llm_object()

            if DB_password and DB_host and DB_user and API_KEY:
                if conn.initialize_credentials(DB_password, DB_host, DB_user):
                    if  llmConnect.initialize_llm(API_KEY):
                        st.session_state.DB_connection = conn
                        st.session_state.llm_connection = llmConnect
                        st.success("llm and DB connected")
                        st.session_state.messages.append({"role": "assistant", "content": "Successfully connected to DB and LLM. You can start the requests now."})
                    else:
                        st.session_state.llm_connection = None
                        st.error("Error connecting llm")
                else:
                    st.session_state.DB_connection = None
                    st.error("Error in connecting to DB")
            else:
                st.error("Please provide required credentials.")
    
    if st.session_state.DB_connection:
        if st.button("Disconnect"):
            if st.session_state.DB_connection.disconnect() and st.session_state.llm_connection.disconnect():
                st.session_state.DB_connection = None
                st.session_state.llm_connection = None
                st.session_state.messages.append({"role": "assistant", "content": "Successfully disconnected."})
                st.success("disconnected")
            else:
                st.error("error disconnecting")


    # -- get Schemas and tables

    if st.session_state.DB_connection:
        st.markdown("---")
        st.session_state.schemas = st.session_state.DB_connection.get_schemas()
        if st.session_state.schemas:
            st.session_state.selected_schema = st.selectbox("Select schema", st.session_state.schemas, index=None, placeholder="Select schema")
        else:
            st.session_state.selected_schema = None
            st.error("No schemas found or error connecting to DB")

        if st.session_state.selected_schema:
            st.session_state.tables = st.session_state.DB_connection.get_tables(st.session_state.selected_schema)
            if st.session_state.tables:
                st.session_state.selected_table = st.selectbox("Select table", st.session_state.tables, index=None, placeholder="Select table")
                if st.session_state.selected_table:
                    st.session_state.table_info = st.session_state.DB_connection.get_table_schema(st.session_state.selected_schema, st.session_state.selected_table)
            else:
                st.session_state.selected_table = None
                st.error("No tables found or error connecting to DB")

                # -- create new table

                with st.popover("create table"):
                    def new_table_schema():
                        st.session_state.new_table.append(
                            {
                                "column_name": st.session_state.new_column_name,
                                "data_type": st.session_state.new_data_type,
                            }
                        )

                    with st.expander("Instructions: "):
                        st.markdown("""
                                    1. Make sure to enter column name properly which does not contain any special characters except underscore(_).
                                    2. Enter the data type of columns as per SQL standards. (VARCHAR, INT, TEXT, etc.)
                                    3. Provide the size of the data type if requireed. (VARCHAR (255), INT (110, etc.))
                                    """)
                    st.subheader("New table")

                    NewTable = pd.DataFrame(st.session_state.new_table)
                    # score_df["total_points"] = score_df["Pushups"] + score_df["Situps"]

                    st.write(NewTable)

                    st.subheader("Add a new column")
                    with st.form("new_table_schema", clear_on_submit=True):
                        column_name = st.text_input("Column Name", key="new_column_name")
                        data_type = st.text_input("data type", key="new_data_type")
                        # situps = st.number_input("Situps", key="situps", step=1, value=0, min_value=0)
                        st.form_submit_button("Add", on_click=new_table_schema)

                    columns = NewTable["column_name"].tolist()
                    data_types = NewTable["data_type"].tolist()

                    table_name = st.text_input("Table name", placeholder="Enter table name")
                    # st.button("Create table", on_click=st.session_state.DB_connection.create_table(columns, data_types, st.session_state.selected_schema, table_name))
                    if st.button("Create table"):
                        if st.session_state.DB_connection.create_table(columns, data_types, st.session_state.selected_schema, table_name):
                            st.success(f"Table `{table_name}` created in `{st.session_state.selected_schema}`")
                        else:
                            st.error("Error creating table. Please check DB connection.")

        if st.button("🔃Refresh"):
            conn, llmConnect = ge_DB_llm_object()

            if conn.initialize_credentials(DB_password, DB_host, DB_user):
                if  llmConnect.initialize_llm(API_KEY):
                    st.session_state.DB_connection = conn
                    st.session_state.llm_connection = llmConnect
                    st.success("Database refreshed.")
                    st.session_state.messages.append({"role": "assistant", "content": "Databse refreshed. Please select the schema and table to continue."})
                else:
                    st.session_state.llm_connection = None
                    st.error("Error connecting llm")
            else:
                st.session_state.DB_connection = None
                st.error("Error in connecting to DB")


    if st.session_state.DB_connection:
        st.markdown("---")

        # -- create new schema
        new_schema = st.text_input("Create schema:", placeholder="Enter schema name")
        if st.button("Create schema"):
            if st.session_state.DB_connection.create_schema(new_schema):
                st.success(f"Schema `{new_schema}` created successfully")
            else:
                st.error("Error creating schema. Please check database connection is established.")

        # -- create new table

        with st.popover("create table"):
            def new_table_sidebar():
                st.session_state.new_table.append(
                    {
                        "column_name": st.session_state.sidebar_column_name,
                        "data_type": st.session_state.sidebar_data_type,
                    }
                )

            with st.expander("Instructions: "):
                st.markdown("""
                            1. Make sure to enter column name properly which does not contain any special characters except underscore(_).
                            2. Enter the data type of columns as per SQL standards. (VARCHAR, INT, TEXT, etc.)
                            3. Provide the size of the data type if requireed. (VARCHAR (255), INT (110, etc.))
                            """)
            st.subheader("New table")

            NewTable = pd.DataFrame(st.session_state.new_table)
            # score_df["total_points"] = score_df["Pushups"] + score_df["Situps"]

            st.write(NewTable)

            st.subheader("Add a new column")
            with st.form("new_table_sidebar", clear_on_submit=True):
                column_name = st.text_input("Column Name", key="sidebar_column_name")
                data_type = st.text_input("data type", key="sidebar_data_type")
                st.form_submit_button("Add", on_click=new_table_sidebar)

            columns = NewTable["column_name"].tolist()
            data_types = NewTable["data_type"].tolist()

            table_name = st.text_input("Table name", placeholder="Enter table name", key="sidebar_table_name")
            # st.button("Create table", on_click=st.session_state.DB_connection.create_table(columns, data_types, st.session_state.selected_schema, table_name))
            if st.button("Create table", key="sidebar_create_table"):
                if st.session_state.DB_connection.create_table(columns, data_types, st.session_state.selected_schema, table_name):
                    st.success(f"Table `{table_name}` created in `{st.session_state.selected_schema}`")
                else:
                    st.error("Error creating table. Please check DB connection.")

        # -- data upload to table
        st.markdown("---")

        st.subheader("Upload data to table")
        with st.popover("upload data"):
            data_file = st.file_uploader("Uoload CSV file", type=["csv"], key="data_file_uploader", label_visibility="collapsed")
            if data_file is not None:
                df=pd.read_csv(data_file)
                st.dataframe(df.head())

                # st.info("""""")
                with st.expander("Instructions: ", expanded=True):
                    st.markdown("""
                                1. Make sure the data types and the number of columns in the CSV file match with the columns in the table.
                                2. Make sure the squence of columns in CSV file is same as the columns in table.
                                3. Keep the column names in the first row of CSV file as per standard CSV format.""")
                
                selected_schema = st.selectbox("select schema", st.session_state.schemas, index=None, placeholder="Select schema", label_visibility="collapsed")
                st.session_state.data_upload_table = st.session_state.DB_connection.get_tables(selected_schema)
                selected_table = st.selectbox("select table", st.session_state.data_upload_table, index=None, placeholder="Select table", label_visibility="collapsed")

                if st.button("Upload to table"):
                    csv_columns = ", ".join(df.columns)
                    placeholder = ", ".join(["%s"]* len(df.columns))
                    values = df.values.tolist()
                    insert_query = f"INSERT INTO {selected_schema}.{selected_table} ({csv_columns}) VALUES ({placeholder})"
                    
                    if st.session_state.DB_connection.insert_data(insert_query, values):
                        st.success(f"Data uploaded to `{selected_table}` in `{selected_schema}`.")
                    else:
                        st.error("Error uploading data.")
                    



# -- main content
st.markdown("<h1 style='text-align: center;'>SQLbot</h1>", unsafe_allow_html=True)
with st.expander("Instructions: "):
    st.markdown("""
                1. First, initialize the credentials by providing Gemini API key and Database credentials.
                2. Select the schema and table from the sidebar to start the conversation.
                3. You can create a new schema from sidebar.
                4. If table is not present in the selected schema, you can create a new table by providing the column names and respective data types.
                5. Make sure to refresh the database after creating a new schema or table to see the changes.""")

for message in st.session_state.messages:
    if message["role"] == "user":
        with st.chat_message(message["role"]):
            st.markdown(message["content"])
    else:
        with st.chat_message(message["role"]):
            # Check if content is a dictionary (for SQL queries with data) or string (for simple messages)
            if isinstance(message["content"], dict):
                if len(message["content"]["data"]) > 0:
                    st.code(message["content"]["sql"], language="sql")
                    df = pd.DataFrame(data=message["content"]["data"], columns=message["content"]["columns"])
                    st.dataframe(df)
                else:
                    st.code(message["content"]["sql"], language="sql")
                    st.info("No data found for the query.")
            else:
                st.markdown(message["content"])

components.html(
"""
<script>
    var elem = window.parent.document.querySelector('section.main');
    elem.scrollTo({ top: elem.scrollHeight, behavior: 'smooth' });
</script>
""",
height=0,
)

user_input = st.chat_input(placeholder="Enter your query here...")

if user_input: 
    if st.session_state.DB_connection and st.session_state.llm_connection:
        # Add user message to session state first
        st.session_state.messages.append({"role": "user", "content": user_input})
        
        # Generate response
        with st.spinner("Thinking..."):
            response = st.session_state.llm_connection.get_response(
                user_input,
                st.session_state.selected_schema,
                st.session_state.selected_table,
                st.session_state.table_info
            )
            result = st.session_state.DB_connection.execute_query(response)
            print("result: ", result)
                

        # Add assistant response to session state
        if response:
            if isinstance(result, dict) and len(result["data"]) > 0:
                st.session_state.messages.append({"role": "assistant", "content": {"sql": response, "data": result["data"], "columns": result["column_names"]}})
            else:
                st.session_state.messages.append({"role": "assistant", "content": {"sql": response, "data": [], "columns": []}})
        else:
            st.session_state.messages.append({"role": "assistant", "content": "Error generating response or executing query. Please check the input and try again."})
        
        # Rerun to display the updated messages
        st.rerun()

        # print(f"\n\nmessages: {st.session_state.messages}\n\n")


    else:
        st.error("Please first initialize the credentials.")
        # Add error message to session state
        st.session_state.messages.append({"role": "assistant", "content": "Please first initialize the credentials."})
        st.rerun()

####################################################################################


