import sqlite3

DB_NAME = "todo.db"

def get_db_connection():
    connection = sqlite3.connect(DB_NAME)
    connection.row_factory = sqlite3.Row  
    return connection

def execute_db_query(sql_query, query_params=(), fetch_type=None):
    db_connection = get_db_connection()  
    cursor = db_connection.cursor()  
    
    cursor.execute(sql_query, query_params)  
    db_connection.commit()  
    
    query_result = None  
    if fetch_type == "all":
        query_result = cursor.fetchall()  
    elif fetch_type == "one":
        query_result = cursor.fetchone()  
    
    db_connection.close()  
    return query_result  

def init_db():
    sql_statement = '''CREATE TABLE IF NOT EXISTS tasks (
                    id INTEGER PRIMARY KEY AUTOINCREMENT, 
                    title TEXT NOT NULL CHECK(LENGTH(title) <= 50), 
                    description TEXT CHECK(LENGTH(description) <= 200), 
                    done INTEGER DEFAULT 0)'''
    execute_db_query(sql_statement)

def get_all_tasks():
    sql_query = "SELECT * FROM tasks"
    return execute_db_query(sql_query, fetch_type="all")

def get_task_by_id(task_id):
    sql_query = "SELECT * FROM tasks WHERE id = ?"
    return execute_db_query(sql_query, (task_id,), fetch_type="one")

def add_task(title, description):
    sql_query = "INSERT INTO tasks (title, description) VALUES (?, ?)"
    execute_db_query(sql_query, (title, description))

def toggle_task_status(task_id):
    sql_query = "UPDATE tasks SET done = NOT done WHERE id = ?"
    execute_db_query(sql_query, (task_id,))

def remove_task(task_id):
    sql_query = "DELETE FROM tasks WHERE id = ?"
    execute_db_query(sql_query, (task_id,))