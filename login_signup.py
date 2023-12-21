# login_signup.py

import os
import mysql.connector as sqltor

def create_database():
    db = sqltor.connect(
        host="localhost",
        user="root",
        passwd="1234",
    )
    cursor = db.cursor()
    cursor.execute("CREATE DATABASE IF NOT EXISTS login_system")
    db.database = "login_system"
    cursor.execute("CREATE TABLE IF NOT EXISTS users (id INT AUTO_INCREMENT PRIMARY KEY, username VARCHAR(255), password VARCHAR(255), is_staff BOOLEAN)")
    db.close()

def signup():
    username = input("Enter a username: ")
    password = input("Enter a password: ")
    is_staff = input("Are you a staff member? (yes/no): ").lower() == "yes"

    if is_staff:
        root_pass = input("Enter the root password for staff creation: ")
        if root_pass == "q94fz7c2ir":
            create_user(username, password, is_staff)
            print("Staff user created successfully.")
        else:
            print("Invalid root password. Staff user not created.")
    else:
        create_user(username, password, is_staff)
        print("User created successfully.")

def create_user(username, password, is_staff):
    db = sqltor.connect(
        host="localhost",
        user="root",
        passwd="1234",
        database="login_system"
    )
    cursor = db.cursor()
    cursor.execute("INSERT INTO users (username, password, is_staff) VALUES (%s, %s, %s)", (username, password, is_staff))
    db.commit()
    db.close()

def login():
    username = input("Enter your username: ")
    password = input("Enter your password: ")
    
    db = sqltor.connect(
        host="localhost",
        user="root",
        passwd="1234",
        database="login_system"
    )
    cursor = db.cursor()
    cursor.execute("SELECT is_staff FROM users WHERE username = %s AND password = %s", (username, password))
    user_data = cursor.fetchone()

    if user_data:
        is_staff = user_data[0]
        print("Login successful!")
        return username, is_staff
    else:
        print("Invalid username or password.")
        return None, False

def login_signup_page():
    create_database()
    
    while True:
        print("\nLogin/Signup Page:")
        print("1. Login")
        print("2. Signup")
        print("3. Exit")
        choice = input("Enter your choice: ")

        if choice == "1":
            username, is_staff = login()
            if username:
                return username, is_staff
        elif choice == "2":
            signup()
        elif choice == "3":
            print("Exiting the program.")
            exit()
        else:
            print("Invalid choice. Please enter a valid option.")

# Automatically run the login/signup page
if __name__ == "__main__":
    login_signup_page()
