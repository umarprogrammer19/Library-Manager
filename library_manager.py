import streamlit as st
import sqlite3
import pandas as pd

# Database Initialization
def init_db():
    conn = sqlite3.connect('library.db')
    c = conn.cursor()
    c.execute('''CREATE TABLE IF NOT EXISTS books
                 (id INTEGER PRIMARY KEY AUTOINCREMENT,
                  title TEXT NOT NULL,
                  author TEXT NOT NULL,
                  isbn TEXT UNIQUE NOT NULL,
                  publication_year INTEGER,
                  genre TEXT)''')
    conn.commit()
    conn.close()

# CRUD Functions
def add_book(title, author, isbn, publication_year, genre):
    conn = sqlite3.connect('library.db')
    c = conn.cursor()
    try:
        c.execute("INSERT INTO books (title, author, isbn, publication_year, genre) VALUES (?, ?, ?, ?, ?)",
                  (title, author, isbn, publication_year, genre))
        conn.commit()
        return True
    except sqlite3.IntegrityError:
        return False
    finally:
        conn.close()

def get_all_books():
    conn = sqlite3.connect('library.db')
    c = conn.cursor()
    c.execute("SELECT * FROM books")
    books = c.fetchall()
    conn.close()
    return books

def search_books(query):
    conn = sqlite3.connect('library.db')
    c = conn.cursor()
    c.execute("SELECT * FROM books WHERE title LIKE ? OR author LIKE ? OR isbn LIKE ?",
              ('%'+query+'%', '%'+query+'%', '%'+query+'%'))
    books = c.fetchall()
    conn.close()
    return books

def update_book(id, title, author, isbn, publication_year, genre):
    conn = sqlite3.connect('library.db')
    c = conn.cursor()
    try:
        c.execute("UPDATE books SET title=?, author=?, isbn=?, publication_year=?, genre=? WHERE id=?",
                  (title, author, isbn, publication_year, genre, id))
        conn.commit()
        return True
    except sqlite3.IntegrityError:
        return False
    finally:
        conn.close()

def delete_book(id):
    conn = sqlite3.connect('library.db')
    c = conn.cursor()
    c.execute("DELETE FROM books WHERE id=?", (id,))
    conn.commit()
    conn.close()

# Streamlit Interface
def main():
    # Initialize database
    init_db()

    # Set page title
    st.title("Library Manager")

    # Initialize session state
    if 'action' not in st.session_state:
        st.session_state['action'] = 'view'

    # Search bar
    search_query = st.text_input("Search books by title, author, or ISBN")

    # Add new book button
    if st.button("Add New Book"):
        st.session_state['action'] = 'add'

    # Book form expander
    with st.expander("Book Form", expanded=(st.session_state['action'] in ['add', 'edit'])):
        if st.session_state['action'] == 'add':
            st.subheader("Add New Book")
            title = st.text_input("Title")
            author = st.text_input("Author")
            isbn = st.text_input("ISBN")
            year = st.number_input("Publication Year", min_value=1000, max_value=9999, step=1)
            genre = st.text_input("Genre")

            col1, col2 = st.columns(2)
            with col1:
                if st.button("Submit"):
                    if title and author and isbn:  # Basic validation
                        if add_book(title, author, isbn, year, genre):
                            st.success("Book added successfully")
                            st.session_state['action'] = 'view'
                            st.experimental_rerun()
                        else:
                            st.error("Error: ISBN already exists")
                    else:
                        st.error("Please fill in all required fields")
            with col2:
                if st.button("Cancel"):
                    st.session_state['action'] = 'view'
                    st.experimental_rerun()

        elif st.session_state['action'] == 'edit':
            st.subheader("Edit Book")
            book_id = st.session_state['edit_id']
            conn = sqlite3.connect('library.db')
            c = conn.cursor()
            c.execute("SELECT * FROM books WHERE id=?", (book_id,))
            book = c.fetchone()
            conn.close()

            if book:
                title = st.text_input("Title", value=book[1])
                author = st.text_input("Author", value=book[2])
                isbn = st.text_input("ISBN", value=book[3])
                year = st.number_input("Publication Year", min_value=1000, max_value=9999, value=book[4], step=1)
                genre = st.text_input("Genre", value=book[5])

                col1, col2 = st.columns(2)
                with col1:
                    if st.button("Update"):
                        if title and author and isbn:
                            if update_book(book_id, title, author, isbn, year, genre):
                                st.success("Book updated successfully")
                                st.session_state['action'] = 'view'
                                st.experimental_rerun()
                            else:
                                st.error("Error: ISBN already exists")
                        else:
                            st.error("Please fill in all required fields")
                with col2:
                    if st.button("Cancel"):
                        st.session_state['action'] = 'view'
                        st.experimental_rerun()
            else:
                st.error("Book not found")
                st.session_state['action'] = 'view'

    # Display books
    st.subheader("Book List")
    books = search_books(search_query) if search_query else get_all_books()

    if books:
        # Table headers
        col1, col2, col3, col4, col5, col6, col7 = st.columns([1, 3, 3, 2, 2, 2, 2])
        col1.write("**ID**")
        col2.write("**Title**")
        col3.write("**Author**")
        col4.write("**ISBN**")
        col5.write("**Year**")
        col6.write("**Genre**")
        col7.write("**Actions**")

        # Book rows
        for book in books:
            with st.container():
                col1, col2, col3, col4, col5, col6, col7 = st.columns([1, 3, 3, 2, 2, 2, 2])
                col1.write(book[0])
                col2.write(book[1])
                col3.write(book[2])
                col4.write(book[3])
                col5.write(book[4])
                col6.write(book[5])
                with col7:
                    if st.button("Edit", key=f"edit_{book[0]}"):
                        st.session_state['action'] = 'edit'
                        st.session_state['edit_id'] = book[0]
                        st.experimental_rerun()
                    if st.button("Delete", key=f"delete_{book[0]}"):
                        delete_book(book[0])
                        st.experimental_rerun()  # Refresh the list
    else:
        st.write("No books found.")

if __name__ == "__main__":
    main()