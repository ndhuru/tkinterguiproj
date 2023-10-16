import tkinter as tk
import sqlite3
import hashlib

conn = sqlite3.connect('allmyusers.db')
cursor = conn.cursor()

newtableQuery = '''
CREATE TABLE IF NOT EXISTS users (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    username TEXT NOT NULL UNIQUE,
    password TEXT NOT NULL,
    first_name TEXT,
    last_name TEXT
);
'''
cursor.execute(newtableQuery)


def newUser(username, password, first_name, last_name):
    insertQuery = '''
    INSERT INTO users (username, password, first_name, last_name)
    VALUES (?, ?, ?, ?);
    '''
    cursor.execute(insertQuery, (username, password, first_name, last_name))
    conn.commit()
    print("New user created successfully!")


def loginUser(username, password):
    select_query = '''
    SELECT * FROM users WHERE username = ? AND password = ?;
    '''
    cursor.execute(select_query, (username, password))
    user = cursor.fetchone()

    if user:
        welcome_window = tk.Toplevel()
        welcome_window.geometry("900x600")

        welcome_label = tk.Label(welcome_window, text=f"Welcome!")
        welcome_label.pack()
    else:
        print("Not a user in the system, sign up first please.")


def displayAllUsers(admin_password):
    hashed_admin_password = hashlib.sha256(admin_password.encode()).hexdigest()
    if admin_password == "LosPollosHermanos":
        select_all_query = '''
        SELECT * FROM users;
        '''
        cursor.execute(select_all_query)
        all_users = cursor.fetchall()
        viewer_window = tk.Toplevel()

        if all_users:
            for user in all_users:
                id_label = tk.Label(viewer_window, text=f"ID: {user[0]}")
                username_label = tk.Label(viewer_window, text=f"Username: {user[1]}")
                first_name_label = tk.Label(viewer_window, text=f"First Name: {user[3]}")
                last_name_label = tk.Label(viewer_window, text=f"Last Name: {user[4]}")

                id_label.pack()
                username_label.pack()
                first_name_label.pack()
                last_name_label.pack()
        else:
            no_users_label = tk.Label(viewer_window, text="No users found")
            no_users_label.pack()
    else:
        invalid_password_label = tk.Label(viewer_window, text="Invalid password")
        invalid_password_label.pack()


def signupMaker():
    def signup():
        username = username_entry.get()
        password = password_entry.get()
        first_name = first_name_entry.get()
        last_name = last_name_entry.get()
        newUser(username, password, first_name, last_name)
        signup_window.destroy()

    signup_window = tk.Toplevel(root)

    username_label = tk.Label(signup_window, text="Username:")
    username_label.pack()
    username_entry = tk.Entry(signup_window)
    username_entry.pack()

    password_label = tk.Label(signup_window, text="Password:")
    password_label.pack()
    password_entry = tk.Entry(signup_window)
    password_entry.pack()

    first_name_label = tk.Label(signup_window, text="First Name:")
    first_name_label.pack()
    first_name_entry = tk.Entry(signup_window)
    first_name_entry.pack()

    last_name_label = tk.Label(signup_window, text="Last Name:")
    last_name_label.pack()
    last_name_entry = tk.Entry(signup_window)
    last_name_entry.pack()

    signup_button = tk.Button(signup_window, text="Sign Up", command=signup)
    signup_button.pack()


def loginMode():
    def login():
        username = username_entry.get()
        password = password_entry.get()
        loginUser(username, password)
        login_window.destroy()

    login_window = tk.Toplevel(root)

    username_label = tk.Label(login_window, text="Username:")
    username_label.pack()
    username_entry = tk.Entry(login_window)
    username_entry.pack()

    password_label = tk.Label(login_window, text="Password:")
    password_label.pack()
    password_entry = tk.Entry(login_window)
    password_entry.pack()

    login_button = tk.Button(login_window, text="Login", command=login)
    login_button.pack()


def adminMode():
    def viewUsers():
        admin_password = admin_password_entry.get()
        displayAllUsers(admin_password)
        viewUsers_window.destroy()

    viewUsers_window = tk.Toplevel(root)

    admin_password_label = tk.Label(viewUsers_window, text="Admin Password:")
    admin_password_label.pack()
    admin_password_entry = tk.Entry(viewUsers_window, show="*")
    admin_password_entry.pack()

    viewUsers_button = tk.Button(viewUsers_window, text="View Users", command=viewUsers)
    viewUsers_button.pack()


root = tk.Tk()
root.geometry("900x600")
root.title("Login thing")

signup_button = tk.Button(root, text="Sign Up", command=signupMaker)
signup_button.pack()

login_button = tk.Button(root, text="Log In", command=loginMode)
login_button.pack()

admin_view_button = tk.Button(root, text="Admin View (display users here)", command=adminMode)
admin_view_button.pack()

root.mainloop()

conn.close()
