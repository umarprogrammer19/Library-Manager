import streamlit as st
import sqlite3
import pandas as pd

def load_css():
    st.markdown(
        """
    <style>
        /* General Styling */
        body {
            font-family: 'Arial', sans-serif;
        }
        .stApp {
            background-color: #f5f7fa;
            color: #333333;
        }
        
        /* Title Styling */
        h1 {
            color: #2c3e50;
            font-weight: bold;
            text-align: center;
            margin-bottom: 20px;
        }
        
        /* Subheader Styling */
        h2 {
            color: #34495e;
            font-size: 1.5em;
        }
        
        /* Buttons */
        .stButton>button {
            background-color: #3498db;
            color: white;
            border-radius: 5px;
            padding: 8px 15px;
            font-weight: bold;
        }
        .stButton>button:hover {
            background-color: #2980b9;
            color: white;
        }
        
        /* Success and Error Messages */
        .stSuccess {
            background-color: #d4edda;
            color: #155724;
            border-radius: 5px;
            padding: 10px;
        }
        .stError {
            background-color: #f8d7da;
            color: #721c24;
            border-radius: 5px;
            padding: 10px;
        }
        
        /* Table Styling */
        .dataframe {
            border-collapse: collapse;
            width: 100%;
        }
        .dataframe th {
            background-color: #34495e;
            color: white;
            padding: 10px;
            text-align: left;
        }
        .dataframe td {
            padding: 10px;
            border-bottom: 1px solid #ddd;
        }
        .dataframe tr:hover {
            background-color: #ecf0f1;
        }
        
        /* Sidebar Styling */
        .css-1d391kg {
            background-color: #2c3e50;
            color: white;
        }
        .css-1d391kg a {
            color: #ecf0f1;
        }
        
        /* Footer */
        .footer {
            text-align: center;
            color: #7f8c8d;
            font-size: 0.9em;
            margin-top: 20px;
        }
    </style>
    """,
        unsafe_allow_html=True,
    )


# Database
def init_db():
    conn = sqlite3.connect("library.db")
    c = conn.cursor()
    c.execute(
        """CREATE TABLE IF NOT EXISTS books
                 (id INTEGER PRIMARY KEY AUTOINCREMENT,
                  title TEXT NOT NULL,
                  author TEXT NOT NULL,
                  isbn TEXT UNIQUE NOT NULL,
                  publication_year INTEGER,
                  genre TEXT)"""
    )
    conn.commit()
    conn.close()


def add_book(title, author, isbn, publication_year, genre):
    conn = sqlite3.connect("library.db")
    c = conn.cursor()
    try:
        c.execute(
            "INSERT INTO books (title, author, isbn, publication_year, genre) VALUES (?, ?, ?, ?, ?)",
            (title, author, isbn, publication_year, genre),
        )
        conn.commit()
        return True
    except sqlite3.IntegrityError:
        return False
    finally:
        conn.close()


def get_all_books():
    conn = sqlite3.connect("library.db")
    df = pd.read_sql_query("SELECT * FROM books", conn)
    conn.close()
    return df


def search_books(query):
    conn = sqlite3.connect("library.db")
    df = pd.read_sql_query(
        "SELECT * FROM books WHERE title LIKE ? OR author LIKE ? OR isbn LIKE ?",
        conn,
        params=("%" + query + "%", "%" + query + "%", "%" + query + "%"),
    )
    conn.close()
    return df


def update_book(id, title, author, isbn, publication_year, genre):
    conn = sqlite3.connect("library.db")
    c = conn.cursor()
    try:
        c.execute(
            "UPDATE books SET title=?, author=?, isbn=?, publication_year=?, genre=? WHERE id=?",
            (title, author, isbn, publication_year, genre, id),
        )
        conn.commit()
        return True
    except sqlite3.IntegrityError:
        return False
    finally:
        conn.close()


def delete_book(id):
    conn = sqlite3.connect("library.db")
    c = conn.cursor()
    c.execute("DELETE FROM books WHERE id=?", (id,))
    conn.commit()
    conn.close()


def main():
    load_css()
    init_db()
    
    st.set_page_config(page_title="Library Manager", layout="wide")

    st.title("Library Manager")

    st.sidebar.title("Navigation")
    page = st.sidebar.radio("Go to", ["View Books", "Add Book", "Search Books"])

    if "edit_id" not in st.session_state:
        st.session_state["edit_id"] = None

    if page == "View Books":
        st.subheader("Book List")
        books_df = get_all_books()
        if not books_df.empty:
            books_df["Actions"] = books_df["id"].apply(
                lambda x: f'<button onclick="st.session_state.edit_id={x};st.rerun()">Edit</button> '
                f'<button onclick="delete_book({x});st.rerun()">Delete</button>'
            )
            st.dataframe(books_df.drop(columns=["Actions"]), use_container_width=True)
            if st.session_state["edit_id"]:
                edit_book(st.session_state["edit_id"])
        else:
            st.write("No books found.")

    elif page == "Add Book":
        st.subheader("Add New Book")
        with st.form(key="add_book_form"):
            title = st.text_input("Title")
            author = st.text_input("Author")
            isbn = st.text_input("ISBN")
            year = st.number_input(
                "Publication Year", min_value=1000, max_value=9999, step=1
            )
            genre = st.text_input("Genre")
            col1, col2 = st.columns(2)
            with col1:
                submit = st.form_submit_button(label="Add Book")
            with col2:
                cancel = st.form_submit_button(label="Cancel")
            if submit:
                if title and author and isbn:
                    if add_book(title, author, isbn, year, genre):
                        st.success("Book added successfully")
                    else:
                        st.error("Error: ISBN already exists")
                else:
                    st.error("Please fill in all required fields")
            if cancel:
                st.rerun()

    elif page == "Search Books":
        st.subheader("Search Books")
        search_query = st.text_input("Search by title, author, or ISBN")
        if search_query:
            books_df = search_books(search_query)
            if not books_df.empty:
                st.dataframe(books_df, use_container_width=True)
            else:
                st.write("No books found.")

    # Footer
    st.markdown(
        '<div class="footer">Developed by [Your Name] | Version 1.0</div>',
        unsafe_allow_html=True,
    )


def edit_book(book_id):
    st.subheader("Edit Book")
    conn = sqlite3.connect("library.db")
    book = pd.read_sql_query(
        "SELECT * FROM books WHERE id=?", conn, params=(book_id,)
    ).iloc[0]
    conn.close()

    with st.form(key="edit_book_form"):
        title = st.text_input("Title", value=book["title"])
        author = st.text_input("Author", value=book["author"])
        isbn = st.text_input("ISBN", value=book["isbn"])
        year = st.number_input(
            "Publication Year",
            min_value=1000,
            max_value=9999,
            value=int(book["publication_year"]),
            step=1,
        )
        genre = st.text_input("Genre", value=book["genre"])
        col1, col2 = st.columns(2)
        with col1:
            update = st.form_submit_button(label="Update Book")
        with col2:
            cancel = st.form_submit_button(label="Cancel")
        if update:
            if title and author and isbn:
                if update_book(book_id, title, author, isbn, year, genre):
                    st.success("Book updated successfully")
                    st.session_state["edit_id"] = None
                    st.rerun()
                else:
                    st.error("Error: ISBN already exists")
            else:
                st.error("Please fill in all required fields")
        if cancel:
            st.session_state["edit_id"] = None
            st.rerun()


if __name__ == "__main__":
    main()
