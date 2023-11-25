import pymysql

tables = {}


tables['Products'] = """create table IF NOT EXISTS Products(
    itemname char(45) not null,
    Price varchar(10) NOT NULL, 
    Category char(10),
    Product_Description varchar(100));"""

tables['Payment_Info'] = """create table IF NOT EXISTS Payment_Info(
    Payment_ID int auto_increment,
    Mode_of_Payment char(50),
    Total char(20),
    primary key(Payment_ID));"""

tables['Orders'] = """create table IF NOT EXISTS Orders(
    Order_ID char(6), 
    ETA date,
    Payment_ID int,
    User_ID char(50),
    primary key(Order_ID));"""

tables['Users'] = """create table IF NOT EXISTS Users(
    User_ID char(50) NOT NULL, 
    Email varchar(40),
    Phone_Number varchar(14),
    Password varchar(20),
    Address varchar(100),
    primary key(User_ID));"""
    

tables['Cart_Items'] = """create table IF NOT EXISTS Cart_Items(
    itemname char(45),
    price char(10),
    Size char(10),
    check (Size in("X small","small","medium","large","X large","XX large")),
    primary key(itemname));"""

tables['Categories'] = """create table IF NOT EXISTS Categories(
    Category_ID char(10) NOT NULL,
    Sub_Category varchar(20),
    Category varchar(20),
    Gender char(1),
    check (Gender in("M","F")),
    primary key(Category_ID));"""

'''
category_id = model
sub_category = category
category = maincat

'''
foreign_keys = [
    """ALTER TABLE Products ADD FOREIGN KEY (itemname) REFERENCES Cart_Items(itemname)""",
    """ALTER TABLE Products ADD FOREIGN KEY (Category) REFERENCES Categories(Sub_Category)""",
    """ALTER TABLE Orders ADD FOREIGN KEY (Payment_ID) REFERENCES Payment_Info(Payment_ID)""",
    """ALTER TABLE Orders ADD FOREIGN KEY (User_ID) REFERENCES Users(User_ID)"""]

def privileges(connection,cursor):
    create =  "CREATE USER IF NOT EXISTS 'admin'@'localhost' IDENTIFIED BY 'admin'"
    cursor.execute(create)
    admin = "GRANT ALL PRIVILEGES ON *.* TO 'admin'@'localhost' WITH GRANT OPTION;"
    cursor.execute(admin)
    connection.commit()

def create_and_use_database(cursor):
    try:
        cursor.execute("CREATE DATABASE IF NOT EXISTS SHOPPING;")
    except pymysql.Error as err:
        print("Failed creating database SHOPPING".format(err))
        exit(1)
    else:
        cursor.execute("USE SHOPPING;")
        print("Successfully using database SHOPPING")

def main(connection,cursor):
    create_and_use_database(cursor)

    for table_name in tables:
        table_description = tables[table_name]
        try:
            print("Creating table IF NOT EXISTS {} ".format(table_name), end='\n')
            cursor.execute(table_description)
        except pymysql.Error as err:
            if err.args[0] == 1050:  # 1050 means table already exists
                print("already exists.")
            else:
                print(err)
    
    privileges(connection,cursor)

'''
    for key in foreign_keys:
        try:
            cursor.execute(key)
        except pymysql.Error as err:
            print(err)
        else:
            print("OK")
'''
