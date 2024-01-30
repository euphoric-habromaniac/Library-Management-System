# main.py

import mysql.connector as sqltor
from tabulate import tabulate
from features01 import *  # Import functions from features01.py
from login_signup import login_signup_page  # Import the login/signup page

# Create a connection to the MySQL server (without specifying database)
mydb = sqltor.connect(host="localhost", user="root", password="1234")
cursor = mydb.cursor()

# Create the library database if it doesn't exist
cursor.execute("CREATE DATABASE IF NOT EXISTS library_db")

# Switch to the library database
mydb.database = "library_db"

# Automatically run the login/signup page
username, is_staff = login_signup_page()

# Function to create necessary tables in the database
def create_tables():
    # Creating a table to store books
    cursor.execute("CREATE TABLE IF NOT EXISTS books (id INT AUTO_INCREMENT PRIMARY KEY, title VARCHAR(255), author VARCHAR(255), available BOOLEAN)")
    
    # Creating a table to store members
    cursor.execute("CREATE TABLE IF NOT EXISTS members (id INT AUTO_INCREMENT PRIMARY KEY, name VARCHAR(255), email VARCHAR(255), fines DECIMAL(10, 2) DEFAULT 0.0)")
    # Add 'fines' column with DECIMAL(10, 2) to store decimal values with 2 decimal places, and a default value of 0.0
    
    # Creating a table to track book lending
    cursor.execute("CREATE TABLE IF NOT EXISTS book_lending (id INT AUTO_INCREMENT PRIMARY KEY, book_id INT, member_id INT, return_date DATE, FOREIGN KEY (book_id) REFERENCES books(id), FOREIGN KEY (member_id) REFERENCES members(id))")


#function to make reports
def reports():
    """
    Generate reports for the library.
    """
    # Print the reports menu
    print("\nReports Menu")
    print("1. List of all books that are currently checked out.")
    print("2. List of all members who have overdue books.")
    print("3. Fines report for a particular member")
    print("4. Number of books borrowed by each member")
    print("5. Most popular books")
    print("6. Least popular books")
    print("7. Return to previous menu")
    
    # Get the user's choice of report
    choice = input("Select a report to generate: ")

    # Generate the report
    if choice == "1":
        # List of all books that are currently checked out.
        cursor.execute("SELECT id, title, author FROM books WHERE available = False")
        books = cursor.fetchall()
        if books:
            print("List of all books that are currently checked out:")
            for book in books:
                print(f"ID: {book[0]}, Title: {book[1]}, Author: {book[2]}")
        else:
            print("No books are currently checked out.")

    elif choice == "2":
        # List of all members who have overdue books.
        cursor.execute("SELECT id, name FROM members WHERE id IN (SELECT member_id FROM book_lending WHERE return_date < CURDATE())")
        members = cursor.fetchall()
        if members:
            print("List of all members who have overdue books:")
            for member in members:
                print(f"ID: {member[0]}, Name: {member[1]}")
        else:
            print("No members have overdue books.")

    elif choice == "3":
        # Fines report for a particular member.
        member_id = input("Enter the ID of the member: ")
        cursor.execute("SELECT fines FROM members WHERE id = %s", (member_id,))
        fines = cursor.fetchone()[0]
        if fines:
            print(f"Fines for member ID {member_id}: {fines}")
        else:
            print(f"No fines for member ID {member_id}.")

    elif choice == "4":
        # Number of books borrowed by each member.
        cursor.execute("SELECT member_id, COUNT(*) AS num_books FROM book_lending GROUP BY member_id")
        borrowed_books = cursor.fetchall()
        if borrowed_books:
            print("Number of books borrowed by each member:")
            for borrowed_book in borrowed_books:
                print(f"ID: {borrowed_book[0]}, Number of books: {borrowed_book[1]}")
        else:
            print("No books have been borrowed.")

    elif choice == "5":
        # Most popular books.
        cursor.execute("SELECT book_id, COUNT(*) AS num_borrows FROM book_lending GROUP BY book_id ORDER BY num_borrows DESC LIMIT 10")
        most_popular_books = cursor.fetchall()
        if most_popular_books:
            print("Most popular books:")
            for book in most_popular_books:
                print(f"ID: {book[0]}, Number of borrows: {book[1]}")
        else:
            print("No books have been borrowed.")

    elif choice == "6":
        # Least popular books.
        cursor.execute("SELECT book_id, COUNT(*) AS num_borrows FROM book_lending GROUP BY book_id ORDER BY num_borrows ASC LIMIT 10")
        least_popular_books = cursor.fetchall()
        if least_popular_books:
            print("Least popular books:")
            for book in least_popular_books:
                print(f"ID: {book[0]}, Number of borrows: {book[1]}")
        else:
            print("No books have been borrowed.")

    elif choice == "7":
        return

    else:
        print("Invalid choice.")

