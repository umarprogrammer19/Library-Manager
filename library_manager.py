import streamlit as st
import sqlite3
import pandas as pd

st.set_page_config(page_title="Library Manager", layout="centered")

def load_css():
    st.markdown("""
    <style>
        .stButton>button {
            background-color: var(--primary-color);
            color: var(--text-color);
            border-radius: 5px;
            padding: 8px 15px;
            font-weight: bold;
        }
        .stButton>button:hover {
            opacity: 0.9;
        }
        
        .dataframe th {
            background-color: var(--primary-color);
            color: var(--text-color);
            padding: 10px;
            text-align: left;
        }
        .dataframe td {
            padding: 10px;
            border-bottom: 1px solid var(--secondary-background-color);
        }
        .dataframe tr:hover {
            background-color: var(--secondary-background-color);
        }
        
        .footer {
            text-align: center;
            color: var(--text-color);
            font-size: 0.9em;
            margin-top: 20px;
        }
        
        hr {
            margin: 20px 0;
        }
        .description {
            color: var(--text-color);
            font-size: 1.1em;
            margin-bottom: 10px;
        }
    </style>
    """, unsafe_allow_html=True)

# Database
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
    df = pd.read_sql_query("SELECT * FROM books", conn)
    conn.close()
    return df

def search_books(query):
    conn = sqlite3.connect('library.db')
    df = pd.read_sql_query("SELECT * FROM books WHERE title LIKE ? OR author LIKE ? OR isbn LIKE ?",
                           conn, params=('%'+query+'%', '%'+query+'%', '%'+query+'%'))
    conn.close()
    return df

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

def main():
    load_css()
    init_db()

    st.title("Library Manager")

    tab1, tab2, tab3 = st.tabs(["View Books", "Add Book", "Search Books"])

    if 'edit_id' not in st.session_state:
        st.session_state['edit_id'] = None

    with tab1:
        st.markdown('<p class="description">Below is the list of books in your library. Use the buttons to edit or delete books.</p>', unsafe_allow_html=True)
        books_df = get_all_books()
        if not books_df.empty:
            for index, row in books_df.iterrows():
                with st.container():
                    col1, col2, col3 = st.columns([3, 1, 1])
                    with col1:
                        st.write(f"{row['title']} by {row['author']} (ISBN: {row['isbn']}) - {row['publication_year']} - {row['genre']}")
                    with col2:
                        if st.button("Edit", key=f"edit_{row['id']}"):
                            st.session_state['edit_id'] = row['id']
                            st.rerun()
                    with col3:
                        if st.button("Delete", key=f"delete_{row['id']}"):
                            delete_book(row['id'])
                            st.rerun()
            if st.session_state['edit_id']:
                st.markdown("<hr>", unsafe_allow_html=True)
                edit_book(st.session_state['edit_id'])
        else:
            st.write("No books in the library.")

    with tab2:
        st.markdown('<p class="description">Fill in the details to add a new book to your library.</p>', unsafe_allow_html=True)
        with st.form(key='add_book_form'):
            title = st.text_input("Title")
            author = st.text_input("Author")
            isbn = st.text_input("ISBN")
            year = st.number_input("Publication Year", min_value=1000, max_value=9999, step=1)
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

    with tab3:
        st.markdown('<p class="description">Enter a search term to find books by title, author, or ISBN.</p>', unsafe_allow_html=True)
        search_query = st.text_input("Search by title, author, or ISBN")
        if search_query:
            books_df = search_books(search_query)
            if not books_df.empty:
                st.dataframe(books_df, use_container_width=True)
            else:
                st.write("No books match your search.")

    st.markdown('<div class="footer">Developed by Umar Farooq | Version 1.0</div>', unsafe_allow_html=True)

def edit_book(book_id):
    conn = sqlite3.connect('library.db')
    book = pd.read_sql_query("SELECT * FROM books WHERE id=?", conn, params=(book_id,)).iloc[0]
    conn.close()

    st.write(f"Editing Book: {book['title']}")
    with st.form(key='edit_book_form'):
        title = st.text_input("Title", value=book['title'])
        author = st.text_input("Author", value=book['author'])
        isbn = st.text_input("ISBN", value=book['isbn'])
        year = st.number_input("Publication Year", min_value=1000, max_value=9999, value=int(book['publication_year']), step=1)
        genre = st.text_input("Genre", value=book['genre'])
        col1, col2 = st.columns(2)
        with col1:
            update = st.form_submit_button(label="Update Book")
        with col2:
            cancel = st.form_submit_button(label="Cancel")
        if update:
            if title and author and isbn:
                if update_book(book_id, title, author, isbn, year, genre):
                    st.success("Book updated successfully")
                    st.session_state['edit_id'] = None
                    st.rerun()
                else:
                    st.error("Error: ISBN already exists")
            else:
                st.error("Please fill in all required fields")
        if cancel:
            st.session_state['edit_id'] = None
            st.rerun()

if __name__ == "__main__":
    main()