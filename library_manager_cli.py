import json
import os


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
    title = input("Enter the book title: ")
    author = input("Enter the author: ")
    while True:
        year_str = input("Enter the publication year: ")
        if year_str.isdigit():
            year = int(year_str)
            break
        print("Please enter a valid year.")
    genre = input("Enter the genre: ")
    while True:
        read_status = input("Have you read this book? (yes/no): ").lower()
        if read_status in ["yes", "no"]:
            read = True if read_status == "yes" else False
            break
        print("Please enter 'yes' or 'no'.")
    book = {
        "title": title,
        "author": author,
        "year": year,
        "genre": genre,
        "read": read,
    }
    library.append(book)
    print("Book added successfully!")


def remove_book(library):
    """Remove a book by title from the library."""
    title = input("Enter the title of the book to remove: ")
    for book in library[:]:  
        if book["title"].lower() == title.lower():
            library.remove(book)
            print("Book removed successfully!")
            return
    print("Book not found.")


def search_books(library):
    """Search for books by title or author and display matches."""
    print("Search by:")
    print("1. Title")
    print("2. Author")
    search_type = input("Enter your choice: ")
    if search_type == "1":
        term = input("Enter the title: ").lower()
        matches = [book for book in library if term in book["title"].lower()]
    elif search_type == "2":
        term = input("Enter the author: ").lower()
        matches = [book for book in library if term in book["author"].lower()]
    else:
        print("Invalid choice.")
        return
    if matches:
        print("Matching Books:")
        for i, book in enumerate(matches, 1):
            status = "Read" if book["read"] else "Unread"
            print(
                f"{i}. {book['title']} by {book['author']} ({book['year']}) - {book['genre']} - {status}"
            )
    else:
        print("No matching books found.")


def display_all_books(library):
    """Display all books in the library with formatted output."""
    if not library:
        print("Your library is empty.")
    else:
        print("Your Library:")
        for i, book in enumerate(library, 1):
            status = "Read" if book["read"] else "Unread"
            print(
                f"{i}. {book['title']} by {book['author']} ({book['year']}) - {book['genre']} - {status}"
            )


def display_statistics(library):
    """Display total number of books and percentage read."""
    total = len(library)
    if total == 0:
        print("Total books: 0")
        print("Percentage read: 0.0%")
    else:
        read_count = sum(book["read"] for book in library)
        percentage = (read_count / total) * 100
        print(f"Total books: {total}")
        print(f"Percentage read: {percentage:.1f}%")


def print_menu():
    """Display the main menu."""
    print("\nWelcome to your Personal Library Manager!")
    print("1. Add a book")
    print("2. Remove a book")
    print("3. Search for a book")
    print("4. Display all books")
    print("5. Display statistics")
    print("6. Exit")


# Main program
def main():
    filename = "library.txt"
    library = load_library(filename)
    while True:
        print_menu()
        choice = input("Enter your choice: ")
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
            print("Library saved to file. Goodbye!")
            break
        else:
            print("Invalid choice. Please enter a number between 1 and 6.")


if __name__ == "__main__":
    main()
