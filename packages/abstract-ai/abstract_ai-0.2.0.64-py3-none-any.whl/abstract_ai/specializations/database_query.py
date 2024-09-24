from abstract_security import *
from abstract_database import *
from .responseContentParser import *
import psycopg2
# Predefined table configurations
def connect_db():
    """Establish a connection to the database."""
    try:
        return psycopg2.connect(
            dbname=get_env_value(key="abstract_ai_dbname"),
            user=get_env_value(key="abstract_ai_user"),
            password=get_env_value(key="abstract_ai_password"),
            host=get_env_value(key="abstract_ai_host"),
            port=int(get_env_value(key="abstract_ai_port"))
        )
    except psycopg2.OperationalError as e:
        print("Unable to connect to the database:", e)
        sys.exit(1)
def get_table_configuration(file_path=None):
    table_configuration = []    
    table_configuration_file_path = file_path or get_env_value(key="abstract_ai_table_configuration_file_path")
    try:
        table_configuration = safe_read_from_json(table_configuration_file_path)
    except:
        print('no table config file path')
    return table_configuration
def get_dict_from_config(tableName,file_path=None):
    """Retrieve value from table configuration."""
    for config in get_table_configuration(file_path=file_path):
        if config.get('tableName').lower() == tableName.lower():
            return config
def get_table_names(file_path=None):
    return [config.get('tableName') for config in get_table_configuration(file_path=file_path)]
def get_first_row_as_dict(tableName=None):
    """Fetch the first row of data from the specified table and return as a dictionary."""
    tableName = tableName or get_env_value(key="abstract_ai_table_name")
    query = f"SELECT * FROM {tableName} ORDER BY id ASC LIMIT 1;"
    
    conn = connect_db()  # Assume connect_db() is your DB connection function
    cur = conn.cursor()
    try:
        cur.execute(query)
        first_row = cur.fetchone()  # Fetch the first row
        
        # Get column names from the cursor description
        col_names = [desc[0] for desc in cur.description]
        
        # Combine column names and row data into a dictionary
        if first_row:
            row_as_dict = dict(zip(col_names, first_row))
            return row_as_dict
        else:
            return None  # Return None if no rows are found

    except psycopg2.Error as e:
        print(f"Error fetching the first row: {e}")
        return None
    finally:
        cur.close()
        conn.close()

def get_instruction_from_tableName(tableName=None):
    tableName = tableName or get_env_value(key="abstract_ai_table_name")
    table_samples = []
    table_configuration_file_path = get_env_value(key="abstract_ai_table_configuration_file_path")
    try:
        table_configuration = safe_read_from_json(table_configuration_file_path)
        table_samples.append({"DATABASE_CONFIG":get_dict_from_config(tableName),"explination":"Database Table Configuration."})
    except:
        pass
    data = get_first_row_as_dict(tableName)
    table_samples.append({"ACTUAL_DATABASE_ROW":data,"explination":f"first row of data from table {tableName} returned as a dictionary."})
    value_keys = {}
    for column,values in data.items():
        value_keys[column]= get_value_keys(values)
    table_samples.append({"VALUE_KEYS":value_keys,"explination":"Type Values for the Values in the Database SCHEMA."})
    table_samples.append({"AVAILABLE_FUNCTION_FOR_FILTERING":f"""def search_multiple_fields(query):
    conn = connect_db()
    cur = conn.cursor()
    try:
        cur.execute(query)
        results = cur.fetchall()
        return results
    except psycopg2.Error as e:
        print(f"Error querying JSONB data: e")
    finally:
        cur.close()
        conn.close()
""","explination":"this is the available function for filtering the database"})
    return table_samples
def search_multiple_fields(query):
    conn = connect_db()
    cur = conn.cursor()
    try:
        cur.execute(query)
        results = cur.fetchall()
        return results
    except psycopg2.Error as e:
        print(f"Error querying JSONB data: {e}")
    finally:
        cur.close()
        conn.close()

def save_to_excel(rows, file_path="output.xlsx"):
    excel = []
    if rows:
        for i,row in enumerate(rows):
            if not isinstance(row,list):
                row = list(row)
            if isinstance(row,tuple):
                row = list(row)
    
            excel.append(flatten_json(row, parent_key='', sep='_'))
        safe_excel_save(pd.DataFrame(excel),file_path)
def get_query_save_to_excel(database_query,file_path ="output.xlsx"):
    result = search_multiple_fields(**database_query)
    save_to_excel(rows=result,file_path=file_path)
    return file_path
def generate_query_from_recent_response(file_path):
    response_content = get_response_content(file_path)
    database_query = response_content.get('database_query')
    if database_query:
        title = response_content.get('generate_title')
        dirName = os.path.dirname(file_path)
        parent_dir = os.path.dirname(dirName)
        new_directory = os.path.join(parent_dir,'queries')
        os.makedirs(new_directory,exist_ok=True)
        new_file_name = f"{title}.xlsx"
        new_file_path = os.path.join(new_directory,new_file_name)
        get_query_save_to_excel(database_query,file_path=new_file_path)
        return file_path
