import streamlit as st
import psycopg2

# Define your connection string
conn_string = st.secrets["conn_string"]

# Establish a connection to the PostgreSQL database
def get_connection():
    conn = psycopg2.connect(conn_string)
    return conn

# Use the connection in your Streamlit app
conn = get_connection()

# Function to get all databases
def get_databases(conn):
    query = "SELECT datname FROM pg_database WHERE datistemplate = false;"
    with conn.cursor() as cursor:
        cursor.execute(query)
        databases = cursor.fetchall()
    return [db[0] for db in databases]

# Function to get all tables in the current database
def get_tables(conn):
    query = """
    SELECT table_name 
    FROM information_schema.tables 
    WHERE table_schema = 'public'
    """
    with conn.cursor() as cursor:
        cursor.execute(query)
        tables = cursor.fetchall()
    return [table[0] for table in tables]

# Get databases and tables
databases = get_databases(conn)
tables = get_tables(conn)

# Display databases and tables in Streamlit
st.write("**Databases:**")
st.write(databases)

st.write("**Tables in the current database:**")
st.write(tables)
