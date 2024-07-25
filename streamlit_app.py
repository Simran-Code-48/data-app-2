import streamlit as st
import psycopg2

# Define your connection string
conn_string = st.secrets["conn_string"]


# Establish a connection to the PostgreSQL database
def get_connection():
    conn = psycopg2.connect(conn_string)
    return conn


# Fetch data from the database
def fetch_data(conn):
    query = "SELECT * FROM apps order by id;"
    with conn.cursor() as cursor:
        cursor.execute(query)
        rows = cursor.fetchall()
    return rows

# Update the female_centric value in the database
def update_female_centric(conn, id, new_value):
    query = "UPDATE apps SET female_centric = %s WHERE id = %s;"
    with conn.cursor() as cursor:
        cursor.execute(query, (new_value, id))
    conn.commit()

# Initialize connection
conn = get_connection()
data = fetch_data(conn)

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
