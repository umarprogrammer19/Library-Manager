import json
import os
from colorama import Fore, Style, init

# Initialize colorama
init(autoreset=True)


def load_library(filename):
    """Load the library from a file if it exists; otherwise, return an empty list."""
    if os.path.exists(filename):
        with open(filename, "r") as file:
            return json.load(file)
    return []


def save_library(library, filename):
    """Save the library to a file."""
    with open(filename, "w") as file:
        json.dump(library, file)


def add_book(library):
    """Prompt user for book details and add the book to the library."""
    print(Fore.CYAN + "📖 Enter the book details:")
    title = input(Fore.GREEN + "Title: ")
    author = input(Fore.GREEN + "Author: ")

    while True:
        year_str = input(Fore.GREEN + "Publication Year: ")
        if year_str.isdigit():
            year = int(year_str)
            break
        print(Fore.RED + "⚠️ Please enter a valid year.")

    genre = input(Fore.GREEN + "Genre: ")

    while True:
        read_status = input(Fore.YELLOW + "Have you read this book? (yes/no): ").lower()
        if read_status in ["yes", "no"]:
            read = read_status == "yes"
            break
        print(Fore.RED + "⚠️ Please enter 'yes' or 'no'.")

    book = {"title": title, "author": author, "year": year, "genre": genre, "read": read}
    library.append(book)
    print(Fore.LIGHTGREEN_EX + "✅ Book added successfully!")


def remove_book(library):
    """Remove a book by title from the library."""
    title = input(Fore.YELLOW + "Enter the title of the book to remove: ")
    for book in library[:]:
        if book["title"].lower() == title.lower():
            library.remove(book)
            print(Fore.RED + "🗑 Book removed successfully!")
            return
    print(Fore.RED + "⚠️ Book not found.")


def search_books(library):
    """Search for books by title or author and display matches."""
    print(Fore.CYAN + "🔍 Search by:")
    print(Fore.YELLOW + "1. Title")
    print(Fore.YELLOW + "2. Author")
    search_type = input(Fore.YELLOW + "Enter your choice: ")

    if search_type == "1":
        term = input(Fore.GREEN + "Enter the title: ").lower()
        matches = [book for book in library if term in book["title"].lower()]
    elif search_type == "2":
        term = input(Fore.GREEN + "Enter the author: ").lower()
        matches = [book for book in library if term in book["author"].lower()]
    else:
        print(Fore.RED + "⚠️ Invalid choice.")
        return

    if matches:
        print(Fore.LIGHTBLUE_EX + "📚 Matching Books:")
        for i, book in enumerate(matches, 1):
            status = Fore.GREEN + "✔ Read" if book["read"] else Fore.RED + "❌ Unread"
            print(
                Fore.YELLOW
                + f"{i}. {book['title']} by {book['author']} ({book['year']}) - {book['genre']} - {status}"
            )
    else:
        print(Fore.RED + "⚠️ No matching books found.")


def display_all_books(library):
    """Display all books in the library with formatted output."""
    if not library:
        print(Fore.RED + "📂 Your library is empty.")
    else:
        print(Fore.LIGHTCYAN_EX + "📚 Your Library:")
        for i, book in enumerate(library, 1):
            status = Fore.GREEN + "✔ Read" if book["read"] else Fore.RED + "❌ Unread"
            print(
                Fore.YELLOW
                + f"{i}. {book['title']} by {book['author']} ({book['year']}) - {book['genre']} - {status}"
            )


def display_statistics(library):
    """Display total number of books and percentage read."""
    total = len(library)
    if total == 0:
        print(Fore.RED + "📂 Total books: 0")
        print(Fore.RED + "📊 Percentage read: 0.0%")
    else:
        read_count = sum(book["read"] for book in library)
        percentage = (read_count / total) * 100
        print(Fore.LIGHTMAGENTA_EX + f"📂 Total books: {total}")
        print(Fore.LIGHTMAGENTA_EX + f"📊 Percentage read: {percentage:.1f}%")


def print_menu():
    """Display the main menu."""
    print(Fore.LIGHTBLUE_EX + "\n📖 Welcome to your Personal Library Manager!")
    print(Fore.YELLOW + "1.  Add a book")
    print(Fore.YELLOW + "2.  Remove a book")
    print(Fore.YELLOW + "3.  Search for a book")
    print(Fore.YELLOW + "4.  Display all books")
    print(Fore.YELLOW + "5.  Display statistics")
    print(Fore.YELLOW + "6.  Exit")


# Main program
def main():
    filename = "library.json"
    library = load_library(filename)

    while True:
        print_menu()
        choice = input(Fore.CYAN + "👉 Enter your choice: ")

        if choice == "1":
            add_book(library)
        elif choice == "2":
            remove_book(library)
        elif choice == "3":
            search_books(library)
        elif choice == "4":
            display_all_books(library)
        elif choice == "5":
            display_statistics(library)
        elif choice == "6":
            save_library(library, filename)
            print(Fore.GREEN + "✅ Library saved. Goodbye! 👋")
            break
        else:
            print(Fore.RED + "⚠️ Invalid choice. Please enter a number between 1 and 6.")


if __name__ == "__main__":
    main()
