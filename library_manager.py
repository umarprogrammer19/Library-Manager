import streamlit as st
import json
import os
import pandas as pd

def load_library(filename):
    """Load the library from a file if it exists; otherwise, return an empty list."""
    try:
        if os.path.exists(filename):
            with open(filename, "r") as file:
                return json.load(file)
        return []
    except json.JSONDecodeError:
        st.error("⚠️ Error loading library file. Starting with an empty library.")
        return []


def save_library(library, filename):
    """Save the library to a file."""
    try:
        with open(filename, "w") as file:
            json.dump(library, file)
    except Exception as e:
        st.error(f"⚠️ Error saving library: {e}")


def style_read_status(df):
    """Style the read status with colored text and emojis."""

    def read_status(row):
        if row["read"]:
            return '<span style="color:green">✔ Read</span>'
        else:
            return '<span style="color:red">❌ Unread</span>'

    df["Read Status"] = df.apply(read_status, axis=1)
    return df.drop(columns=["read"]) 


def main():
    filename = "library.json"

    if "library" not in st.session_state:
        st.session_state["library"] = load_library(filename)

    st.set_page_config(page_title="Personal Library Manager", layout="centered")
    st.title("📖 Personal Library Manager")

    tab1, tab2, tab3, tab4, tab5 = st.tabs(
        ["Add Book", "Remove Book", "Search Books", "View All Books", "Statistics"]
    )

    with tab1:
        st.header("📖 Add a Book")
        with st.form(key="add_book_form"):
            title = st.text_input("Title", placeholder="Enter book title")
            author = st.text_input("Author", placeholder="Enter author name")
            year = st.number_input(
                "Publication Year", min_value=1000, max_value=9999, step=1
            )
            genre = st.text_input("Genre", placeholder="Enter genre")
            read = st.radio("Have you read this book?", ("Yes", "No")) == "Yes"
            submit = st.form_submit_button("Add Book")
            if submit:
                if title and author and genre:
                    book = {
                        "title": title,
                        "author": author,
                        "year": int(year),
                        "genre": genre,
                        "read": read,
                    }
                    st.session_state["library"].append(book)
                    save_library(st.session_state["library"], filename)
                    st.success("✅ Book added successfully!")
                else:
                    st.error("⚠️ Please fill in all fields.")

    with tab2:
        st.header("🗑 Remove a Book")
        title_to_remove = st.text_input("Enter the title of the book to remove")
        if st.button("Remove Book"):
            library = st.session_state["library"]
            for book in library[
                :
            ]:  
                if book["title"].lower() == title_to_remove.lower():
                    library.remove(book)
                    save_library(library, filename)
                    st.success("✅ Book removed successfully!")
                    break
            else:
                st.error("⚠️ Book not found.")

    with tab3:
        st.header("🔍 Search for a Book")
        search_by = st.radio("Search by", ("Title", "Author"))
        search_term = st.text_input("Enter search term")
        if st.button("Search"):
            library = st.session_state["library"]
            if search_by == "Title":
                matches = [
                    book
                    for book in library
                    if search_term.lower() in book["title"].lower()
                ]
            else:
                matches = [
                    book
                    for book in library
                    if search_term.lower() in book["author"].lower()
                ]
            if matches:
                df = pd.DataFrame(matches)
                df = style_read_status(df)
                table_style = """
                <style>
                table {
                    width: 100%;
                    border-collapse: collapse;
                }
                th, td {
                    padding: 8px;
                    text-align: left;
                    border-bottom: 1px solid #ddd;
                }
                tr:hover {
                    background-color: #f5f5f5;
                }
                </style>
                """
                st.write(
                    table_style + df.to_html(escape=False, index=False),
                    unsafe_allow_html=True,
                )
            else:
                st.write("No matching books found.")

    with tab4:
        st.header("📚 All Books")
        library = st.session_state["library"]
        if library:
            df = pd.DataFrame(library)
            df = style_read_status(df)
            table_style = """
            <style>
            table {
                width: 100%;
                border-collapse: collapse;
            }
            th, td {
                padding: 8px;
                text-align: left;
                border-bottom: 1px solid #ddd;
            }
            tr:hover {
                background-color: #f5f5f5;
            }
            </style>
            """
            st.write(
                table_style + df.to_html(escape=False, index=False),
                unsafe_allow_html=True,
            )
        else:
            st.write("Your library is empty.")

    with tab5:
        st.header("📊 Library Statistics")
        library = st.session_state["library"]
        total = len(library)
        if total > 0:
            read_count = sum(book["read"] for book in library)
            percentage = (read_count / total) * 100
            st.write(f"Total books: {total}")
            st.write(f"Percentage read: {percentage:.1f}%")
        else:
            st.write("Total books: 0")
            st.write("Percentage read: 0.0%")


if __name__ == "__main__":
    main()
