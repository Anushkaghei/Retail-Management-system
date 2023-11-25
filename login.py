from tkinter import *
from functools import partial
import time
from admin import OnlineShoppingAdminGUI
import shopping_page
# Connecting to the database

def create_trigger_phone_no(connection, cursor):
    trigger_phone_no = """
    CREATE TRIGGER IF NOT EXISTS before_insert_update_phone_number
    BEFORE INSERT ON Users
    FOR EACH ROW
    BEGIN
        IF NEW.Phone_Number IS NOT NULL AND NEW.Phone_Number NOT LIKE '+91%' THEN
            SET NEW.Phone_Number = CONCAT('+91 ', NEW.Phone_Number);
        END IF;
    END;
    """
    cursor.execute(trigger_phone_no)
    connection.commit()

def create_function_email(connection,cursor):
    function_email = """
    CREATE FUNCTION IF NOT EXISTS is_valid_email(email VARCHAR(255)) RETURNS BOOLEAN DETERMINISTIC
    BEGIN
        DECLARE at_pos INT;
        DECLARE dot_com_pos INT;
        DECLARE dot_in_pos INT;
        DECLARE dot_edu_pos INT;

        SET at_pos = LOCATE('@', email);
        SET dot_com_pos = LOCATE('.com', email);
        SET dot_in_pos = LOCATE('.in', email);
        SET dot_edu_pos = LOCATE('.edu', email);

        IF at_pos > 0 AND (dot_com_pos = LENGTH(email) - 3 OR dot_in_pos = LENGTH(email) - 2 OR dot_edu_pos = LENGTH(email) - 3) THEN
            RETURN TRUE;
        ELSE
            RETURN FALSE;
        END IF;
    END;
    """
    cursor.execute(function_email)
    connection.commit()


def error_destroy():
    err.destroy()


def succ_destroy():
    succ.destroy()
    root1.destroy()


def fields_error():
    global err
    err = Toplevel(root1)
    err.title("Error")
    err.geometry("200x100")
    Label(err, text="All fields are required", fg="red", font="bold").pack()
    Label(err, text="").pack()
    Button(err, text="Ok", bg="grey", width=8, height=1, command=error_destroy).pack()


def password_error():
    global err
    err = Toplevel(root1)
    err.title("Error")
    err.geometry("200x100")
    Label(err, text="Passwords not matching", fg="red", font="bold").pack()
    Label(err, text="").pack()
    Button(err, text="Ok", bg="grey", width=8, height=1, command=error_destroy).pack()


def email_error():
    global err
    err = Toplevel(root1)
    err.title("Error")
    err.geometry("200x100")
    Label(err, text="Invalid email ID", fg="red", font="bold").pack()
    Label(err, text="").pack()
    Button(err, text="Ok", bg="grey", width=8, height=1, command=error_destroy).pack()

def login_verify(connection,cursor):
    user_verify = User_ID_verify.get()
    pas_verify = password_verify.get()

    if user_verify.lower() == 'admin' and pas_verify == 'admin':
        open_admin_page(connection,cursor)
    else:
        sql = "select * from Users where User_ID = %s and password = %s"
        cursor.execute(sql, [(user_verify), (pas_verify)])
        results = cursor.fetchone()
        if results:
            for i in results:
                logged(connection,cursor)
                break
        else:
            failed()

def is_valid_email(cursor,email):
    # Call the stored function is_valid_email
    sql = "SELECT is_valid_email(%s)"
    t = (email,)
    cursor.execute(sql, t)
    # Fetch the result
    result = cursor.fetchone()[0]

    # Return the result
    return bool(result)


def success():
    global succ
    succ = Toplevel(root1)
    succ.title("Success")
    succ.geometry("200x100")
    Label(succ, text="Registration successful...", fg="green", font="bold").pack()
    Label(succ, text="").pack()
    Button(succ, text="Ok", bg="grey", width=8, height=1, command=succ_destroy).pack()


def register_user(connection,cursor):
    username_info = User_ID.get()
    password_info = password.get()
    confirm_password_info = confirm_password.get()
    phone_info = Phone_Number.get()
    email_info = email.get()
    address_info = address.get()

    if username_info == "" or password_info == "" or confirm_password_info == "" or phone_info == "" or email_info == "" or address_info == "":
        fields_error()
    elif password_info != confirm_password_info:
        # Passwords do not match, show an error
        password_error()

    elif is_valid_email(cursor,email_info) == False:
        email_error()
    else:
        # Passwords match, proceed with registration
        sql = "INSERT INTO Users VALUES (%s, %s, %s, %s, %s)"
        t = (username_info, email_info, phone_info, password_info, address_info)
        cursor.execute(sql, t)
        connection.commit()
        Label(root1, text="").pack()
        time.sleep(0.50)
        success()


