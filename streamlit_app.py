import streamlit as st
import psycopg2

# Define your connection string
conn_string = st.secrets["conn_string"]


# Establish a connection to the PostgreSQL database
def get_connection():
    try:
        conn = psycopg2.connect(conn_string)
        return conn
    except OperationalError as e:
        st.error(f"Could not connect to the database: {e}")
        return None


# Fetch data from the database
def fetch_data(conn):
    query = "SELECT * FROM apps ORDER BY id;"
    try:
        with conn.cursor() as cursor:
            cursor.execute(query)
            rows = cursor.fetchall()
        return rows
    except DatabaseError as e:
        st.error(f"Could not fetch data from the database: {e}")
        return []

# Update the female_centric value in the database
def update_female_centric(conn, id, new_value):
   query = "UPDATE apps SET female_centric = %s WHERE id = %s;"
    try:
        with conn.cursor() as cursor:
            cursor.execute(query, (new_value, id))
        conn.commit()
    except DatabaseError as e:
        st.error(f"Could not update the database: {e}")

# Initialize connection
conn = get_connection()
if conn:
    data = fetch_data(conn)
else:
    data = []

# Initialize session state for row index and female_centric value
if 'row_index' not in st.session_state:
    st.session_state.row_index = 0
if 'female_centric' not in st.session_state:
    st.session_state.female_centric = data[st.session_state.row_index][6]

# Display the current row data
def display_row(row):
    # st.write(f"Id: {row[0]}")
    # st.write(f"Package: {row[1]}")
    st.write(f"App Name: {row[2]}")
    st.write(f"Description: {row[3]}")
    st.write(f"Category: {row[4]}")
    # st.write(f"Package ID: {row[5]}")
    # st.write(f"User Count: {row[6]}")
    st.write(f"Female Centric: {row[7]}")
    st.write("Want to make changes ?")
    st.session_state.female_centric = st.radio(
        "Want to make changes to Female Centric?",
        ["Female centric", "Non-female centric"],
        index=0 if row[7] else 1
    ) == "Female centric"
    st.write(st.session_state.female_centric)


# Check if data is available
if data:
    # Display the current row
    current_row = data[st.session_state.row_index]
    display_row(current_row)

    # Button to save changes
    if st.button('Save Changes'):
        update_female_centric(conn, current_row[0], st.session_state.female_centric)
        st.success("Changes saved successfully!")
        # Refresh data after saving changes
        data = fetch_data(conn)

    # Navigation buttons in the same row
    col1, col2 = st.columns([1, 3])  # Adjust the ratios if needed

    with col1:
        if st.button('Previous'):
            if st.session_state.row_index > 0:
                st.session_state.row_index -= 1

    with col2:
        if st.button('Next'):
            if st.session_state.row_index < len(data) - 1:
                st.session_state.row_index += 1

    # Ensure the female_centric checkbox updates correctly when navigating
    if st.session_state.row_index != current_row[0]:
        st.session_state.female_centric = data[st.session_state.row_index][7]
else:
    st.warning("No data available.")
