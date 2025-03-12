import streamlit as st
import json
import os
import pandas as pd

def load_library(filename):
    if os.path.exists(filename):
        try:
            with open(filename, "r") as file:
                return json.load(file)
        except json.JSONDecodeError:
            st.error("⚠️ Error loading library file. Starting with an empty library.")
            return []
    return []

def save_library(library, filename):
    try:
        with open(filename, "w") as file:
            json.dump(library, file, indent=4)
    except Exception as e:
        st.error(f"⚠️ Error saving library: {e}")

def initialize_state():
    if "library" not in st.session_state:
        st.session_state["library"] = load_library("library.json")
    if "active_tab" not in st.session_state:
        st.session_state["active_tab"] = "Add Book"
    if "success_message" not in st.session_state:
        st.session_state["success_message"] = None

def reset_success_message():
    st.session_state["success_message"] = None

def main():
    filename = "library.json"
    initialize_state()
    
    st.set_page_config(page_title="Personal Library Manager", layout="centered")
    st.title("📚 Personal Library Manager")
    
    tab_names = ["Add Book", "Remove Book", "Search Books", "View All Books", "Statistics"]
    active_tab = st.session_state["active_tab"]
    tabs = st.tabs(tab_names)
    
    if st.session_state["success_message"]:
        st.success(st.session_state["success_message"])
        st.session_state["success_message"] = None  
        
    with tabs[0]:
        st.header("📖 Add a Book")
        with st.form(key="add_book_form", clear_on_submit=True):
            title = st.text_input("Title", placeholder="Enter book title")
            author = st.text_input("Author", placeholder="Enter author name")
            year = st.number_input("Publication Year", min_value=1000, max_value=9999, step=1)
            genre = st.text_input("Genre", placeholder="Enter genre")
            read = st.radio("Have you read this book?", ("Yes", "No")) == "Yes"

            submit = st.form_submit_button("Add Book")
            if submit:
                if title and author and genre:
                    book = {"title": title, "author": author, "year": int(year), "genre": genre, "read": read}
                    st.session_state["library"].append(book)
                    save_library(st.session_state["library"], filename)

                    st.session_state["success_message"] = "✅ Book added successfully!"
                    st.session_state["active_tab"] = "View All Books"
                    st.rerun()
                else:
                    st.error("⚠️ Please fill in all fields.")

    with tabs[1]:
        st.header("🗑 Remove a Book")
        title_to_remove = st.text_input("Enter the title of the book to remove")
        if st.button("Remove Book"):
            library = st.session_state["library"]
            for book in library[:]:
                if book["title"].lower() == title_to_remove.lower():
                    library.remove(book)
                    save_library(library, filename)

                    st.session_state["success_message"] = "✅ Book removed successfully!"
                    st.session_state["active_tab"] = "View All Books"
                    st.rerun()
                    break
            else:
                st.error("⚠️ Book not found.")

    with tabs[2]:
        st.header("🔍 Search for a Book")
        search_by = st.radio("Search by", ("Title", "Author"))
        search_term = st.text_input("Enter search term")

        if search_term:
            library = st.session_state["library"]
            matches = [book for book in library if search_term.lower() in book[search_by.lower()].lower()]

            if matches:
                df = pd.DataFrame(matches)
                df["Read Status"] = df["read"].apply(lambda x: "✔ Read" if x else "❌ Unread")
                df = df.drop(columns=["read"])
                st.dataframe(df)
            else:
                st.info("🔍 No matching books found.")

    with tabs[3]:
        st.header("📚 All Books")
        library = st.session_state["library"]
        
        if library:
            df = pd.DataFrame(library)
            df["Read Status"] = df["read"].apply(lambda x: "✔ Read" if x else "❌ Unread")
            df = df.drop(columns=["read"])
            st.dataframe(df)
        else:
            st.info("📚 Your library is empty.")

    with tabs[4]:
        st.header("📊 Library Statistics")
        library = st.session_state["library"]
        total_books = len(library)
        
        if total_books > 0:
            read_count = sum(book["read"] for book in library)
            read_percentage = (read_count / total_books) * 100

            col1, col2 = st.columns(2)
            col1.metric(label="📚 Total Books", value=total_books)
            col2.metric(label="📖 Books Read", value=f"{read_percentage:.1f}%")

            st.progress(int(read_percentage))
        else:
            st.write("**Total books:** 0")
            st.write("**Books read:** 0")
            st.write("**Percentage read:** 0.0%")

if __name__ == "__main__":
    main()