def registration(connection,cursor):
    global root1
    root1 = Toplevel(root)
    root1.title("Registration Portal")
    root1.geometry("400x400")  # Increased height to accommodate additional fields
    global User_ID
    global password
    global confirm_password
    global Phone_Number
    global email
    global address
    Label(root1, text="Register your account", bg="grey", fg="black", font="bold", width=500).pack()
    User_ID = StringVar()
    password = StringVar()
    confirm_password = StringVar()
    Phone_Number = StringVar()
    email = StringVar()
    address = StringVar()

    Label(root1, text="").pack()
    Label(root1, text="Username:", font="bold").pack()
    Entry(root1, textvariable=User_ID).pack()

    Label(root1, text="").pack()
    Label(root1, text="Password:").pack()
    Entry(root1, textvariable=password, show="*").pack()

    Label(root1, text="").pack()
    Label(root1, text="Confirm Password:").pack()
    Entry(root1, textvariable=confirm_password, show="*").pack()

    Label(root1, text="").pack()
    Label(root1, text="Phone Number:").pack()
    Entry(root1, textvariable=Phone_Number).pack()

    Label(root1, text="").pack()
    Label(root1, text="Email Address:").pack()
    Entry(root1, textvariable=email).pack()

    Label(root1, text="").pack()
    Label(root1, text="Address:").pack()
    Entry(root1, textvariable=address).pack()

    Label(root1, text="").pack()
    Button(root1, text="Register", bg="red", command=partial(register_user,connection,cursor)).pack()


def login(connection,cursor):
    global root2
    root2 = Toplevel(root)
    root2.title("Log-In Portal")
    root2.geometry("300x300")
    global User_ID_verify
    global password_verify
    Label(root2, text="Log-In Portal", bg="grey", fg="black", font="bold", width=300).pack()
    User_ID_verify = StringVar()
    password_verify = StringVar()
    Label(root2, text="").pack()
    Label(root2, text="Username :", font="bold").pack()
    Entry(root2, textvariable=User_ID_verify).pack()
    Label(root2, text="").pack()
    Label(root2, text="Password :").pack()
    Entry(root2, textvariable=password_verify, show="*").pack()
    Label(root2, text="").pack()
    Button(root2, text="Log-In", bg="red", command=partial(login_verify,connection,cursor)).pack()
    Label(root2, text="")




def fail_destroy():
    fail.destroy()


def logged(connection,cursor):
    global logg
    logg = Toplevel(root2)
    logg.title("Welcome")
    logg.geometry("200x100")
    Label(logg, text="Welcome {} ".format(User_ID_verify.get()), fg="green", font="bold").pack()
    Label(logg, text="").pack()

    root.destroy()
    shopping_page.main(connection,cursor,'user')



def failed():
    global fail
    fail = Toplevel(root2)
    fail.title("Invalid")
    fail.geometry("200x100")
    Label(fail, text="Invalid credentials", fg="red", font="bold").pack()
    Label(fail, text="").pack()
    Button(fail, text="Ok", bg="grey", width=8, height=1, command=fail_destroy).pack()

def open_admin_page(connection,cursor):
    root = Tk()
    app = OnlineShoppingAdminGUI(root,connection,cursor)

    root.mainloop()


def main_screen(connection,cursor):
    global root
    root = Tk()
    root.title("Log-IN Portal")
    root.geometry("300x300")
    Label(root, text="Welcome to Log-In Protal", font="bold", bg="grey", fg="black", width=300).pack()
    Label(root, text="").pack()
    Button(root, text="Log-IN", width="8", height="1", bg="red", font="bold", command=partial(login,connection,cursor)).pack()
    Label(root, text="").pack()
    Button(root, text="Registration", height="1", width="15", bg="red", font="bold", command = partial(registration,connection,cursor)).pack()
    Label(root, text="").pack()
    Label(root, text="").pack()


def main(connection,cursor):
        create_trigger_phone_no(connection, cursor)
        create_function_email(connection,cursor)
        main_screen(connection,cursor)
        root.mainloop()