# Function to manage books
def manage_books():
    while True:
        print("\nManage Books:")
        print("1. Add Book")
        print("2. Update Book")
        print("3. Delete Book")
        print("4. Show Available Books")
        print("5. Issue / Return Books")
        print("6. More")
        print("7. Return to main menu")
        choice = input("Enter your choice: ")

        if choice == "1":
            title = input("Enter the title of the book: ")
            author = input("Enter the author of the book: ")
            add_book(title, author)
        elif choice == "2":
            book_id = input("Enter the ID of the book to update: ")
            title = input("Enter the new title of the book: ")
            author = input("Enter the new author of the book: ")
            cursor.execute("UPDATE books SET title = %s, author = %s WHERE id = %s", (title, author, book_id))
            mydb.commit()
            print("Book updated successfully!")
        elif choice == "3":
            book_id = input("Enter the ID of the book to delete: ")
            cursor.execute("DELETE FROM books WHERE id = %s", (book_id,))
            mydb.commit()
            print("Book deleted successfully!")
        elif choice == "4":
            show_available_books()
        elif choice == "5":
            issue_return_books()
        elif choice == "6":
            # Call the features page function
            features_page()
        elif choice == "7":
            break
        else:
            print("Invalid choice. Please enter a valid option.")

# Function to manage members
def manage_members():
    while True:
        print("\nManage Members:")
        print("1. Add Member")
        print("2. Show Members")
        print("3. Show Member Details")
        print("4. Return to main menu")
        choice = input("Enter your choice: ")

        if choice == "1":
            name = input("Enter the name of the member: ")
            email = input("Enter the email of the member: ")
            add_member(name, email)
        elif choice == "2":
            show_members()
        elif choice == "3":
            show_member_details()
        elif choice == "4":
            break
        else:
            print("Invalid choice. Please enter a valid option.")


# Add a function to call functions from features01.py
def features_page():
    while True:
        print("\nFeatures Page:")
        print("1. Reserve a Book")
        print("2. Renew a Book")
        print("3. Calculate Fines")
        print("4. Show Book Details")
        print("5. Return to main menu")
        choice = input("Enter your choice: ")

        if choice == "1":
            reserve_book()
        elif choice == "2":
            renew_book()
        elif choice == "3":
            calculate_fines()
        elif choice == "4":
            show_book_details()
        elif choice == "5":
            break
        else:
            print("Invalid choice. Please enter a valid option.")

# Function to add a book to the library
def add_book(title, author):
    cursor.execute("INSERT INTO books (title, author, available) VALUES (%s, %s, %s)", (title, author, True))
    mydb.commit()
    print("Book added successfully!")

# Function to add a member
def add_member(name, email):
    cursor.execute("INSERT INTO members (name, email) VALUES (%s, %s)", (name, email))
    mydb.commit()
    print("Member added successfully!")

# Function to lend a book to a member
def lend_book(book_id, member_id, return_date):
    cursor.execute("UPDATE books SET available = False WHERE id = %s", (book_id,))
    cursor.execute("INSERT INTO book_lending (book_id, member_id, return_date) VALUES (%s, %s, %s)", (book_id, member_id, return_date))
    mydb.commit()
    print("Book lent successfully!")

# Function to return a book
def return_book(book_id):
    cursor.execute("UPDATE books SET available = True WHERE id = %s", (book_id,))
    cursor.execute("DELETE FROM book_lending WHERE book_id = %s", (book_id,))
    mydb.commit()
    print("Book returned successfully!")

# Function to show available books
def show_available_books():
    cursor.execute("SELECT id, title, author FROM books WHERE available = True")
    available_books = cursor.fetchall()
    if available_books:
        print("Available Books:")
        for book in available_books:
            print(f"ID: {book[0]}, Title: {book[1]}, Author: {book[2]}")
    else:
        print("No available books.")

# Function to show members
def show_members():
    cursor.execute("SELECT id, name, email FROM members")
    members = cursor.fetchall()
    if members:
        print("Members:")
        for member in members:
            print(f"ID: {member[0]}, Name: {member[1]}, Email: {member[2]}")
    else:
        print("No members.")

# Function to issue/return a book
def issue_return_books():
    while True:
        print("\nIssue/Return Books:")
        print("1. Issue Book")
        print("2. Return Book")
        print("3. Return to main menu")
        choice = input("Enter your choice: ")

        if choice == "1":
            book_id = input("Enter the ID of the book to lend: ")
            member_id = input("Enter the ID of the member: ")
            return_date = input("Enter the return date (YYYY-MM-DD): ")
            lend_book(book_id, member_id, return_date)
        elif choice == "2":
            book_id = input("Enter the ID of the book to return: ")
            return_book(book_id)
        elif choice == "3":
            break
        else:
            print("Invalid choice. Please enter a valid option.")


# Creating necessary tables
create_tables()

# main loop menu6
while True:
    if (is_staff == 1):
            print("\nMain Menu:")
            print("1. Manage Books")
            print("2. Manage Members")
            print("3. Reports")
            print("4. Exit")
            option = input("Enter your choice: ")

            if option == "1":
                manage_books()
            elif option == "2":
                manage_members()
            elif option == "3":
                reports()
            elif option == "4":
                print("Exiting the program.")
                break
            else:
                print("Invalid choice. Please enter a valid option.")
    else :
            print("\nMain Menu:")
            print("1. Show Available Books")
            print("2. Issue / Return Books")
            print("3. Exit")
            option = input("Enter your choice: ")

            if option == "1":
                show_available_books()
            elif option == "2":
                issue_return_books()
            elif option == "3":
                print("Exiting the program.") 
                break
            else:
                print("Invalid choice.")


# Close the database connection
mydb.close()
