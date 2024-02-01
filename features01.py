import mysql.connector

# Database connection
db = mysql.connector.connect(
    host="localhost",
    user="root",
    passwd="1234",
)
cursor = db.cursor()

# Reserve a book
def reserve_book():
    book_id = input("Enter the book ID to reserve: ")
    member_id = input("Enter your member ID: ")

    # Check if the book is available
    cursor.execute("SELECT status FROM books WHERE book_id = %s", (book_id,))
    status = cursor.fetchone()

    if not status:
        print("Book not found.")
        return

    if status[0] == "available":
        cursor.execute("UPDATE books SET status = 'reserved' WHERE book_id = %s", (book_id,))
        cursor.execute("INSERT INTO reservations (book_id, member_id) VALUES (%s, %s)", (book_id, member_id))
        db.commit()
        print("Book reserved successfully.")
    else:
        print("Book is not available for reservation.")

# Renew a book
def renew_book():
    book_id = input("Enter the book ID to renew: ")

    # Select the library database
    cursor.execute("USE library_db")

    # Check if the book is borrowed by the member
    cursor.execute("SELECT status, member_id FROM books WHERE book_id = %s", (book_id,))
    book_data = cursor.fetchone()

    if not book_data:
        print("Book not found.")
        return

    if book_data[0] == "borrowed":
        member_id = input("Enter your member ID: ")
        if member_id == book_data[1]:
            cursor.execute("UPDATE books SET due_date = DATE_ADD(due_date, INTERVAL 14 DAY) WHERE book_id = %s", (book_id,))
            db.commit()
            print("Book renewed successfully.")
        else:
            print("You are not the borrower of this book.")
    else:
        print("Book is not borrowed.")

# Calculate fines for overdue books
def calculate_fines():
    member_id = input("Enter your member ID: ")

    cursor.execute("SELECT SUM(DATEDIFF(NOW(), due_date)) * 0.50 FROM books WHERE member_id = %s AND status = 'borrowed'", (member_id,))
    total_fine = cursor.fetchone()[0]

    if total_fine:
        print(f"Total fine: ${total_fine:.2f}")
    else:
        print("No fines to calculate.")

# Show book details
def show_book_details():
    book_id = input("Enter the book ID: ")

    cursor.execute("SELECT * FROM books WHERE book_id = %s", (book_id,))
    book_details = cursor.fetchone()

    if not book_details:
        print("Book not found.")
    else:
        print("Book Details:")
        print("Book ID:", book_details[0])
        print("Title:", book_details[1])
        print("Author:", book_details[2])
        print("Status:", book_details[3])
        print("Due Date:", book_details[4])

# Show member details
def show_member_details():
    member_id = input("Enter the member ID: ")

    cursor.execute("SELECT * FROM members WHERE member_id = %s", (member_id,))
    member_details = cursor.fetchone()

    if not member_details:
        print("Member not found.")
    else:
        print("Member Details:")
        print("Member ID:", member_details[0])
        print("Name:", member_details[1])
        print("Email:", member_details[2])

def manage_books():
    while True:
        print("Manage Books:")
        print("1. Reserve a Book")
        print("2. Renew a Book")
        print("3. Calculate Fines")
        print("4. Show Book Details")
        print("5. Back to main menu")
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

def issue_book():
    book_id = input("Enter the ID of the book to issue: ")
    member_id = input("Enter the ID of the member to issue the book to: ")
    return_date = input("Enter the return date of the book: ")

    # Check if the book is available
    cursor.execute("SELECT available FROM books WHERE id = %s", (book_id,))
    available = cursor.fetchone()[0]
    if not available:
        print("The book is not available.")
        return

    # Check if the member is a valid member
    cursor.execute("SELECT name FROM members WHERE id = %s", (member_id,))
    name = cursor.fetchone()
    if name is None:
        print("The member is not a valid member.")
        return

    # Lend the book to the member
    cursor.execute("UPDATE books SET available = 0 WHERE id = %s", (book_id,))
    cursor.execute("INSERT INTO book_issues (book_id, member_id, return_date) VALUES (%s, %s, %s)", (book_id, member_id, return_date))
    db.commit()
    print("Book issued successfully!")
