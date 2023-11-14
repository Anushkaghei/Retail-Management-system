import tkinter as tk
import pymysql
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import datetime

pay=[]
gl=[]#graph list
root=tk.Tk()
root.geometry("1600x800+0+0")
root.configure (bg="turquoise")

frame=tk.Frame(root).pack()
dict={}
l=[]
     
b=input("Do you wish to modify records (y/n):")
if(b=="Y" or b=="y"):
    import admin    
    
def insert():
    read_query="insert into products(itemname,price,category_id,product_description) values(%s,%s,%s,%s)"
    values=(name,price,model,category)
    cursor.execute(read_query,values)
    connection.commit()
    print("new record inserted")
    
'''
category_id = modelno
product_description = category
'''

tables = {}


tables['Products'] = """create table IF NOT EXISTS Products(
    itemcode int auto_increment, 
    itemname char(45) not null,
    Price varchar(10) NOT NULL, 
    Category_ID char(10),
    Product_Description varchar(100),
    primary key(itemcode));"""

tables['Payment_Info'] = """create table IF NOT EXISTS Payment_Info(
    Payment_ID int auto_increment,
    Mode_of_Payment char(50),
    Total char(20),
    primary key(Payment_ID));"""

tables['Orders'] = """create table IF NOT EXISTS Orders(
    Order_ID char(6), 
    ETA date,
    primary key(Order_ID));"""

tables['Users'] = """create table IF NOT EXISTS Users(
    User_ID char(50) NOT NULL, 
    Email varchar(40),
    Phone_Number char(10),
    Password varchar(20),
    Address varchar(100),
    primary key(User_ID));"""
    

tables['Cart_Items'] = """create table IF NOT EXISTS Cart_Items(
    itemname char(45),
    price char(10),
    Size char(10),
    check (Size in("X small","small","medium","large","X large","XX large")));"""

tables['Categories'] = """create table IF NOT EXISTS Categories(
    Category_ID char(10) NOT NULL,
    Sub_Category varchar(20),
    Category varchar(20),
    Gender char(1),
    check (Gender in("M","F")));"""

'''
category_id = model
sub_category = category
category = maincat

'''
#foreign_keys = [
#     """ ALTER TABLE Products ADD FOREIGN KEY (Category_ID) REFERENCES Categories(Category_ID);""",
  #   """ ALTER TABLE Orders ADD FOREIGN KEY (Payment_ID) REFERENCES Payment_Info(Payment_ID);""",
#     #""" ALTER TABLE Orders ADD FOREIGN KEY (itemcode) REFERENCES Products(itemcode);""",
#     """ ALTER TABLE Users ADD FOREIGN KEY (Previous_Orders) REFERENCES Orders(Order_ID);""",
#     """ ALTER TABLE Users ADD FOREIGN KEY (Active_Orders) REFERENCES Orders(Order_ID);"""
#]

def create_and_use_database(cursor):
    try:
        cursor.execute("CREATE DATABASE IF NOT EXISTS SHOPPING;")
    except pymysql.Error as err:
        print("Failed creating database SHOPPING".format(err))
        exit(1)
    else:
        cursor.execute("USE SHOPPING;")
        print("Successfully using database SHOPPING")

# Database connection parameters
host = "localhost"
user = "root"
#password=input("enter your mysql password :")

try:
    connection = pymysql.connect(host=host, user=user, password="Gobbles#77")
except pymysql.Error as e:
    print("Error")
    print(e)

else:
    cursor = connection.cursor()
    print("Connection established")

    # CREATE DATABASE SHOPPING
    # USE SHOPPING
    create_and_use_database(cursor)

    # CREATE TABLES
    for table_name in tables:
        table_description = tables[table_name]
        try:
            print("Creating table {}: ".format(table_name), end='')
            cursor.execute(table_description)
        except pymysql.Error as err:
            if err.args[0] == 1050:  # 1050 means table already exists
                print("already exists.")
            else:
                print(err)

    #ALTER TABLE ADD FOREIGN KEY
    # for key in foreign_keys:
    #     try:
    #         cursor.execute(key)
    #     except pymysql.Error as err:
    #         print(err)
    #     else:
    #         print("OK")

import projectext as ext

#concluding page


def final():
    final = tk.Tk()
    final.geometry("500x500+0+0")
    final.config(bg="aqua")
    final.title("THANK YOU !!")
    
    
    def get_next_order_id():
        # Function to get the next order ID based on the current maximum order ID in the database
        cursor.execute("SELECT MAX(Order_ID) FROM Orders")
        result = cursor.fetchone()[0]
        if result:
            next_order_id = int(result[1:]) + 1
        else:
            next_order_id = 1
        return f'O{next_order_id:03}'
        
    def insert_order(order_id, eta):
        
        # Function to insert values into the Orders table
        insert_orders_query = f"""
            INSERT INTO Orders(Order_ID, ETA)
            VALUES('{order_id}', '{eta}');
        """
        cursor.execute(insert_orders_query)
        connection.commit()
        
    current_date = datetime.datetime.now().date()
    eta = current_date + datetime.timedelta(days=5)
    eta_str = eta.strftime('%Y-%m-%d')
    order_id= get_next_order_id()
    insert_order(order_id,eta_str)
    
    message= "Thank you for shopping with us \nYour order will be delivered on,",eta_str,"\n\nPLEASE DO VISIT US AGAIN "
    msg = tk.Message(final, text = message)
    msg.config(bg='aqua', font=('times', 24, 'italic'))
    msg.pack()
    tk.mainloop()  
#input credit and debit card information
def debcred():
    masterss = tk.Tk()
    masterss.geometry("500x500+0+0")
    masterss.config(background="medium aquamarine")
    masterss.title("DEBIT OR CREDIT CARD")
    
    tk.Label(masterss,
             text="Card number",
             bg="medium aquamarine").grid(row=0)
    tk.Label(masterss,
             text="expiry date",
             bg="medium aquamarine").grid(row=1)
    tk.Label(masterss,
             text="cvv number",
             bg="medium aquamarine").grid(row=2)
    
    e1 = tk.Entry(masterss)
    e2 = tk.Entry(masterss)
    e3 = tk.Entry(masterss)
    
    e1.grid(row=0, column=1)
    e2.grid(row=1, column=1)
    e3.grid(row=2, column=1)
    
    go=tk.Button(masterss,
                 text="next",
                 highlightbackground="blue",
                 command=final)
    
    go.grid(row=3, column=1)

    masterss.mainloop()
#input gift card information
def giftcard():
    masters = tk.Tk()
    masters.geometry("500x500+0+0")
    masters.config(bg="medium aquamarine")
    masters.title("GIFT CARD")
    
    tk.Label(masters,
             text="voucher no./code").grid(row=0)
    
    e1 = tk.Entry(masters)
    e1.grid(row=0, column=1)
    
    go=tk.Button(masters,
                 text="next",
                 highlightbackground="blue",
                 command=final)
    
    go.grid(row=3, column=1)

    masters.mainloop()   
#methods for payment

def cart():
    user=tk.Tk()
    user.geometry("500x500+0+0")
    user.config(bg="light pink")
    user.title("CART")
    
    global add
    add=sum(l)
    print(l)
    print(add)
    print(dict)
    key=list(dict.keys())
    for i in key:
        size = dict[i][1].split(':')[-1].strip()
        read_query="insert into cart_items(itemname,price,size) values(%s,%s,%s)"
        values=(i,add,size)
        cursor.execute(read_query,values)
        connection.commit()
        print("cart item inserted")
    
    uggh= dict

    txt="Total amount to be paid=",add
    tk.Label(user,bg="light pink").pack()
    tk.Label(user,
             text=txt).pack()
    tk.Label(user,bg="light pink").pack()
    tk.Label(user,bg="light pink").pack()
    
    for key, value in dict.items():
        uggh=key,":",value
        ug = tk.Label(user,
                      text = uggh,
                      bg="aqua")  
        ug.config(bg='aqua',
                  font=('times', 24, 'italic'))
        ug.pack()
    tk.Label(user,bg="light pink").pack()
    tk.Label(user,bg="light pink").pack()
    buy=tk.Button(user,
                  text="proceed to buy now",
                  fg="dark blue",
                  command=payment).pack()

def pay_method():
    pm = tk.Tk()
    pm.geometry("500x500+0+0")
    pm.config(bg="RosyBrown1")
    pm.title("PAYMENT METHOD")
    
    v = tk.IntVar()
    tk.Label(pm, 
            text="payment method:-",
            justify = tk.LEFT,
            padx = 20).pack()
    
    def one():
        read_query="insert into payment_info(mode_of_payment,total) values(%s,%s)"
        values=("debit card",add)
        cursor.execute(read_query,values)
        connection.commit()
        print("payment method inserted")
        debcred()
    
    def two():
        read_query="insert into payment_info(mode_of_payment,total) values(%s,%s)"
        values=("credit card",add)
        cursor.execute(read_query,values)
        connection.commit()
        print("payment method inserted")
        debcred()
    
    def three():
        read_query="insert into payment_info(mode_of_payment,total) values(%s,%s)"
        values=("gift card",add)
        cursor.execute(read_query,values)
        connection.commit()
        print("payment method inserted")
        giftcard()
        
    def four():
        read_query="insert into payment_info(mode_of_payment,total) values(%s,%s)"
        values=("cash on delivery",add)
        cursor.execute(read_query,values)
        connection.commit()
        print("payment method inserted")
        final()
    
    pay = tk.Radiobutton(pm, 
                  text="debit card",
                  padx = 20, 
                  variable=v, 
                  value=1,
                  command=one).pack(anchor=tk.W)
    
    pay = tk.Radiobutton(pm, 
                  text="credit card",
                  padx = 20, 
                  variable=v, 
                  value=2,
                  command=two).pack(anchor=tk.W)
    
    pay = tk.Radiobutton(pm, 
                  text="gift card balance",
                  padx = 20, 
                  variable=v, 
                  value=3,
                  command=three).pack(anchor=tk.W)
    
    pay = tk.Radiobutton(pm, 
                  text="cash on delivery",
                  padx = 20, 
                  variable=v, 
                  value=4,
                  command=four).pack(anchor=tk.W)  

    root.mainloop()
#input payment information

def profile(name_entry, email_entry, mobile_entry, password_entry, address_entry):
    # Function to insert user details into the Users table
    user_id = name_entry.get()
    email = email_entry.get()
    mobile = mobile_entry.get()
    password = " "
    address = address_entry.get()

    insert_query = f"""
        INSERT INTO Users(User_ID, Email, Phone_Number, Password, Address)
        VALUES('{user_id}', '{email}', '{mobile}', '{password}', '{address}');
    """
    cursor.execute(insert_query)
    connection.commit()
    print("new user inserted")
    pay_method()

    
def payment():
    master = tk.Tk()
    master.geometry("500x500+0+0")
    master.config(bg="spring green")
    master.title("PLEASE ENTER YOUR DETAILS")
    
    a = sum(l)
    print(l)
    print(a)

    whatever = "Total amount to be paid:", a
    tk.Label(master, text=whatever).grid(row=0)
    
    tk.Label(master, text="name").grid(row=1)
    tk.Label(master, text="email").grid(row=2)  # Add email label
    tk.Label(master, text="mobile number").grid(row=3)  # Shifted down to make room for email
    tk.Label(master, text="address").grid(row=4)  # Shifted down to make room for email
    
    name = tk.Entry(master)
    email = tk.Entry(master)  # Add email entry
    mobile = tk.Entry(master)
    address = tk.Entry(master)
    
    name.grid(row=1, column=1)
    email.grid(row=2, column=1)  # Place email entry in the second column
    mobile.grid(row=3, column=1)
    address.grid(row=4, column=1)
    
    # Assuming an empty string for the password for simplicity
    go = tk.Button(master, text="next", highlightbackground="blue", command=lambda: profile(name, email, mobile, "", address))
    go.grid(row=5, column=1)
    
    master.mainloop()


# def payment():
#     master = tk.Tk()
#     master.geometry("500x500+0+0")
#     master.config(bg="spring green")
#     master.title("PLEASE ENTER YOUR DETAILS")
    
#     a=sum(l)
#     print(l)
#     print(a)
 
#     whatever="Total amount to be paid:",a
#     tk.Label(master,
#              text=whatever).grid(row=0)
    
#     tk.Label(master,
#              text="name").grid(row=1)
    
#     tk.Label(master,
#              text="mobile number").grid(row=2)
    
#     tk.Label(master,
#              text="address").grid(row=3)
    
#     name = tk.Entry(master)
#     mobile = tk.Entry(master)
#     address = tk.Entry(master)
    
#     name.grid(row=1, column=1)
#     mobile.grid(row=2, column=1)
#     address.grid(row=3, column=1)
    
#     profile(name," ",mobile," ",address)
    
    
#     go=tk.Button(master,
#                  text="next",
#                  highlightbackground="blue",
#                  command=pay_method)
    
#     go.grid(row=4, column=1)
#     master.mainloop()   
 
def categories(model,category,maincat,gender):
    read_query="insert into categories(category_id, sub_category, category, gender) values(%s,%s,%s,%s)"
    values=(model,category,maincat,gender)
    cursor.execute(read_query,values)
    connection.commit()
    print("new record inserted")   
    
def top1():
    
    
    
    choice4=tk.Toplevel()
    choice4.geometry("1000x1000+0+0")
    choice4.title("TOP 1")
    
    frame2=tk.Frame(choice4,height=400,width=500)
    frame2.config(background="misty rose")
    desc=tk.PhotoImage(file="top1adesc.gif")
    tk.Label(frame2,image=desc).pack()
    
    frame1=tk.Frame(choice4,height=900,width=500)
    frame1.config(background="misty rose")
    
    display1a=tk.PhotoImage(file="top1a.gif")
    
    tk.Label(frame1).pack()
    tk.Label(frame1,
             image=display1a).pack()
    
    tk.Label(frame1).pack()
    tk.Label(frame1,
             text="Rs.436\n").pack()
    tk.Label(frame1).pack()
    
    press1a=tk.Button(frame1,
                      text="Add to cart",
                      highlightbackground="yellow",
                      bg="snow",
                      command=insert).pack()
    tk.Label(frame1).pack()    
        
        
    press1aa=tk.Button(frame1,
                       text="GO to cart",
                       command=cart,
                       highlightbackground="yellow",
                       bg="snow").pack()
    
    def purchase(size):
        key="top1"
        value=[436,size]
        dict[key]=value
        l.append(value[0])
        
    tk.Label(frame1,text="Size:").pack(side="left")
    global size 
        
    size=tk.Button(frame1,
                  text="X small",
                  bg="snow",
                  command=lambda: purchase("  size: X small")).pack(padx=10,pady=5,side="left")
    
    size=tk.Button(frame1,
                    text="small",
                    bg="snow",
                    command=lambda: purchase("  size: small")).pack(padx=10,pady=10,side="left")
    size=tk.Button(frame1,
                    text="medium",
                    bg="snow",
                    command=lambda: purchase(" size: medium")).pack(padx=10,pady=15,side="left")
    size=tk.Button(frame1,
                    text="large",
                    bg="snow",
                    command=lambda: purchase(" size: large")).pack(padx=10,pady=20,side="left")
    size=tk.Button(frame1,
                   text="X large",
                   bg="snow",
                    command=lambda: purchase(" size: X large")).pack(padx=10,pady=25,side="left")
    size=tk.Button(frame1,
                   text="XX large",
                   bg="snow",
                    command=lambda: purchase(" size: XX large")).pack(padx=10,pady=25,side="left")
    
   
        
    global name
    global price
    global model
    global category
    global gender
    gender='F'
    name="top1"
    price="Rs.436"
    model="A001"
    category="tops"
    
    global maincat
    maincat="women western wear"
    
    categories(model,category,maincat,gender)
    
    frame3=tk.Frame(choice4,height=500,width=500)
    
    # query="SELECT * FROM products WHERE CATEGORY=%s"
    # value=category
    # cursor.execute(query,value)
    # connection.commit()
    # result=cursor.fetchall()
    
    # for i in range(len(result)):
    #     gl.append(result[i]['itemname'])

    
    # xaxis=["top1","top2","top3","top4","top5"]
    # strength=[gl.count("top1"),gl.count("top2"),gl.count("top3"),gl.count("top4"),gl.count("top5")]
    # fig = plt.figure(figsize =(10,7)) 
    # plt.pie(strength, labels = xaxis)
    # chart=FigureCanvasTkAgg(fig,frame3)
    # chart.get_tk_widget().pack()
    
    
    frame1.pack(fill="both",side="left")
    frame2.pack(fill="both",side="top")
    frame3.pack(fill="both",side="top")
    
    choice4.mainloop()
def top2():
    choice5=tk.Toplevel()
    choice5.geometry("1000x1000+0+0")
    choice5.title("TOP 2")
    
    frame2=tk.Frame(choice5,height=400,width=500)
    frame2.config(background="misty rose")
    
    desc=tk.PhotoImage(file="top2adesc.gif")
    tk.Label(frame2,image=desc).pack()
    
    frame1=tk.Frame(choice5,height=900,width=500)
    frame1.config(background="misty rose")
    
    display2a=tk.PhotoImage(file="top2a.gif")
    
    tk.Label(frame1).pack()
    tk.Label(frame1,
             image=display2a).pack()
    
    tk.Label(frame1).pack()
    tk.Label(frame1,
             text="Rs.650").pack()
    tk.Label(frame1).pack()
    
    press1a=tk.Button(frame1,
                    text="Add to cart",
                    highlightbackground="yellow",
                    bg="snow",
                    command=insert).pack()
    
    tk.Label(frame1).pack() 
    
    press2aa=tk.Button(frame1,
                    text="GO to cart",
                    command=cart,
                    highlightbackground="yellow",
                    bg="snow").pack()
    
    def purchase(size):
        key="top2"
        value=[650,size]
        dict[key]=value
        l.append(value[0])
    
    tk.Label(frame1,text="Size:").pack(side="left")
    global size 
    
    size=tk.Button(frame1,
                  text="X small",
                  bg="snow",
                  command=lambda: purchase("  size: X small")).pack(padx=10,pady=5,side="left")
    
    size=tk.Button(frame1,
                    text="small",
                    bg="snow",
                    command=lambda: purchase("  size: small")).pack(padx=10,pady=10,side="left")
    size=tk.Button(frame1,
                    text="medium",
                    bg="snow",
                    command=lambda: purchase(" size: medium")).pack(padx=10,pady=15,side="left")
    size=tk.Button(frame1,
                    text="large",
                    bg="snow",
                    command=lambda: purchase(" size: large")).pack(padx=10,pady=20,side="left")
    size=tk.Button(frame1,
                   text="X large",
                   bg="snow",
                    command=lambda: purchase(" size: X large")).pack(padx=10,pady=25,side="left")
    size=tk.Button(frame1,
                   text="XX large",
                   bg="snow",
                    command=lambda: purchase(" size: XX large")).pack(padx=10,pady=25,side="left")
    
    global name
    global price
    global model
    global category
    global gender
    gender='F'
    name="top2"
    price="Rs.650"
    model="A002"
    category="tops"
    
    global maincat
    maincat="women western wear"
    
    categories(model,category,maincat,gender)
    
    frame3=tk.Frame(choice5,height=500,width=500)
    
    # query="SELECT * FROM products WHERE CATEGORY=%s"
    # value=category
    # cursor.execute(query,value)
    # connection.commit()
    # result=cursor.fetchall()
    
    # for i in range(len(result)):
    #     gl.append(result[i]['itemname'])

    
    # xaxis=["top1","top2","top3","top4","top5"]
    # strength=[gl.count("top1"),gl.count("top2"),gl.count("top3"),gl.count("top4"),gl.count("top5")]
    # fig = plt.figure(figsize =(10,7)) 
    # plt.pie(strength, labels = xaxis)
    # chart=FigureCanvasTkAgg(fig,frame3)
    # chart.get_tk_widget().pack()
    
    
    frame1.pack(fill="both",side="left")
    frame2.pack(fill="both",side="top")
    frame3.pack(fill="both",side="top")
    
    choice5.mainloop()   
def top3():
    choice6=tk.Toplevel()
    choice6.geometry("1000x1000+0+0")
    choice6.title("TOP 3")
    
    frame2=tk.Frame(choice6,height=400,width=500)
    frame2.config(background="misty rose")
    
    desc=tk.PhotoImage(file="top3adesc.gif")
    tk.Label(frame2,image=desc).pack()
    
    frame1=tk.Frame(choice6,height=900,width=500)
    frame1.config(background="misty rose")
    
    
    display3a=tk.PhotoImage(file="top3a.gif")
    tk.Label(frame1).pack()
    
    tk.Label(frame1,
             image=display3a).pack()
    tk.Label(frame1).pack()
    tk.Label(frame1,
             text="Rs.780").pack()
    tk.Label(frame1).pack()
    
    press1a=tk.Button(frame1,
                    text="Add to cart",
                    highlightbackground="yellow",
                    command=insert,
                    bg="snow").pack()
    
    tk.Label(frame1).pack()
    
    press3aa=tk.Button(frame1,
                    text="GO to cart",
                    command=cart,
                    highlightbackground="yellow",
                    bg="snow").pack()
   
    def purchase(size):   
        key="top3"
        value=[780,size]
        dict[key]=value
        l.append(value[0])
        
    global size     
        
    size=tk.Button(frame1,
                  text="X small",
                  bg="snow",
                  command=lambda: purchase("  size: X small")).pack(padx=10,pady=5,side="left")
    
    size=tk.Button(frame1,
                    text="small",
                    bg="snow",
                    command=lambda: purchase("  size: small")).pack(padx=10,pady=10,side="left")
    size=tk.Button(frame1,
                    text="medium",
                    bg="snow",
                    command=lambda: purchase(" size: medium")).pack(padx=10,pady=15,side="left")
    size=tk.Button(frame1,
                    text="large",
                    bg="snow",
                    command=lambda: purchase(" size: large")).pack(padx=10,pady=20,side="left")
    size=tk.Button(frame1,
                   text="X large",
                   bg="snow",
                    command=lambda: purchase(" size: X large")).pack(padx=10,pady=25,side="left")
    size=tk.Button(frame1,
                   text="XX large",
                   bg="snow",
                    command=lambda: purchase(" size: XX large")).pack(padx=10,pady=25,side="left")
    
    
    global name
    global price
    global model
    global category
    global gender
    gender='F'
    name="top3"
    price="Rs.780"
    model="A003"
    category="tops"
    
    global maincat
    maincat="women western wear"
    
    categories(model,category,maincat,gender)
    
    frame3=tk.Frame(choice6,height=500,width=500)
    
    # query="SELECT * FROM products WHERE CATEGORY=%s"
    # value=category
    # cursor.execute(query,value)
    # connection.commit()
    # result=cursor.fetchall()
    
    # for i in range(len(result)):
    #     gl.append(result[i]['itemname'])

    
    # xaxis=["top1","top2","top3","top4","top5"]
    # strength=[gl.count("top1"),gl.count("top2"),gl.count("top3"),gl.count("top4"),gl.count("top5")]
    # fig = plt.figure(figsize =(10,7)) 
    # plt.pie(strength, labels = xaxis)
    # chart=FigureCanvasTkAgg(fig,frame3)
    # chart.get_tk_widget().pack()
    
    
    frame1.pack(fill="both",side="left")
    frame2.pack(fill="both",side="top")
    frame3.pack(fill="both",side="top")
    
    choice6.mainloop()
def top4():
    choice7=tk.Toplevel()
    choice7.geometry("1000x1000+0+0")
    choice7.title("TOP 4")
    
    frame2=tk.Frame(choice7,height=400,width=500)
    frame2.config(background="misty rose")
    
    desc=tk.PhotoImage(file="top4adesc.gif")
    tk.Label(frame2,image=desc).pack()
    
    frame1=tk.Frame(choice7,height=900,width=500)
    frame1.config(background="misty rose")
    
    display4a=tk.PhotoImage(file="top4a.gif")
    tk.Label(frame1).pack()
    tk.Label(frame1,
             image=display4a).pack()
    tk.Label(frame1).pack()
    tk.Label(frame1,
             text="Rs.800").pack()
    tk.Label(frame1).pack()
    
    press1a=tk.Button(frame1,
                    text="Add to cart",
                    highlightbackground="yellow",
                    command=insert,
                    bg="snow").pack()
    
    
    tk.Label(frame1).pack()
    press1aa=tk.Button(frame1,
                    text="GO to cart",
                    command=cart,
                    highlightbackground="yellow",
                    bg="snow").pack()
    
    def purchase(size):
        key="top4"
        value=[800,size]
        dict[key]=value
        l.append(value[0])
    
    tk.Label(frame1,text="Size:").pack(side="left")
    
    global size 
    
    size=tk.Button(frame1,
                  text="X small",
                  bg="snow",
                  command=lambda: purchase("  size: X small")).pack(padx=10,pady=5,side="left")
    
    size=tk.Button(frame1,
                    text="small",
                    bg="snow",
                    command=lambda: purchase("  size: small")).pack(padx=10,pady=10,side="left")
    size=tk.Button(frame1,
                    text="medium",
                    bg="snow",
                    command=lambda: purchase(" size: medium")).pack(padx=10,pady=15,side="left")
    size=tk.Button(frame1,
                    text="large",
                    bg="snow",
                    command=lambda: purchase(" size: large")).pack(padx=10,pady=20,side="left")
    size=tk.Button(frame1,
                   text="X large",
                   bg="snow",
                    command=lambda: purchase(" size: X large")).pack(padx=10,pady=25,side="left")
    size=tk.Button(frame1,
                   text="XX large",
                   bg="snow",
                    command=lambda: purchase(" size: XX large")).pack(padx=10,pady=25,side="left")
        
    global name
    global price
    global model
    global category
    global gender
    gender='F'
    name="top4"
    price="Rs.800"
    model="A004"
    category="tops"
    
    global maincat
    maincat="women western wear"
    
    categories(model,category,maincat,gender)
    
    frame3=tk.Frame(choice7,height=500,width=500)
    
    # query="SELECT * FROM products WHERE CATEGORY=%s"
    # value=category
    # cursor.execute(query,value)
    # connection.commit()
    # result=cursor.fetchall()
    
    # for i in range(len(result)):
    #     gl.append(result[i]['itemname'])

    
    # xaxis=["top1","top2","top3","top4","top5"]
    # strength=[gl.count("top1"),gl.count("top2"),gl.count("top3"),gl.count("top4"),gl.count("top5")]
    # fig = plt.figure(figsize =(10,7)) 
    # plt.pie(strength, labels = xaxis)
    # chart=FigureCanvasTkAgg(fig,frame3)
    # chart.get_tk_widget().pack()
    
    
    frame1.pack(fill="both",side="left")
    frame2.pack(fill="both",side="top")
    frame3.pack(fill="both",side="top")
    
    choice7.mainloop()    
def top5():
    choice8=tk.Toplevel()
    choice8.geometry("1000x1000+0+0")
    choice8.title("TOP 5")
    
    frame2=tk.Frame(choice8,height=400,width=500)
    frame2.config(background="misty rose")
    
    desc=tk.PhotoImage(file="top5adesc.gif")
    tk.Label(frame2,image=desc).pack()
    
    frame1=tk.Frame(choice8,height=900,width=500)
    frame1.config(background="misty rose")
    
    display5a=tk.PhotoImage(file="top5a.gif")
    tk.Label(frame1).pack()
    tk.Label(frame1,
             image=display5a).pack()
    tk.Label(frame1).pack()
    tk.Label(frame1,
             text="840").pack()
    
    tk.Label(frame1).pack()
    press1a=tk.Button(frame1,
                    text="Add to cart",
                    highlightbackground="yellow",
                    command=insert,bg="snow").pack()
    
    tk.Label(frame1).pack()
    
    press1aa=tk.Button(frame1,
                    text="GO to cart",
                    command=cart,
                    highlightbackground="yellow",
                    bg="snow").pack()
    
    def purchase(size):
        key="top5"
        value=[840,size]
        dict[key]=value
        l.append(value[0])
     
    tk.Label(frame1,text="Size:").pack(side="left")
      
      
    global size   
        
    size=tk.Button(frame1,
                  text="X small",
                  bg="snow",
                  command=lambda: purchase("  size: X small")).pack(padx=10,pady=5,side="left")
    
    size=tk.Button(frame1,
                    text="small",
                    bg="snow",
                    command=lambda: purchase("  size: small")).pack(padx=10,pady=10,side="left")
    size=tk.Button(frame1,
                    text="medium",
                    bg="snow",
                    command=lambda: purchase(" size: medium")).pack(padx=10,pady=15,side="left")
    size=tk.Button(frame1,
                    text="large",
                    bg="snow",
                    command=lambda: purchase(" size: large")).pack(padx=10,pady=20,side="left")
    size=tk.Button(frame1,
                   text="X large",
                   bg="snow",
                    command=lambda: purchase(" size: X large")).pack(padx=10,pady=25,side="left")
    size=tk.Button(frame1,
                   text="XX large",
                   bg="snow",
                    command=lambda: purchase(" size: XX large")).pack(padx=10,pady=25,side="left")
    
    global name
    global price
    global model
    global category
    global gender
    gender='F'
    name="top5"
    price="Rs.840"
    model="A005"
    category="tops"
    
    global maincat
    maincat="women western wear"
    
    categories(model,category,maincat,gender)
    
    frame3=tk.Frame(choice8,height=500,width=500)
    
    # query="SELECT * FROM products WHERE CATEGORY=%s"
    
    # value=category
    # cursor.execute(query,value)
    # connection.commit()
    # result=cursor.fetchall()
    
    # for i in range(len(result)):
    #     gl.append(result[i]['itemname'])

    
    # xaxis=["top1","top2","top3","top4","top5"]
    # strength=[gl.count("top1"),gl.count("top2"),gl.count("top3"),gl.count("top4"),gl.count("top5")]
    # fig = plt.figure(figsize =(10,7)) 
    # plt.pie(strength, labels = xaxis)
    # chart=FigureCanvasTkAgg(fig,frame3)
    # chart.get_tk_widget().pack()
    
    
    frame1.pack(fill="both",side="left")
    frame2.pack(fill="both",side="top")
    frame3.pack(fill="both",side="top")
    
    choice8.mainloop()      
def dress1():
    choice9=tk.Toplevel()
    choice9.geometry("1000x1000+0+0")
    choice9.title("DRESS 1")
    
    frame2=tk.Frame(choice9,height=400,width=500)
    frame2.config(background="misty rose")
    desc=tk.PhotoImage(file="dress1adesc.gif")
    tk.Label(frame2,image=desc).pack()
    
    frame1=tk.Frame(choice9,height=900,width=500)
    frame1.config(background="misty rose")
    
    
    displ1a=tk.PhotoImage(file="dress1a.gif")
    tk.Label(frame1).pack()
    tk.Label(frame1,
             image=displ1a).pack()
    tk.Label(frame1).pack()
    tk.Label(frame1,
             text="Rs.650").pack()
    
    tk.Label(frame1).pack()
    press1a=tk.Button(frame1,
                    text="Add to cart",
                    highlightbackground="yellow",
                    bg="snow",
                    command=insert).pack()
    tk.Label(frame1).pack()
    
    press1aa=tk.Button(frame1,
                    text="GO to cart",
                    command=cart,
                    highlightbackground="yellow",
                    bg="snow").pack()
    
    def purchase(size):
        key="dress1"
        value=[650,size]
        dict[key]=value
        l.append(value[0])
        
    tk.Label(frame1,text="Size:").pack(side="left")
    
    global size 
        
    size=tk.Button(frame1,
                  text="X small",
                  bg="snow",
                  command=lambda: purchase("  size: X small")).pack(padx=10,pady=5,side="left")
    
    size=tk.Button(frame1,
                    text="small",
                    bg="snow",
                    command=lambda: purchase("  size: small")).pack(padx=10,pady=10,side="left")
    size=tk.Button(frame1,
                    text="medium",
                    bg="snow",
                    command=lambda: purchase(" size: medium")).pack(padx=10,pady=15,side="left")
    size=tk.Button(frame1,
                    text="large",
                    bg="snow",
                    command=lambda: purchase(" size: large")).pack(padx=10,pady=20,side="left")
    size=tk.Button(frame1,
                   text="X large",
                   bg="snow",
                    command=lambda: purchase(" size: X large")).pack(padx=10,pady=25,side="left")
    size=tk.Button(frame1,
                   text="XX large",
                   bg="snow",
                    command=lambda: purchase(" size: XX large")).pack(padx=10,pady=25,side="left")
    
    global name
    global price
    global model
    global category
    global gender
    gender='F'
    name="dress1"
    price="Rs.650"
    model="B001"
    category="dresses"
    
    global maincat
    maincat="women western wear"
    
    categories(model,category,maincat,gender)
    
    frame3=tk.Frame(choice9,height=500,width=500)
    
    # query="SELECT * FROM products WHERE CATEGORY=%s"

    # value=category
    # cursor.execute(query,value)
    # connection.commit()
    # result=cursor.fetchall()
    
    # for i in range(len(result)):
    #     gl.append(result[i]['itemname'])

    
    # xaxis=["dress1","dress2","dress3","dress4"]
    # strength=[gl.count("dress1"),gl.count("dress2"),gl.count("dress3"),gl.count("dress4")]
    # fig = plt.figure(figsize =(10,7)) 
    # plt.pie(strength, labels = xaxis)
    # chart=FigureCanvasTkAgg(fig,frame3)
    # chart.get_tk_widget().pack()
    
    
    frame1.pack(fill="both",side="left")
    frame2.pack(fill="both",side="top")
    frame3.pack(fill="both",side="top")
    
    
    
    choice9.mainloop()       
def dress2():
    choice10=tk.Toplevel()
    choice10.geometry("1000x1009+0+0")
    choice10.title("DRESS 2")
    
    frame2=tk.Frame(choice10,height=400,width=500)
    frame2.config(background="misty rose")
    desc=tk.PhotoImage(file="dress2adesc.gif")
    tk.Label(frame2,image=desc).pack()
    
    frame1=tk.Frame(choice10,height=900,width=500)
    frame1.config(background="misty rose")
    
    
    displ2a=tk.PhotoImage(file="dress2a.gif")
    tk.Label(frame1,
             image=displ2a).pack()
    
    tk.Label(frame1,
             text="Rs.800").pack()
    tk.Label(frame1).pack()
    
    press1a=tk.Button(frame1,
                    text="Add to cart",
                    highlightbackground="yellow",
                    command=insert,
                    bg="snow").pack()
    
    tk.Label(frame1).pack()
    
    press1aa=tk.Button(frame1,
                    text="GO to cart",
                    command=cart,
                    highlightbackground="yellow",
                    bg="snow").pack()
    
    def purchase(size):
        key="dress2"
        value=[800,size]
        dict[key]=value
        l.append(value[0])
        
    tk.Label(frame1,text="Size:").pack(side="left")
    
    global size 
        
    size=tk.Button(frame1,
                  text="X small",
                  bg="snow",
                  command=lambda: purchase("  size: X small")).pack(padx=10,pady=5,side="left")
    
    size=tk.Button(frame1,
                    text="small",
                    bg="snow",
                    command=lambda: purchase("  size: small")).pack(padx=10,pady=10,side="left")
    size=tk.Button(frame1,
                    text="medium",
                    bg="snow",
                    command=lambda: purchase(" size: medium")).pack(padx=10,pady=15,side="left")
    size=tk.Button(frame1,
                    text="large",
                    bg="snow",
                    command=lambda: purchase(" size: large")).pack(padx=10,pady=20,side="left")
    size=tk.Button(frame1,
                   text="X large",
                   bg="snow",
                    command=lambda: purchase(" size: X large")).pack(padx=10,pady=25,side="left")
    size=tk.Button(frame1,
                   text="XX large",
                   bg="snow",
                    command=lambda: purchase(" size: XX large")).pack(padx=10,pady=25,side="left")
    
    global name
    global price
    global model
    global category
    global gender
    gender='F'
    name="dress2"
    price="Rs.800"
    model="B001"
    category="dresses"
    
    global maincat
    maincat="women western wear"
    
    categories(model,category,maincat,gender)
    
    frame3=tk.Frame(choice10,height=500,width=500)
    
    # query="SELECT * FROM products WHERE CATEGORY=%s"
    # value=category
    # cursor.execute(query,value)
    # connection.commit()
    # result=cursor.fetchall()
    
    # for i in range(len(result)):
    #     gl.append(result[i]['itemname'])

    
    # xaxis=["dress1","dress2","dress3","dress4"]
    # strength=[gl.count("dress1"),gl.count("dress2"),gl.count("dress3"),gl.count("dress4")]
    # fig = plt.figure(figsize =(10,7)) 
    # plt.pie(strength, labels = xaxis)
    # chart=FigureCanvasTkAgg(fig,frame3)
    # chart.get_tk_widget().pack()
    
    
    frame1.pack(fill="both",side="left")
    frame2.pack(fill="both",side="top")
    frame3.pack(fill="both",side="top")
    

    choice10.mainloop()   
def dress3():
    choice11=tk.Toplevel()
    choice11.geometry("1000x1000+0+0")
    choice11.title("DRESS 3")
    
    frame2=tk.Frame(choice11,height=400,width=500)
    frame2.config(background="misty rose")
    desc=tk.PhotoImage(file="dress3adesc.gif")
    tk.Label(frame2,image=desc).pack()
    
    frame1=tk.Frame(choice11,height=900,width=500)
    frame1.config(background="misty rose")
    
    
    displ3a=tk.PhotoImage(file="dress3a.gif")
    tk.Label(frame1).pack()
    tk.Label(frame1,
             image=displ3a).pack()
    tk.Label(frame1).pack()
    tk.Label(frame1,
             text="Rs.1050").pack()
    tk.Label(frame1).pack()
    
    press3a=tk.Button(frame1,
                    text="Add to cart",
                    highlightbackground="yellow",
                    command=insert,
                    bg="snow").pack()
    
    tk.Label(frame1).pack()
    press1aa=tk.Button(frame1,
                    text="GO to cart",
                    command=cart,
                    highlightbackground="yellow",
                    bg="snow").pack()
    
    def purchase(size):
        key="dress 3"
        value=[1050,size]
        dict[key]=value
        l.append(value[0])
        
    tk.Label(frame1,text="Size:").pack(side="left")
    
    global size 
        
    size=tk.Button(frame1,
                  text="X small",
                  bg="snow",
                  command=lambda: purchase("  size: X small")).pack(padx=10,pady=5,side="left")
    
    size=tk.Button(frame1,
                    text="small",
                    bg="snow",
                    command=lambda: purchase("  size: small")).pack(padx=10,pady=10,side="left")
    size=tk.Button(frame1,
                    text="medium",
                    bg="snow",
                    command=lambda: purchase(" size: medium")).pack(padx=10,pady=15,side="left")
    size=tk.Button(frame1,
                    text="large",
                    bg="snow",
                    command=lambda: purchase(" size: large")).pack(padx=10,pady=20,side="left")
    size=tk.Button(frame1,
                   text="X large",
                   bg="snow",
                    command=lambda: purchase(" size: X large")).pack(padx=10,pady=25,side="left")
    size=tk.Button(frame1,
                   text="XX large",
                   bg="snow",
                    command=lambda: purchase(" size: XX large")).pack(padx=10,pady=25,side="left")
    
    global name
    global price
    global model
    global category
    global gender
    gender='F'
    name="dress3"
    price="Rs.1050"
    model="B003"
    category="dresses"
   
    global maincat
    maincat="women western wear"
    
    categories(model,category,maincat,gender)
    
    frame3=tk.Frame(choice11,height=500,width=500)
    
    # query="SELECT * FROM products WHERE CATEGORY=%s"
    # value=category
    # cursor.execute(query,value)
    # connection.commit()
    # result=cursor.fetchall()
    
    # for i in range(len(result)):
    #     gl.append(result[i]['itemname'])

    
    # xaxis=["dress1","dress2","dress3","dress4"]
    # strength=[gl.count("dress1"),gl.count("dress2"),gl.count("dress3"),gl.count("dress4")]
    # fig = plt.figure(figsize =(10,7)) 
    # plt.pie(strength, labels = xaxis)
    # chart=FigureCanvasTkAgg(fig,frame3)
    # chart.get_tk_widget().pack()
    
    
    frame1.pack(fill="both",side="left")
    frame2.pack(fill="both",side="top")
    frame3.pack(fill="both",side="top")
    
    choice11.mainloop()   
def dress4():
    choice12=tk.Toplevel()
    choice12.geometry("1000x1000+0+0")
    choice12.title("DRESS 4")
    
    frame2=tk.Frame(choice12,height=400,width=500)
    frame2.config(background="misty rose")
    desc=tk.PhotoImage(file="dress4adesc.gif")
    tk.Label(frame2,image=desc).pack()
    
    frame1=tk.Frame(choice12,height=900,width=500)
    frame1.config(background="misty rose")
    
    
    displ4a=tk.PhotoImage(file="dress4a.gif")
    tk.Label(frame1).pack()
    tk.Label(frame1,
             image=displ4a).pack()
    tk.Label(frame1).pack()
    tk.Label(frame1,
             text="Rs.2100").pack()
    tk.Label(frame1).pack()
    
    
    press4a=tk.Button(frame1,
                    text="Add to cart",
                    highlightbackground="yellow",
                    command=insert,
                    bg="snow").pack()
    tk.Label(frame1).pack()
   
    
    press1aa=tk.Button(frame1,
                    text="GO to cart",
                    command=cart,
                    highlightbackground="yellow",
                    bg="snow").pack()
    
    def purchase(size):
        key="dress 4"
        value=[2100,size]
        dict[key]=value
        l.append(value[0])
        
    tk.Label(frame1,text="Size:").pack(side="left")
    
    global size 
        
    size=tk.Button(frame1,
                  text="X small",
                  bg="snow",
                  command=lambda: purchase("  size: X small")).pack(padx=10,pady=5,side="left")
    
    size=tk.Button(frame1,
                    text="small",
                    bg="snow",
                    command=lambda: purchase("  size: small")).pack(padx=10,pady=10,side="left")
    size=tk.Button(frame1,
                    text="medium",
                    bg="snow",
                    command=lambda: purchase(" size: medium")).pack(padx=10,pady=15,side="left")
    size=tk.Button(frame1,
                    text="large",
                    bg="snow",
                    command=lambda: purchase(" size: large")).pack(padx=10,pady=20,side="left")
    size=tk.Button(frame1,
                   text="X large",
                   bg="snow",
                    command=lambda: purchase(" size: X large")).pack(padx=10,pady=25,side="left")
    size=tk.Button(frame1,
                   text="XX large",
                   bg="snow",
                    command=lambda: purchase(" size: XX large")).pack(padx=10,pady=25,side="left")
    
    global name
    global price
    global model
    global category
    global gender
    gender='F'
    name="dress4"
    price="Rs.2100"
    model="B004"
    category="dresses"
    
    global maincat
    maincat="women western wear"
    
    categories(model,category,maincat,gender)
    
    frame3=tk.Frame(choice12,height=500,width=500)
    
    # query="SELECT * FROM products WHERE CATEGORY=%s"
    # value=category
    # cursor.execute(query,value)
    # connection.commit()
    # result=cursor.fetchall()
    
    # for i in range(len(result)):
    #     gl.append(result[i]['itemname'])

    
    # xaxis=["dress1","dress2","dress3","dress4"]
    # strength=[gl.count("dress1"),gl.count("dress2"),gl.count("dress3"),gl.count("dress4")]
    # fig = plt.figure(figsize =(10,7)) 
    # plt.pie(strength, labels = xaxis)
    # chart=FigureCanvasTkAgg(fig,frame3)
    # chart.get_tk_widget().pack()
    
    
    frame1.pack(fill="both",side="left")
    frame2.pack(fill="both",side="top")
    frame3.pack(fill="both",side="top")
    
    
    choice12.mainloop() 
def jeans1():
    choice15=tk.Toplevel()
    choice15.geometry("1000x1000+0+0")
    choice15.title("JEANS 1")
    
    frame2=tk.Frame(choice15,height=400,width=500)
    frame2.config(background="misty rose")
    desc=tk.PhotoImage(file="jeans1adesc.gif")
    tk.Label(frame2,image=desc).pack()
    
    frame1=tk.Frame(choice15,height=900,width=500)
    frame1.config(background="misty rose")
    
    d1a=tk.PhotoImage(file="jeans1a.gif")
    
    tk.Label(frame1).pack()
    tk.Label(frame1,
             image=d1a).pack()
    tk.Label(frame1).pack()
    tk.Label(frame1,
             text="Rs.1050").pack()
    tk.Label(frame1).pack()
    
    press1aj=tk.Button(frame1,
                    text="Add to cart",
                    highlightbackground="yellow",
                    command=insert,
                    bg="snow").pack()
    
    tk.Label(frame1).pack()
    press1aa=tk.Button(frame1,
                    text="GO to cart",
                    command=cart,
                    highlightbackground="yellow",
                    bg="snow").pack()
    
    def purchase(size):
        key="jeans 1"
        value=[1050,size]
        dict[key]=value
        l.append(value[0])
        
    tk.Label(frame1,text="Size:").pack(side="left")
        
    global size 
    
    size=tk.Button(frame1,
                  text="X small",
                  bg="snow",
                  command=lambda: purchase("  size: X small")).pack(padx=10,pady=5,side="left")
    
    size=tk.Button(frame1,
                    text="small",
                    bg="snow",
                    command=lambda: purchase("  size: small")).pack(padx=10,pady=10,side="left")
    size=tk.Button(frame1,
                    text="medium",
                    bg="snow",
                    command=lambda: purchase(" size: medium")).pack(padx=10,pady=15,side="left")
    size=tk.Button(frame1,
                    text="large",
                    bg="snow",
                    command=lambda: purchase(" size: large")).pack(padx=10,pady=20,side="left")
    size=tk.Button(frame1,
                   text="X large",
                   bg="snow",
                    command=lambda: purchase(" size: X large")).pack(padx=10,pady=25,side="left")
    size=tk.Button(frame1,
                   text="XX large",
                   bg="snow",
                    command=lambda: purchase(" size: XX large")).pack(padx=10,pady=25,side="left")
    
    global name
    global price
    global model
    global category
    global gender
    gender='F'
    name="jeans1"
    price="Rs.1050"
    model="C001"
    category="jeans"
    
    global maincat
    maincat="women western wear"
    
    categories(model,category,maincat,gender)
    
    frame3=tk.Frame(choice15,height=500,width=500)
    
    # query="SELECT * FROM products WHERE CATEGORY=%s"
    # value=category
    # cursor.execute(query,value)
    # connection.commit()
    # result=cursor.fetchall()
    
    # for i in range(len(result)):
    #     gl.append(result[i]['itemname'])

    
    # xaxis=["jeans1","jeans2","jeans3","jeans4"]
    # strength=[gl.count("jeans1"),gl.count("jeans2"),gl.count("jeans3"),gl.count("jeans4")]
    # fig = plt.figure(figsize =(10,7)) 
    # plt.pie(strength, labels = xaxis)
    # chart=FigureCanvasTkAgg(fig,frame3)
    # chart.get_tk_widget().pack()
    
    
    frame1.pack(fill="both",side="left")
    frame2.pack(fill="both",side="top")
    frame3.pack(fill="both",side="top")
    
    
    choice15.mainloop() 
def jeans2():
    choice16=tk.Toplevel()
    choice16.geometry("1000x1000+0+0")
    choice16.title("JEANS 2")
    
    frame2=tk.Frame(choice16,height=400,width=500)
    frame2.config(background="misty rose")
    desc=tk.PhotoImage(file="jeans2adesc.gif")
    tk.Label(frame2,image=desc).pack()
    
    frame1=tk.Frame(choice16,height=900,width=500)
    frame1.config(background="misty rose")
    
    
    d2a=tk.PhotoImage(file="jeans2a.gif")
    tk.Label(frame1).pack()
    tk.Label(frame1,
             image=d2a).pack()
    tk.Label(frame1).pack()
    tk.Label(frame1,
             text="Rs.980").pack()
    tk.Label(frame1).pack()
    
    press2aj=tk.Button(frame1,
                    text="Add to cart",
                    highlightbackground="yellow",
                    command=insert,
                    bg="snow").pack()
    
   
    tk.Label(frame1).pack()
    press1aa=tk.Button(frame1,
                    text="GO to cart",
                    command=cart,
                    highlightbackground="yellow",
                    bg="snow").pack()
    
    def purchase(size):
        key="jeans 2"
        value=[980,size]
        dict[key]=value
        l.append(value[0])
        
    tk.Label(frame1,text="Size:").pack(side="left")
        
    global size 
    
    size=tk.Button(frame1,
                  text="X small",
                  bg="snow",
                  command=lambda: purchase("  size: X small")).pack(padx=10,pady=5,side="left")
    
    size=tk.Button(frame1,
                    text="small",
                    bg="snow",
                    command=lambda: purchase("  size: small")).pack(padx=10,pady=10,side="left")
    size=tk.Button(frame1,
                    text="medium",
                    bg="snow",
                    command=lambda: purchase(" size: medium")).pack(padx=10,pady=15,side="left")
    size=tk.Button(frame1,
                    text="large",
                    bg="snow",
                    command=lambda: purchase(" size: large")).pack(padx=10,pady=20,side="left")
    size=tk.Button(frame1,
                   text="X large",
                   bg="snow",
                    command=lambda: purchase(" size: X large")).pack(padx=10,pady=25,side="left")
    size=tk.Button(frame1,
                   text="XX large",
                   bg="snow",
                    command=lambda: purchase(" size: XX large")).pack(padx=10,pady=25,side="left")
    
    global name
    global price
    global model
    global category
    global gender
    gender='F'
    name="jeans2"
    price="Rs.980"
    model="C002"
    category="jeans"
    
    global maincat
    maincat="women western wear"
    
    categories(model,category,maincat,gender)
    
    frame3=tk.Frame(choice16,height=500,width=500)
    
    # query="SELECT * FROM products WHERE CATEGORY=%s"
    # value=category
    # cursor.execute(query,value)
    # connection.commit()
    # result=cursor.fetchall()
    
    # for i in range(len(result)):
    #     gl.append(result[i]['itemname'])

    
    # xaxis=["jeans1","jeans2","jeans3","jeans4"]
    # strength=[gl.count("jeans1"),gl.count("jeans2"),gl.count("jeans3"),gl.count("jeans4")]
    # fig = plt.figure(figsize =(10,7)) 
    # plt.pie(strength, labels = xaxis)
    # chart=FigureCanvasTkAgg(fig,frame3)
    # chart.get_tk_widget().pack()
    
    
    frame1.pack(fill="both",side="left")
    frame2.pack(fill="both",side="top")
    frame3.pack(fill="both",side="top")
    
    choice16.mainloop()    
def jeans3():
    choice17=tk.Toplevel()
    choice17.geometry("1000x1000+0+0")
    choice17.title("JEANS 3")
    
    frame2=tk.Frame(choice17,height=400,width=500)
    frame2.config(background="misty rose")
    desc=tk.PhotoImage(file="jeans3adesc.gif")
    tk.Label(frame2,image=desc).pack()
    
    frame1=tk.Frame(choice17,height=900,width=500)
    frame1.config(background="misty rose")
    
    
    d3a=tk.PhotoImage(file="jeans3a.gif")
    
    tk.Label(frame1).pack()
    tk.Label(frame1,
             image=d3a).pack()
    tk.Label(frame1).pack()
    tk.Label(frame1,
             text="Rs.760").pack()
    tk.Label(frame1).pack()
    
    
    press3aj=tk.Button(frame1,
                    text="Add to cart",
                    highlightbackground="yellow",
                    command=insert,
                    bg="snow").pack()
    
    tk.Label(frame1).pack()
    
    press1aa=tk.Button(frame1,
                    text="GO to cart",
                    command=cart,
                    highlightbackground="yellow",
                    bg="snow").pack()
    
    def purchase(size):
        key="jeans 3"
        value=[760,size]
        dict[key]=value
        l.append(value[0])
        
    tk.Label(frame1,text="Size:").pack(side="left")
        
    global size 
    
    size=tk.Button(frame1,
                  text="X small",
                  bg="snow",
                  command=lambda: purchase("  size: X small")).pack(padx=10,pady=5,side="left")
    
    size=tk.Button(frame1,
                    text="small",
                    bg="snow",
                    command=lambda: purchase("  size: small")).pack(padx=10,pady=10,side="left")
    size1=tk.Button(frame1,
                    text="medium",
                    bg="snow",
                    command=lambda: purchase(" size: medium")).pack(padx=10,pady=15,side="left")
    size2=tk.Button(frame1,
                    text="large",
                    bg="snow",
                    command=lambda: purchase(" size: large")).pack(padx=10,pady=20,side="left")
    size3=tk.Button(frame1,
                   text="X large",
                   bg="snow",
                    command=lambda: purchase(" size: X large")).pack(padx=10,pady=25,side="left")
    size4=tk.Button(frame1,
                   text="XX large",
                   bg="snow",
                    command=lambda: purchase(" size: XX large")).pack(padx=10,pady=25,side="left")
    
    
    global name
    global price
    global model
    global category
    global gender
    gender='F'
    name="jeans3"
    price="Rs.760"
    model="C003"
    category="jeans"
    
    global maincat
    maincat="women western wear"
    
    categories(model,category,maincat,gender)
    
    frame3=tk.Frame(choice17,height=500,width=500)
    
    # query="SELECT * FROM products WHERE CATEGORY=%s"
    # value=category
    # cursor.execute(query,value)
    # connection.commit()
    # result=cursor.fetchall()
    
    # for i in range(len(result)):
    #     gl.append(result[i]['itemname'])

    
    # xaxis=["jeans1","jeans2","jeans3","jeans4"]
    # strength=[gl.count("jeans1"),gl.count("jeans2"),gl.count("jeans3"),gl.count("jeans4")]
    # fig = plt.figure(figsize =(10,7)) 
    # plt.pie(strength, labels = xaxis)
    # chart=FigureCanvasTkAgg(fig,frame3)
    # chart.get_tk_widget().pack()
    
    
    frame1.pack(fill="both",side="left")
    frame2.pack(fill="both",side="top")
    frame3.pack(fill="both",side="top")
    
    choice17.mainloop()    
def jeans4():
    choice19=tk.Toplevel()
    choice19.geometry("1000x1000+0+0")
    choice19.title("JEANS 4")
    
    frame2=tk.Frame(choice19,height=400,width=500)
    frame2.config(background="misty rose")
    desc=tk.PhotoImage(file="jeans4adesc.gif")
    tk.Label(frame2,image=desc).pack()
    
    frame1=tk.Frame(choice19,height=900,width=500)
    frame1.config(background="misty rose")
    
    
    d5a=tk.PhotoImage(file="jeans5a.gif")
    tk.Label(frame1).pack()
    tk.Label(frame1,
             image=d5a).pack()
    tk.Label(frame1).pack()
    tk.Label(frame1,
             text="Rs.670").pack()
    tk.Label(frame1).pack()
    
    
    press5aj=tk.Button(frame1,
                    text="Add to cart",
                    highlightbackground="yellow",
                    command=insert,
                    bg="snow").pack()
    
    tk.Label(frame1).pack()
    
    press1aa=tk.Button(frame1,
                    text="GO to cart",
                    command=cart,
                    highlightbackground="yellow",
                    bg="snow").pack()
    
    def purchase(size):
        key="jeans 4"
        value=[670,size]
        dict[key]=value
        l.append(value[0])
        
    tk.Label(frame1,text="Size:").pack(side="left")
        
    global size 
    
    size=tk.Button(frame1,
                  text="X small",
                  bg="snow",
                  command=lambda: purchase("  size: X small")).pack(padx=10,pady=5,side="left")
    
    size=tk.Button(frame1,
                    text="small",
                    bg="snow",
                    command=lambda: purchase("  size: small")).pack(padx=10,pady=10,side="left")
    size=tk.Button(frame1,
                    text="medium",
                    bg="snow",
                    command=lambda: purchase(" size: medium")).pack(padx=10,pady=15,side="left")
    size=tk.Button(frame1,
                    text="large",
                    bg="snow",
                    command=lambda: purchase(" size: large")).pack(padx=10,pady=20,side="left")
    size=tk.Button(frame1,
                   text="X large",
                   bg="snow",
                    command=lambda: purchase(" size: X large")).pack(padx=10,pady=25,side="left")
    size=tk.Button(frame1,
                   text="XX large",
                   bg="snow",
                    command=lambda: purchase(" size: XX large")).pack(padx=10,pady=25,side="left")
    
    global name
    global price
    global model
    global category
    global gender
    gender='F'
    name="jeans4"
    price="Rs.670"
    model="C004"
    category="jeans"
    
    global maincat
    maincat="women western wear"
    
    categories(model,category,maincat,gender)
    
    frame3=tk.Frame(choice19,height=500,width=500)
    
    # query="SELECT * FROM products WHERE CATEGORY=%s"
    # value=category
    # cursor.execute(query,value)
    # connection.commit()
    # result=cursor.fetchall()
    
    # for i in range(len(result)):
    #     gl.append(result[i]['itemname'])

    
    # xaxis=["jeans1","jeans2","jeans3","jeans4"]
    # strength=[gl.count("jeans1"),gl.count("jeans2"),gl.count("jeans3"),gl.count("jeans4")]
    # fig = plt.figure(figsize =(10,7)) 
    # plt.pie(strength, labels = xaxis)
    # chart=FigureCanvasTkAgg(fig,frame3)
    # chart.get_tk_widget().pack()
    
    
    frame1.pack(fill="both",side="left")
    frame2.pack(fill="both",side="top")
    frame3.pack(fill="both",side="top")
    
    
    choice19.mainloop()
def tops():
    choice=tk.Toplevel()
    choice.geometry("1700x800+0+0")
    choice.config(background="seashell3")
    choice.title("TOPS,TEES AND SWEATSHIRTS")
    frame1=tk.Frame(choice,height=400,width=850)
    frame2=tk.Frame(choice,height=400,width=850)
    
    disp=tk.PhotoImage(file="top1a.gif")
    btop=tk.Button(frame1,
                text="top1",
                image=disp,
                compound="top",
                command=top1).pack(side="left")
    
    disp1=tk.PhotoImage(file="top2a.gif")
    btop1=tk.Button(frame1,
                text="top2",
                image=disp1,
                compound="top",
                command=top2).pack(side="left")
    
    disp2=tk.PhotoImage(file="top3a.gif")
    btop2=tk.Button(frame1,
                text="top3",
                image=disp2,
                compound="top",
                command=top3).pack(side="left")
    
    disp3=tk.PhotoImage(file="top4a.gif")
    btop3=tk.Button(frame2,
                text="top4",
                image=disp3,
                compound="top",
                command=top4).pack(side="left")
    
    disp4=tk.PhotoImage(file="top5a.gif")
    btop4=tk.Button(frame2,
                text="top5",
                image=disp4,
                compound="top",
                command=top5).pack(side="left")
    
    frame1.pack(side="top",padx=200)
    frame2.pack(side="top",padx=400)
    
    choice.mainloop()
def dresses():
    choice2=tk.Toplevel()
    choice2.geometry("1700x800+0+0")
    choice2.config(background="seashell3")
    choice2.title("DRESSES AND GOWNS")
    
    m=tk.PhotoImage(file="dresscaption.gif")
    tk.Label(choice2,
             image=m).pack(side=tk.TOP)
    
    dispa=tk.PhotoImage(file="dress1a.gif")
    btopa=tk.Button(choice2,
                text="dress1",
                image=dispa,
                compound="top",
                command=dress1).pack(side=tk.LEFT)
    
    dispb=tk.PhotoImage(file="dress2a.gif")
    btopb=tk.Button(choice2,
                text="dress2",
                image=dispb,
                compound="top",
                command=dress2).pack(side=tk.LEFT)
    
    dispc=tk.PhotoImage(file="dress3a.gif")
    btopc=tk.Button(choice2,
                text="dress3",
                image=dispc,
                compound="top",
                command=dress3).pack(side=tk.LEFT)
    
    dispd=tk.PhotoImage(file="dress4a.gif")
    btopd=tk.Button(choice2,
                text="dress4",
                image=dispd,
                compound="top",
                command=dress4).pack(side=tk.LEFT)
    
    
    choice2.mainloop()
def jeans():
    choice3=tk.Toplevel()
    choice3.geometry("1700x800")
    choice3.config(background="seashell3")
    choice3.title("DENIMS AND TROUSERS")
    
    m=tk.PhotoImage(file="jeanscaption.gif")
    tk.Label(choice3,
             image=m).pack(side=tk.TOP)
    
    disp6=tk.PhotoImage(file="jeans1a.gif")
    btop6=tk.Button(choice3,
                text="jeans 1",
                image=disp6,
                compound="top",
                command=jeans1).pack(side=tk.LEFT)
    
    disp7=tk.PhotoImage(file="jeans2a.gif")
    btop7=tk.Button(choice3,
                text="jeans2",
                image=disp7,
                compound="top",
                command=jeans2).pack(side=tk.LEFT)
    
    disp8=tk.PhotoImage(file="jeans3a.gif")
    btop8=tk.Button(choice3,
                text="jeans3",
                image=disp8,
                compound="top",
                command=jeans3).pack(side=tk.LEFT)
    
    disp10=tk.PhotoImage(file="jeans5a.gif")
    btop10=tk.Button(choice3,
                text="jeans4",
                image=disp10,
                compound="top",
                command=jeans4).pack(side=tk.LEFT)
    choice3.mainloop()
def kurta1():
    k=tk.Toplevel()
    k.geometry("1000x1000+0+0")
    k.title("KURTA 1")
    
    frame2=tk.Frame(k,height=400,width=500)
    frame2.config(background="misty rose")
    desc=tk.PhotoImage(file="kurta1desc.gif")
    tk.Label(frame2,image=desc).pack()
    
    frame1=tk.Frame(k,height=900,width=500)
    frame1.config(background="misty rose")
    
    
    k1=tk.PhotoImage(file="kurta1.gif")
    
    tk.Label(frame1).pack()
    tk.Label(frame1,
             image=k1).pack()
    
    tk.Label(frame1).pack()
    tk.Label(frame1,
             text="Rs.770").pack()
    tk.Label(frame1).pack()
    
    b1k=tk.Button(frame1,
                  text="Add to cart",
                  highlightbackground="yellow",
                  command=insert,
                  bg="snow").pack()
    
    tk.Label(frame1).pack()
    press1aa=tk.Button(frame1,
                    text="GO to cart",
                    command=cart,
                    highlightbackground="yellow",
                    bg="snow").pack()
    
    def purchase(size):
        key="kurta 1"
        value=[770,size]
        dict[key]=value
        l.append(value[0])
        
    tk.Label(frame1,text="Size:").pack(side="left")
        
    global size 
    
    size=tk.Button(frame1,
                  text="X small",
                  bg="snow",
                  command=lambda: purchase("  size: X small")).pack(padx=10,pady=5,side="left")
    
    size=tk.Button(frame1,
                    text="small",
                    bg="snow",
                    command=lambda: purchase("  size: small")).pack(padx=10,pady=10,side="left")
    size=tk.Button(frame1,
                    text="medium",
                    bg="snow",
                    command=lambda: purchase(" size: medium")).pack(padx=10,pady=15,side="left")
    size=tk.Button(frame1,
                    text="large",
                    bg="snow",
                    command=lambda: purchase(" size: large")).pack(padx=10,pady=20,side="left")
    size=tk.Button(frame1,
                   text="X large",
                   bg="snow",
                    command=lambda: purchase(" size: X large")).pack(padx=10,pady=25,side="left")
    size=tk.Button(frame1,
                   text="XX large",
                   bg="snow",
                    command=lambda: purchase(" size: XX large")).pack(padx=10,pady=25,side="left")
    
    global name
    global price
    global model
    global category
    global gender
    gender='F'
    name="kurta1"
    price="Rs.770"
    model="D001"
    category="kurtas"
    
    global maincat
    maincat="women ethnic wear"
    
    categories(model,category,maincat,gender)
    
    frame3=tk.Frame(k,height=500,width=500)
    
    # query="SELECT * FROM products WHERE CATEGORY=%s"
    # value=category
    # cursor.execute(query,value)
    # connection.commit()
    # result=cursor.fetchall()
    
    # for i in range(len(result)):
    #     gl.append(result[i]['itemname'])

    
    # xaxis=["kurta1","kurta2","kurta3","kurta4"]
    # strength=[gl.count("kurta1"),gl.count("kurta2"),gl.count("kurta3"),gl.count("kurta4")]
    # fig = plt.figure(figsize =(10,7)) 
    # plt.pie(strength, labels = xaxis)
    # chart=FigureCanvasTkAgg(fig,frame3)
    # chart.get_tk_widget().pack()
    
    
    frame1.pack(fill="both",side="left")
    frame2.pack(fill="both",side="top")
    frame3.pack(fill="both",side="top")
    
    k.mainloop()
def kurta2():
    k1=tk.Toplevel()
    k1.geometry("1000x1000+0+0")
    k1.title("KURTA 2")
    
    frame2=tk.Frame(k1,height=400,width=500)
    frame2.config(background="misty rose")
    desc=tk.PhotoImage(file="kurta2desc.gif")
    tk.Label(frame2,image=desc).pack()
    
    frame1=tk.Frame(k1,height=900,width=500)
    frame1.config(background="misty rose")
    
    k2=tk.PhotoImage(file="kurta2.gif")
    tk.Label(frame1).pack()
    tk.Label(frame1,
             image=k2).pack()
    tk.Label(frame1).pack()
    tk.Label(frame1,
             text="Rs.900").pack()
    tk.Label(frame1).pack()
   
    b1k=tk.Button(frame1,
                  text="Add to cart",
                  highlightbackground="yellow",
                  command=insert,
                  bg="snow").pack()
    
    tk.Label(frame1).pack()
    
    press1aa=tk.Button(frame1,
                    text="GO to cart",
                    command=cart,
                    highlightbackground="yellow",
                    bg="snow").pack()
    
    def purchase(size):
        key="kurta 2"
        value=[900,size]
        dict[key]=value
        l.append(value[0])
        
    tk.Label(frame1,text="Size:").pack(side="left")
        
    global size 
    
    size=tk.Button(frame1,
                  text="X small",
                  bg="snow",
                  command=lambda: purchase("  size: X small")).pack(padx=10,pady=5,side="left")
    
    size=tk.Button(frame1,
                    text="small",
                    bg="snow",
                    command=lambda: purchase("  size: small")).pack(padx=10,pady=10,side="left")
    size=tk.Button(frame1,
                    text="medium",
                    bg="snow",
                    command=lambda: purchase(" size: medium")).pack(padx=10,pady=15,side="left")
    size=tk.Button(frame1,
                    text="large",
                    bg="snow",
                    command=lambda: purchase(" size: large")).pack(padx=10,pady=20,side="left")
    size=tk.Button(frame1,
                   text="X large",
                   bg="snow",
                    command=lambda: purchase(" size: X large")).pack(padx=10,pady=25,side="left")
    size=tk.Button(frame1,
                   text="XX large",
                   bg="snow",
                    command=lambda: purchase(" size: XX large")).pack(padx=10,pady=25,side="left")
    
    global name
    global price
    global model
    global category
    global gender
    gender='F'
    name="kurta2"
    price="Rs.900"
    model="D002"
    category="kurtas"
      
    global maincat
    maincat="women ethnic wear"  
    
    categories(model,category,maincat,gender)
    
    frame3=tk.Frame(k1,height=500,width=500)
    
    # query="SELECT * FROM products WHERE CATEGORY=%s"
    # value=category
    # cursor.execute(query,value)
    # connection.commit()
    # result=cursor.fetchall()
    
    # for i in range(len(result)):
    #     gl.append(result[i]['itemname'])

    
    # xaxis=["kurta1","kurta2","kurta3","kurta4"]
    # strength=[gl.count("kurta1"),gl.count("kurta2"),gl.count("kurta3"),gl.count("kurta4")]
    # fig = plt.figure(figsize =(10,7)) 
    # plt.pie(strength, labels = xaxis)
    # chart=FigureCanvasTkAgg(fig,frame3)
    # chart.get_tk_widget().pack()
    
    
    frame1.pack(fill="both",side="left")
    frame2.pack(fill="both",side="top")
    frame3.pack(fill="both",side="top")
    
    
    k1.mainloop()
def kurta3():
    k2=tk.Toplevel()
    k2.geometry("1000x1000+0+0")
    k2.title("KURTA 3")
    
    frame2=tk.Frame(k2,height=400,width=500)
    frame2.config(background="misty rose")
    desc=tk.PhotoImage(file="kurta3desc.gif")
    tk.Label(frame2,image=desc).pack()
    
    frame1=tk.Frame(k2,height=900,width=500)
    frame1.config(background="misty rose")
    
    
    k3=tk.PhotoImage(file="kurta3.gif")
    tk.Label(frame1).pack()
    
    tk.Label(frame1,
             image=k3).pack()
    tk.Label(frame1).pack()
    
    tk.Label(frame1,
             text="Rs.650").pack()
    tk.Label(frame1).pack()
    
    b1k=tk.Button(frame1,
                  text="Add to cart",
                  highlightbackground="yellow",
                  command=insert,
                  bg="snow").pack()
    
    tk.Label(frame1).pack()
    
    press1aa=tk.Button(frame1,
                    text="GO to cart",
                    command=cart,
                    highlightbackground="yellow",
                    bg="snow").pack()
    
    def purchase(size):
        key="kurta 3"
        value=[650,size]
        dict[key]=value
        l.append(value[0])
        
    tk.Label(frame1,text="Size:").pack(side="left")
        
    global size 
    
    size=tk.Button(frame1,
                  text="X small",
                  bg="snow",
                  command=lambda: purchase("  size: X small")).pack(padx=10,pady=5,side="left")
    
    size=tk.Button(frame1,
                    text="small",
                    bg="snow",
                    command=lambda: purchase("  size: small")).pack(padx=10,pady=10,side="left")
    size=tk.Button(frame1,
                    text="medium",
                    bg="snow",
                    command=lambda: purchase(" size: medium")).pack(padx=10,pady=15,side="left")
    size=tk.Button(frame1,
                    text="large",
                    bg="snow",
                    command=lambda: purchase(" size: large")).pack(padx=10,pady=20,side="left")
    size=tk.Button(frame1,
                   text="X large",
                   bg="snow",
                    command=lambda: purchase(" size: X large")).pack(padx=10,pady=25,side="left")
    size=tk.Button(frame1,
                   text="XX large",
                   bg="snow",
                    command=lambda: purchase(" size: XX large")).pack(padx=10,pady=25,side="left")
    
    global name
    global price
    global model
    global category
    global gender
    gender='F'
    name="kurta3"
    price="Rs.770"
    model="D001"
    category="kurtas"
    
    global maincat
    maincat="women ethnic wear"
    
    categories(model,category,maincat,gender)
    
    frame3=tk.Frame(k2,height=500,width=500)
    
    # query="SELECT * FROM products WHERE CATEGORY=%s"
    # value=category
    # cursor.execute(query,value)
    # connection.commit()
    # result=cursor.fetchall()
    
    # for i in range(len(result)):
    #     gl.append(result[i]['itemname'])

    
    # xaxis=["kurta1","kurta2","kurta3","kurta4"]
    # strength=[gl.count("kurta1"),gl.count("kurta2"),gl.count("kurta3"),gl.count("kurta4")]
    # fig = plt.figure(figsize =(10,7)) 
    # plt.pie(strength, labels = xaxis)
    # chart=FigureCanvasTkAgg(fig,frame3)
    # chart.get_tk_widget().pack()
    
    
    frame1.pack(fill="both",side="left")
    frame2.pack(fill="both",side="top")
    frame3.pack(fill="both",side="top")
    
    k2.mainloop()  
def kurta4():
    k3=tk.Toplevel()
    k3.geometry("1000x1000+0+0")
    k3.title("KURTA 4")
    
    frame2=tk.Frame(k3,height=400,width=500)
    frame2.config(background="misty rose")
    
    desc=tk.PhotoImage(file="kurta4desc.gif")
    tk.Label(frame2,image=desc).pack()
    
    frame1=tk.Frame(k3,height=900,width=500)
    frame1.config(background="misty rose")
    
    k4=tk.PhotoImage(file="kurta4.gif")
    tk.Label(frame1).pack()
    lab=tk.Label(frame1,
                 image=k4).pack()
    tk.Label(frame1).pack()
    tk.Label(frame1,
             text="Rs.800").pack()
    tk.Label(frame1).pack()
    
    b1k=tk.Button(frame1,
                  text="Add to cart",
                  highlightbackground="yellow",
                  command=insert,
                  bg="snow").pack()
    
    tk.Label(frame1).pack()
    press1aa=tk.Button(frame1,
                    text="GO to cart",
                    command=cart,
                    highlightbackground="yellow",
                    bg="snow").pack()
    
    def purchase(size):
        key="kurta 4"
        value=[800,size]
        dict[key]=value
        l.append(value[0])
        
    tk.Label(frame1,text="Size:").pack(side="left")
        
    global size 
    
    size=tk.Button(frame1,
                  text="X small",
                  bg="snow",
                  command=lambda: purchase("  size: X small")).pack(padx=10,pady=5,side="left")
    
    size=tk.Button(frame1,
                    text="small",
                    bg="snow",
                    command=lambda: purchase("  size: small")).pack(padx=10,pady=10,side="left")
    size=tk.Button(frame1,
                    text="medium",
                    bg="snow",
                    command=lambda: purchase(" size: medium")).pack(padx=10,pady=15,side="left")
    size=tk.Button(frame1,
                    text="large",
                    bg="snow",
                    command=lambda: purchase(" size: large")).pack(padx=10,pady=20,side="left")
    size=tk.Button(frame1,
                   text="X large",
                   bg="snow",
                    command=lambda: purchase(" size: X large")).pack(padx=10,pady=25,side="left")
    size=tk.Button(frame1,
                   text="XX large",
                   bg="snow",
                    command=lambda: purchase(" size: XX large")).pack(padx=10,pady=25,side="left")
    
    global name
    global price
    global model
    global category
    global gender
    gender='F'
    name="kurta4"
    price="Rs.800"
    model="D004"
    category="kurtas"
    
    global maincat
    maincat="women ethnic wear"
    
    categories(model,category,maincat,gender)
    
    frame3=tk.Frame(k3,height=500,width=500)
    
    # query="SELECT * FROM products WHERE CATEGORY=%s"
    # value=category
    # cursor.execute(query,value)
    # connection.commit()
    # result=cursor.fetchall()
    
    # for i in range(len(result)):
    #     gl.append(result[i]['itemname'])

    
    # xaxis=["kurta1","kurta2","kurta3","kurta4"]
    # strength=[gl.count("kurta1"),gl.count("kurta2"),gl.count("kurta3"),gl.count("kurta4")]
    # fig = plt.figure(figsize =(10,7)) 
    # plt.pie(strength, labels = xaxis)
    # chart=FigureCanvasTkAgg(fig,frame3)
    # chart.get_tk_widget().pack()
    
    
    frame1.pack(fill="both",side="left")
    frame2.pack(fill="both",side="top")
    frame3.pack(fill="both",side="top")
    
    k3.mainloop()
def lehenga1():
    l1=tk.Toplevel()
    l1.geometry("1000x1000+0+0")
    l1.title("LEHENGA 1")
    
    frame2=tk.Frame(l1,height=400,width=500)
    frame2.config(background="misty rose")
    
    desc=tk.PhotoImage(file="lehenga1desc.gif")
    tk.Label(frame2,image=desc).pack()
    
    frame1=tk.Frame(l1,height=900,width=500)
    frame1.config(background="misty rose")
    
    leh1=tk.PhotoImage(file="lehenga1.gif")
    
    tk.Label(frame1).pack()
    tk.Label(frame1,
             image=leh1).pack()
    tk.Label(frame1).pack()
    tk.Label(frame1,
             text="Rs.980").pack()
    tk.Label(frame1).pack()
    
    b1l=tk.Button(frame1,
                  text="Add to cart",
                  highlightbackground="yellow",
                  command=insert,
                  bg="snow").pack()
    
    tk.Label(frame1).pack()
    
    press1aa=tk.Button(frame1,
                    text="GO to cart",
                    command=cart,
                    highlightbackground="yellow",
                    bg="snow").pack()
    
    def purchase(size):
        key="lehenga1"
        value=[980,size]
        dict[key]=value
        l.append(value[0])
        
    tk.Label(frame1,text="Size:").pack(side="left")
    
    global size     
    
    size=tk.Button(frame1,
                  text="X small",
                  bg="snow",
                  command=lambda: purchase("  size: X small")).pack(padx=10,pady=5,side="left")
    
    size=tk.Button(frame1,
                    text="small",
                    bg="snow",
                    command=lambda: purchase("  size: small")).pack(padx=10,pady=10,side="left")
    size=tk.Button(frame1,
                    text="medium",
                    bg="snow",
                    command=lambda: purchase(" size: medium")).pack(padx=10,pady=15,side="left")
    size=tk.Button(frame1,
                    text="large",
                    bg="snow",
                    command=lambda: purchase(" size: large")).pack(padx=10,pady=20,side="left")
    size=tk.Button(frame1,
                   text="X large",
                   bg="snow",
                    command=lambda: purchase(" size: X large")).pack(padx=10,pady=25,side="left")
    size=tk.Button(frame1,
                   text="XX large",
                   bg="snow",
                    command=lambda: purchase(" size: XX large")).pack(padx=10,pady=25,side="left")
    
    global name
    global price
    global model
    global category
    global gender
    gender='F'
    name="lehenga1"
    price="Rs.980"
    model="E001"
    category="lehengas"
    
    global maincat
    maincat="women ethnic wear"
    
    categories(model,category,maincat,gender)
    
    frame3=tk.Frame(l1,height=500,width=500)
    
    # query="SELECT * FROM products WHERE CATEGORY=%s"
    # value=category
    # cursor.execute(query,value)
    # connection.commit()
    # result=cursor.fetchall()
    
    # for i in range(len(result)):
    #     gl.append(result[i]['itemname'])

    
    # xaxis=["lehenga1","lehenga2","saree1","saree2"]
    # strength=[gl.count("lehenga1"),gl.count("lehenga2"),gl.count("saree1"),gl.count("saree2")]
    # fig = plt.figure(figsize =(10,7)) 
    # plt.pie(strength, labels = xaxis)
    # chart=FigureCanvasTkAgg(fig,frame3)
    # chart.get_tk_widget().pack()
    
    
    frame1.pack(fill="both",side="left")
    frame2.pack(fill="both",side="top")
    frame3.pack(fill="both",side="top")
    
    l1.mainloop()
def lehenga2():
    l2=tk.Toplevel()
    l2.geometry("1000x1000+0+0")
    l2.title("LEHENGA 2")
    
    frame2=tk.Frame(l2,height=400,width=500)
    frame2.config(background="misty rose")
    
    desc=tk.PhotoImage(file="lehenga2desc.gif")
    tk.Label(frame2,image=desc).pack()
    
    frame1=tk.Frame(l2,height=900,width=500)
    frame1.config(background="misty rose")
    
    
    leh2=tk.PhotoImage(file="lehenga2.gif")
    
    tk.Label(frame1).pack()
    tk.Label(frame1,
             image=leh2).pack()
    tk.Label(frame1).pack()
    tk.Label(frame1,
             text="Rs.1055").pack()

    tk.Label(frame1).pack()
    
    b3l=tk.Button(frame1,
                  text="Add to cart",
                  highlightbackground="yellow",
                  command=insert,
                  bg="snow").pack()
    
    tk.Label(frame1).pack()
    
    press1aa=tk.Button(frame1,
                    text="GO to cart",
                    command=cart,
                    highlightbackground="yellow",
                    bg="snow").pack()
    
    def purchase(size):
        key="lehenga 2"
        value=[1055,size]
        dict[key]=value
        l.append(value[0])
        
    tk.Label(frame1,text="Size:").pack(side="left")
    
    global size     
    
    size=tk.Button(frame1,
                  text="X small",
                  bg="snow",
                  command=lambda: purchase("  size: X small")).pack(padx=10,pady=5,side="left")
    
    size=tk.Button(frame1,
                    text="small",
                    bg="snow",
                    command=lambda: purchase("  size: small")).pack(padx=10,pady=10,side="left")
    size=tk.Button(frame1,
                    text="medium",
                    bg="snow",
                    command=lambda: purchase(" size: medium")).pack(padx=10,pady=15,side="left")
    size=tk.Button(frame1,
                    text="large",
                    bg="snow",
                    command=lambda: purchase(" size: large")).pack(padx=10,pady=20,side="left")
    size=tk.Button(frame1,
                   text="X large",
                   bg="snow",
                    command=lambda: purchase(" size: X large")).pack(padx=10,pady=25,side="left")
    size=tk.Button(frame1,
                   text="XX large",
                   bg="snow",
                    command=lambda: purchase(" size: XX large")).pack(padx=10,pady=25,side="left")
    
    global name
    global price
    global model
    global category
    global gender
    gender='F'
    name="lehenga2"
    price="Rs.1055"
    model="E002"
    category="lehengas"
    
    global maincat
    maincat="women ethnic wear"
    
    categories(model,category,maincat,gender)
    
    frame3=tk.Frame(l2,height=500,width=500)
    
    # query="SELECT * FROM products WHERE CATEGORY=%s"
    # value=category
    # cursor.execute(query,value)
    # connection.commit()
    # result=cursor.fetchall()
    
    # for i in range(len(result)):
    #     gl.append(result[i]['itemname'])

    
    # xaxis=["lehenga1","lehenga2","saree1","saree2"]
    # strength=[gl.count("lehenga1"),gl.count("lehenga2"),gl.count("saree1"),gl.count("saree2")]
    # fig = plt.figure(figsize =(10,7)) 
    # plt.pie(strength, labels = xaxis)
    # chart=FigureCanvasTkAgg(fig,frame3)
    # chart.get_tk_widget().pack()


    
    frame1.pack(fill="both",side="left")
    frame2.pack(fill="both",side="top")
    frame3.pack(fill="both",side="top")
    
    l2.mainloop()
def saree1():
    s1=tk.Toplevel()
    s1.geometry("1000x1000+0+0")
    s1.title("SAREE 1")
    frame2=tk.Frame(s1,height=400,width=500)
    frame2.config(background="misty rose")
    
    desc=tk.PhotoImage(file="saree1desc.gif")
    tk.Label(frame2,image=desc).pack()
    
    frame1=tk.Frame(s1,height=900,width=500)
    frame1.config(background="misty rose")
    
    sar1=tk.PhotoImage(file="saree1.gif")
    
    tk.Label(frame1).pack()
    tk.Label(frame1,
             image=sar1).pack()
    tk.Label(frame1).pack()
    tk.Label(frame1,
             text="Rs.1080").pack()
    tk.Label(frame1).pack()
    
    b1s=tk.Button(frame1,
                  text="Add to cart",
                  highlightbackground="yellow",
                  command=insert,
                  bg="snow").pack()
    
    tk.Label(frame1).pack()
    
    press1aa=tk.Button(frame1,
                    text="GO to cart",
                    command=cart,
                    highlightbackground="yellow",
                    bg="snow").pack()
   
    def purchase(size):
        key="saree 1"
        value=[1080,size]
        dict[key]=value
        l.append(value[0])
        
    tk.Label(frame1,text="Size:").pack(side="left")
        
    global size 
    
    size=tk.Button(frame1,
                  text="X small",
                  bg="snow",
                  command=lambda: purchase("  size: X small")).pack(padx=10,pady=5,side="left")
    
    size=tk.Button(frame1,
                    text="small",
                    bg="snow",
                    command=lambda: purchase("  size: small")).pack(padx=10,pady=10,side="left")
    size=tk.Button(frame1,
                    text="medium",
                    bg="snow",
                    command=lambda: purchase(" size: medium")).pack(padx=10,pady=15,side="left")
    size=tk.Button(frame1,
                    text="large",
                    bg="snow",
                    command=lambda: purchase(" size: large")).pack(padx=10,pady=20,side="left")
    size=tk.Button(frame1,
                   text="X large",
                   bg="snow",
                    command=lambda: purchase(" size: X large")).pack(padx=10,pady=25,side="left")
    size=tk.Button(frame1,
                   text="XX large",
                   bg="snow",
                    command=lambda: purchase(" size: XX large")).pack(padx=10,pady=25,side="left")
    
    global name
    global price
    global model
    global category
    global gender
    gender='F'
    name="saree1"
    price="Rs.1080"
    model="E003"
    category="lehengas"
    
    global maincat
    maincat="women ethnic wear"
    
    categories(model,category,maincat,gender)
    
    frame3=tk.Frame(s1,height=500,width=500)
    
    # query="SELECT * FROM products WHERE CATEGORY=%s"
    # value=category
    # cursor.execute(query,value)
    # connection.commit()
    # result=cursor.fetchall()
    
    # for i in range(len(result)):
    #     gl.append(result[i]['itemname'])

    
    # xaxis=["lehenga1","lehenga2","saree1","saree2"]
    # strength=[gl.count("lehenga1"),gl.count("lehenga2"),gl.count("saree1"),gl.count("saree2")]
    # fig = plt.figure(figsize =(10,7)) 
    # plt.pie(strength, labels = xaxis)
    # chart=FigureCanvasTkAgg(fig,frame3)
    # chart.get_tk_widget().pack()
    
    
    frame1.pack(fill="both",side="left")
    frame2.pack(fill="both",side="top")
    frame3.pack(fill="both",side="top")
    
    
    s1.mainloop()
def saree2():
    s2=tk.Toplevel()
    s2.geometry("1000x1000+0+0")
    s2.title("SAREE 1")
    
    frame2=tk.Frame(s2,height=400,width=500)
    frame2.config(background="misty rose")
    
    desc=tk.PhotoImage(file="saree2desc.gif")
    tk.Label(frame2,image=desc).pack()
    
    frame1=tk.Frame(s2,height=900,width=500)
    frame1.config(background="misty rose")
    
    sar2=tk.PhotoImage(file="saree2.gif")
    
    tk.Label(frame1).pack()
    tk.Label(frame1,
             image=sar2).pack()
    
    tk.Label(frame1).pack()
    tk.Label(frame1,
             text="Rs.3000").pack()
    tk.Label(frame1).pack()
    
    
    b3s=tk.Button(frame1,
                  text="Add to cart",
                  highlightbackground="yellow",
                  command=insert,
                  bg="snow").pack()
    
    tk.Label(frame1).pack()
    
    press1aa=tk.Button(frame1,
                    text="GO to cart",
                    command=cart,
                    highlightbackground="yellow",
                    bg="snow").pack()
    
    def purchase(size):
        key="saree 2"
        value=[3000,size]
        dict[key]=value
        l.append(value[0])
        
    tk.Label(frame1,text="Size:").pack(side="left")
   
    global size 

    size=tk.Button(frame1,
                  text="X small",
                  bg="snow",
                  command=lambda: purchase("  size: X small")).pack(padx=10,pady=5,side="left")
    
    size=tk.Button(frame1,
                    text="small",
                    bg="snow",
                    command=lambda: purchase("  size: small")).pack(padx=10,pady=10,side="left")
    size=tk.Button(frame1,
                    text="medium",
                    bg="snow",
                    command=lambda: purchase(" size: medium")).pack(padx=10,pady=15,side="left")
    size=tk.Button(frame1,
                    text="large",
                    bg="snow",
                    command=lambda: purchase(" size: large")).pack(padx=10,pady=20,side="left")
    size=tk.Button(frame1,
                   text="X large",
                   bg="snow",
                    command=lambda: purchase(" size: X large")).pack(padx=10,pady=25,side="left")
    size=tk.Button(frame1,
                   text="XX large",
                   bg="snow",
                    command=lambda: purchase(" size: XX large")).pack(padx=10,pady=25,side="left")
    
    global name
    global price
    global model
    global category
    global gender
    gender='F'
    name="saree2"
    price="Rs.3000"
    model="E004"
    category="lehengas"
    
    global maincat
    maincat="women ethnic wear"
    
    categories(model,category,maincat,gender)
    
    frame3=tk.Frame(s2,height=500,width=500)
    
    # query="SELECT * FROM products WHERE CATEGORY=%s"
    # value=category
    # cursor.execute(query,value)
    # connection.commit()
    # result=cursor.fetchall()
    
    # for i in range(len(result)):
    #     gl.append(result[i]['itemname'])

    
    # xaxis=["lehenga1","lehenga2","saree1","saree2"]
    # strength=[gl.count("lehenga1"),gl.count("lehenga2"),gl.count("saree1"),gl.count("saree2")]
    # fig = plt.figure(figsize =(10,7)) 
    # plt.pie(strength, labels = xaxis)
    # chart=FigureCanvasTkAgg(fig,frame3)
    # chart.get_tk_widget().pack()
    
    
    frame1.pack(fill="both",side="left")
    frame2.pack(fill="both",side="top")
    frame3.pack(fill="both",side="top")
    
    
    s2.mainloop() 
def lehenga():
    l=tk.Toplevel()
    l.geometry("1700x800+0+0")
    l.config(background="seashell3")
    l.title("SAREES AND LEHENGAS")
    
    m=tk.PhotoImage(file="lehengacaption.gif")
    tk.Label(l,
             image=m).pack(side=tk.TOP)
    
    l1=tk.PhotoImage(file="lehenga1.gif")
    ln1=tk.Button(l,
                 text="lehenga 1",
                 image=l1,
                 compound="top",
                 command=lehenga1).pack(side=tk.LEFT)
    
    l2=tk.PhotoImage(file="lehenga2.gif")
    ln2=tk.Button(l,
                 text="lehenga 2",
                 image=l2,
                 compound="top",
                 command=lehenga2).pack(side=tk.LEFT)
    
    l3=tk.PhotoImage(file="saree1.gif")
    ln3=tk.Button(l,
                 text="saree 1",
                 image=l3,
                 compound="top",
                 command=saree1).pack(side=tk.LEFT)

    l4=tk.PhotoImage(file="saree2.gif")
    ln4=tk.Button(l,
                 text="saree 2",
                 image=l4,
                 compound="top",
                 command=saree2).pack(side=tk.LEFT)

    l.mainloop()
def kurta():
    kurti=tk.Toplevel()
    kurti.geometry("1700x800+0+0")
    kurti.config(background="seashell3")
    kurti.title("KURTAS AND SUIT SETS")
    
    m=tk.PhotoImage(file="kurtacaption.gif")
    tk.Label(kurti,
             image=m).pack(side=tk.TOP)
    
    k1=tk.PhotoImage(file="kurta1.gif")
    kt1=tk.Button(kurti,
                 text="kurta 1",
                 image=k1,
                 compound="top",
                 command=kurta1).pack(side=tk.LEFT)
    
    k2=tk.PhotoImage(file="kurta2.gif")
    kt2=tk.Button(kurti,
                 text="kurta 2",
                 image=k2,
                 compound="top",
                 command=kurta2).pack(side=tk.LEFT)
    
    k3=tk.PhotoImage(file="kurta3.gif")
    kt3=tk.Button(kurti,
                 text="kurta 3",
                 image=k3,
                 compound="top",
                  command=kurta3).pack(side=tk.LEFT)
    
    k4=tk.PhotoImage(file="kurta4.gif")
    kt4=tk.Button(kurti,
                 text="kurta 4",
                 image=k4,
                 compound="top",
                 command=kurta4).pack(side=tk.LEFT)
    
    kurti.mainloop()
def shirt1():
    upper=tk.Toplevel()
    upper.geometry("1000x1000+0+0")
    upper.title("SHIRT 1")
    
    frame2=tk.Frame(upper,height=400,width=500)
    frame2.config(background="misty rose")
    desc=tk.PhotoImage(file="shirt1desc.gif")
    tk.Label(frame2,image=desc).pack()
    
    frame1=tk.Frame(upper,height=900,width=500)
    frame1.config(background="misty rose")
    
    
    upper1=tk.PhotoImage(file="shirt1.gif")
    tk.Label(frame1).pack()
    lab=tk.Label(frame1,
                 image=upper1).pack()
    tk.Label(frame1).pack()
    tk.Label(frame1,
             text="Rs.800").pack()
    tk.Label(frame1).pack()
    
    b1s=tk.Button(frame1,
                  text="Add to cart",
                  highlightbackground="yellow",
                  command=insert,
                  bg="snow").pack()
    tk.Label(frame1).pack()
    
    press1aa=tk.Button(frame1,
                    text="GO to cart",
                    command=cart,
                    highlightbackground="yellow",
                    bg="snow").pack()
    
    def purchase(size):
        key="shirt1"
        value=[800,size]
        dict[key]=value
        l.append(value[0])
    
    tk.Label(frame1,text="Size:").pack(side="left")
        
    global size 
    
    size=tk.Button(frame1,
                  text="X small",
                  bg="snow",
                  command=lambda: purchase("  size: X small")).pack(padx=10,pady=5,side="left")
    
    size=tk.Button(frame1,
                    text="small",
                    bg="snow",
                    command=lambda: purchase("  size: small")).pack(padx=10,pady=10,side="left")
    size=tk.Button(frame1,
                    text="medium",
                    bg="snow",
                    command=lambda: purchase(" size: medium")).pack(padx=10,pady=15,side="left")
    size=tk.Button(frame1,
                    text="large",
                    bg="snow",
                    command=lambda: purchase(" size: large")).pack(padx=10,pady=20,side="left")
    size=tk.Button(frame1,
                   text="X large",
                   bg="snow",
                    command=lambda: purchase(" size: X large")).pack(padx=10,pady=25,side="left")
    size=tk.Button(frame1,
                   text="XX large",
                   bg="snow",
                    command=lambda: purchase(" size: XX large")).pack(padx=10,pady=25,side="left")
    
    global name
    global price
    global model
    global category
    global gender
    gender='M'
    name="shirt1"
    price="Rs.800"
    model="F001"
    category="shirts"
    
    global maincat
    maincat="men western wear"
    
    categories(model,category,maincat,gender)
    
    frame3=tk.Frame(upper,height=500,width=500)
    
    # query="SELECT * FROM products WHERE CATEGORY=%s"
    # value=category
    # cursor.execute(query,value)
    # connection.commit()
    # result=cursor.fetchall()
    
    # for i in range(len(result)):
    #     gl.append(result[i]['itemname'])

    
    # xaxis=["shirt1","shirt2","shirt3","shirt4"]
    # strength=[gl.count("shirt1"),gl.count("shirt2"),gl.count("shirt3"),gl.count("shirt4")]
    # fig = plt.figure(figsize =(10,7)) 
    # plt.pie(strength, labels = xaxis)
    # chart=FigureCanvasTkAgg(fig,frame3)
    # chart.get_tk_widget().pack()
    
    
    frame1.pack(fill="both",side="left")
    frame2.pack(fill="both",side="top")
    frame3.pack(fill="both",side="top")
    
    
    upper.mainloop()
def shirt2():
    uppe=tk.Toplevel()
    uppe.geometry("1000x1000+0+0")
    uppe.title("SHIRT 2")
    
    frame2=tk.Frame(uppe,height=400,width=500)
    frame2.config(background="misty rose")
    desc=tk.PhotoImage(file="shirt2desc.gif")
    tk.Label(frame2,image=desc).pack()
    
    frame1=tk.Frame(uppe,height=900,width=500)
    frame1.config(background="misty rose")
    
    
    upper1=tk.PhotoImage(file="shirt2.gif")
    tk.Label(frame1).pack()
    lab=tk.Label(frame1,
                 image=upper1).pack()
    tk.Label(frame1).pack()
    tk.Label(frame1,
             text="Rs.900").pack()
    tk.Label(frame1).pack()
    
    b1s=tk.Button(frame1,
                  text="Add to cart",
                  highlightbackground="yellow",
                  command=insert,
                  bg="snow").pack()
    
    tk.Label(frame1).pack()
    
    press1aa=tk.Button(frame1,
                    text="GO to cart",
                    command=cart,
                    highlightbackground="yellow",
                    bg="snow").pack()
    
    def purchase(size):
        key="shirt2"
        value=[900,size]
        dict[key]=value
        l.append(value[0])
    
    tk.Label(frame1,text="Size:").pack(side="left")
        
    global size 
    
    size=tk.Button(frame1,
                  text="X small",
                  bg="snow",
                  command=lambda: purchase("  size: X small")).pack(padx=10,pady=5,side="left")
    
    size=tk.Button(frame1,
                    text="small",
                    bg="snow",
                    command=lambda: purchase("  size: small")).pack(padx=10,pady=10,side="left")
    size=tk.Button(frame1,
                    text="medium",
                    bg="snow",
                    command=lambda: purchase(" size: medium")).pack(padx=10,pady=15,side="left")
    size=tk.Button(frame1,
                    text="large",
                    bg="snow",
                    command=lambda: purchase(" size: large")).pack(padx=10,pady=20,side="left")
    size=tk.Button(frame1,
                   text="X large",
                   bg="snow",
                    command=lambda: purchase(" size: X large")).pack(padx=10,pady=25,side="left")
    size=tk.Button(frame1,
                   text="XX large",
                   bg="snow",
                    command=lambda: purchase(" size: XX large")).pack(padx=10,pady=25,side="left")
    
    global name
    global price
    global model
    global category
    global gender
    gender='M'
    name="shirt2"
    price="Rs.900"
    model="F002"
    category="shirts"
    
    global maincat
    maincat="men western wear"
    
    categories(model,category,maincat,gender)
    
    frame3=tk.Frame(uppe,height=500,width=500)
    
    # query="SELECT * FROM products WHERE CATEGORY=%s"
    # value=category
    # cursor.execute(query,value)
    # connection.commit()
    # result=cursor.fetchall()
    
    # for i in range(len(result)):
    #     gl.append(result[i]['itemname'])

    
    # xaxis=["shirt1","shirt2","shirt3","shirt4"]
    # strength=[gl.count("shirt1"),gl.count("shirt2"),gl.count("shirt3"),gl.count("shirt4")]
    # fig = plt.figure(figsize =(10,7)) 
    # plt.pie(strength, labels = xaxis)
    # chart=FigureCanvasTkAgg(fig,frame3)
    # chart.get_tk_widget().pack()
    
    
    frame1.pack(fill="both",side="left")
    frame2.pack(fill="both",side="top")
    frame3.pack(fill="both",side="top")
    
    
    uppe.mainloop()    
def shirt3():
    upp=tk.Toplevel()
    upp.geometry("1000x1000+0+0")
    upp.title("SHIRT 3")
    
    frame2=tk.Frame(upp,height=400,width=500)
    frame2.config(background="misty rose")
    desc=tk.PhotoImage(file="shirt3desc.gif")
    tk.Label(frame2,image=desc).pack()
    
    frame1=tk.Frame(upp,height=900,width=500)
    frame1.config(background="misty rose")
    
    
    upper3=tk.PhotoImage(file="shirt3.gif")
    tk.Label(frame1).pack()
    lab=tk.Label(frame1,
                 image=upper3).pack()
    tk.Label(frame1).pack()
    tk.Label(frame1,
             text="Rs.650").pack()
    tk.Label(frame1).pack()
    
    
    b1s=tk.Button(frame1,
                  text="Add to cart",
                  highlightbackground="yellow",
                  command=insert,
                  bg="snow").pack()
    
    tk.Label(frame1).pack()
    
    press1aa=tk.Button(frame1,
                    text="GO to cart",
                    command=cart,
                    highlightbackground="yellow",
                    bg="snow").pack()
    
    def purchase(size):
        key="shirt3"
        value=[650,size]
        dict[key]=value
        l.append(value[0])
        
    tk.Label(frame1,text="Size:").pack(side="left")
        
    global size 
    
    size=tk.Button(frame1,
                  text="X small",
                  bg="snow",
                  command=lambda: purchase("  size: X small")).pack(padx=10,pady=5,side="left")
    
    size=tk.Button(frame1,
                    text="small",
                    bg="snow",
                    command=lambda: purchase("  size: small")).pack(padx=10,pady=10,side="left")
    size=tk.Button(frame1,
                    text="medium",
                    bg="snow",
                    command=lambda: purchase(" size: medium")).pack(padx=10,pady=15,side="left")
    size=tk.Button(frame1,
                    text="large",
                    bg="snow",
                    command=lambda: purchase(" size: large")).pack(padx=10,pady=20,side="left")
    size=tk.Button(frame1,
                   text="X large",
                   bg="snow",
                    command=lambda: purchase(" size: X large")).pack(padx=10,pady=25,side="left")
    size=tk.Button(frame1,
                   text="XX large",
                   bg="snow",
                    command=lambda: purchase(" size: XX large")).pack(padx=10,pady=25,side="left")
    
    global name
    global price
    global model
    global category
    global gender
    gender='M'
    name="shirt3"
    price="Rs.650"
    model="F002"
    category="shirts"
    
    global maincat
    maincat="men western wear"
    
    categories(model,category,maincat,gender)
    
    frame3=tk.Frame(upp,height=500,width=500)
    
    # query="SELECT * FROM products WHERE CATEGORY=%s"
    # value=category
    # cursor.execute(query,value)
    # connection.commit()
    # result=cursor.fetchall()
    
    # for i in range(len(result)):
    #     gl.append(result[i]['itemname'])

    
    # xaxis=["shirt1","shirt2","shirt3","shirt4"]
    # strength=[gl.count("shirt1"),gl.count("shirt2"),gl.count("shirt3"),gl.count("shirt4")]
    # fig = plt.figure(figsize =(10,7)) 
    # plt.pie(strength, labels = xaxis)
    # chart=FigureCanvasTkAgg(fig,frame3)
    # chart.get_tk_widget().pack()
    
    
    frame1.pack(fill="both",side="left")
    frame2.pack(fill="both",side="top")
    frame3.pack(fill="both",side="top")
    
    
    upp.mainloop()
def shirt4():
    up=tk.Toplevel()
    up.geometry("1000x1000+0+0")
    up.title("SHIRT 4")
    
    frame2=tk.Frame(up,height=400,width=500)
    frame2.config(background="misty rose")
    desc=tk.PhotoImage(file="shirt4desc.gif")
    tk.Label(frame2,image=desc).pack()
    
    frame1=tk.Frame(up,height=900,width=500)
    frame1.config(background="misty rose")
    
    
    upper4=tk.PhotoImage(file="shirt4.gif")
    tk.Label(frame1).pack()
    lab=tk.Label(frame1,
                 image=upper4).pack()
    tk.Label(frame1).pack()
    tk.Label(frame1,
             text="Rs.700").pack()
    tk.Label(frame1).pack()
    
    
    b1s=tk.Button(frame1,
                  text="Add to cart",
                  highlightbackground="yellow",
                  command=insert,
                  bg="snow").pack()
    tk.Label(frame1).pack()

    press1aa=tk.Button(frame1,
                    text="GO to cart",
                    command=cart,
                    highlightbackground="yellow",
                    bg="snow").pack()
    
    def purchase(size):
        key="shirt4"
        value=[700,size]
        dict[key]=value
        l.append(value[0])
      
    tk.Label(frame1,text="Size:").pack(side="left")
        
    global size 
    
    size=tk.Button(frame1,
                  text="X small",
                  bg="snow",
                  command=lambda: purchase("  size: X small")).pack(padx=10,pady=5,side="left")
    
    size=tk.Button(frame1,
                    text="small",
                    bg="snow",
                    command=lambda: purchase("  size: small")).pack(padx=10,pady=10,side="left")
    size=tk.Button(frame1,
                    text="medium",
                    bg="snow",
                    command=lambda: purchase(" size: medium")).pack(padx=10,pady=15,side="left")
    size=tk.Button(frame1,
                    text="large",
                    bg="snow",
                    command=lambda: purchase(" size: large")).pack(padx=10,pady=20,side="left")
    size=tk.Button(frame1,
                   text="X large",
                   bg="snow",
                    command=lambda: purchase(" size: X large")).pack(padx=10,pady=25,side="left")
    size=tk.Button(frame1,
                   text="XX large",
                   bg="snow",
                    command=lambda: purchase(" size: XX large")).pack(padx=10,pady=25,side="left")
    
    
    global name
    global price
    global model
    global category
    global gender
    gender='M'
    name="shirt4"
    price="Rs.700"
    model="F004"
    category="shirts"
   
    global maincat
    maincat="men western wear"
    
    categories(model,category,maincat,gender)
    
    frame3=tk.Frame(up,height=500,width=500)
    
    # query="SELECT * FROM products WHERE CATEGORY=%s"
    # value=category
    # cursor.execute(query,value)
    # connection.commit()
    # result=cursor.fetchall()
    
    # for i in range(len(result)):
    #     gl.append(result[i]['itemname'])

    
    # xaxis=["shirt1","shirt2","shirt3","shirt4"]
    # strength=[gl.count("shirt1"),gl.count("shirt2"),gl.count("shirt3"),gl.count("shirt4")]
    # fig = plt.figure(figsize =(10,7)) 
    # plt.pie(strength, labels = xaxis)
    # chart=FigureCanvasTkAgg(fig,frame3)
    # chart.get_tk_widget().pack()
    
    
    frame1.pack(fill="both",side="left")
    frame2.pack(fill="both",side="top")
    frame3.pack(fill="both",side="top")
    
    up.mainloop()
def shirt():
    tee=tk.Toplevel()
    tee.geometry("1700x800+0+0")
    tee.config(background="seashell3")
    tee.title("SHIRTS AND T-SHIRTS")
    
    m=tk.PhotoImage(file="shirtcaption.gif")
    tk.Label(tee,
             image=m).pack(side=tk.TOP)
    
    t=tk.PhotoImage(file="shirt1.gif")
    btt=tk.Button(tee,
                text="shirt1",
                image=t,
                compound="top",
                command=shirt1).pack(side=tk.LEFT)
    
    t1=tk.PhotoImage(file="shirt2.gif")
    btt1=tk.Button(tee,
                text="shirt2",
                image=t1,
                compound="top",
                command=shirt2).pack(side=tk.LEFT)
    
    t2=tk.PhotoImage(file="shirt3.gif")
    btt2=tk.Button(tee,
                text="shirt3",
                image=t2,
                compound="top",
                command=shirt3).pack(side=tk.LEFT)
    
    t3=tk.PhotoImage(file="shirt4.gif")
    btt3=tk.Button(tee,
                text="shirt4",
                image=t3,
                compound="top",
                command=shirt4).pack(side=tk.LEFT)
    
    tee.mainloop()
def denim1():
    den1=tk.Toplevel()
    den1.geometry("1000x1000+0+0")
    den1.title("DENIM 1")
    
    frame2=tk.Frame(den1,height=400,width=500)
    frame2.config(background="misty rose")
    desc=tk.PhotoImage(file="mjeans1desc.gif")
    tk.Label(frame2,image=desc).pack()
    
    frame1=tk.Frame(den1,height=900,width=500)
    frame1.config(background="misty rose")
    
    
    de1=tk.PhotoImage(file="mjeans1.gif")
    tk.Label(frame1).pack()
    tk.Label(frame1,
             image=de1).pack()
    tk.Label(frame1).pack()
    tk.Label(frame1,
             text="Rs.650").pack()
    tk.Label(frame1).pack()
    
    
    tk.Button(frame1,
              text="Add to cart",
              highlightbackground="yellow",
              command=insert,
              bg="snow").pack()
    
    tk.Label(frame1).pack()
    
    press1aa=tk.Button(frame1,
                       text="GO to cart",
                       command=cart,
                       highlightbackground="yellow",
                       bg="snow").pack()
    
    def purchase(size):
        key="denim1"
        value=[650,size]
        dict[key]=value
        l.append(value[0])
        
    tk.Label(frame1,text="Size:").pack(side="left")
    
    global size     
    
    size=tk.Button(frame1,
                  text="X small",
                  bg="snow",
                  command=lambda: purchase("  size: X small")).pack(padx=10,pady=5,side="left")
    
    size=tk.Button(frame1,
                    text="small",
                    bg="snow",
                    command=lambda: purchase("  size: small")).pack(padx=10,pady=10,side="left")
    size=tk.Button(frame1,
                    text="medium",
                    bg="snow",
                    command=lambda: purchase(" size: medium")).pack(padx=10,pady=15,side="left")
    size=tk.Button(frame1,
                    text="large",
                    bg="snow",
                    command=lambda: purchase(" size: large")).pack(padx=10,pady=20,side="left")
    size=tk.Button(frame1,
                   text="X large",
                   bg="snow",
                    command=lambda: purchase(" size: X large")).pack(padx=10,pady=25,side="left")
    size=tk.Button(frame1,
                   text="XX large",
                   bg="snow",
                    command=lambda: purchase(" size: XX large")).pack(padx=10,pady=25,side="left")
    
    global name
    global price
    global model
    global category
    global gender
    gender='M'
    name="denim1"
    price="Rs.650"
    model="G001"
    category="denims"
    
    global maincat
    maincat="men western wear"
    
    categories(model,category,maincat,gender)
    
    frame3=tk.Frame(den1,height=500,width=500)
    
    # query="SELECT * FROM products WHERE CATEGORY=%s"
    # value=category
    # cursor.execute(query,value)
    # connection.commit()
    # result=cursor.fetchall()
    
    # for i in range(len(result)):
    #     gl.append(result[i]['itemname'])

    
    # xaxis=["denim1","denim2","denim3","denim4"]
    # strength=[gl.count("denim1"),gl.count("denim2"),gl.count("denim3"),gl.count("denim4")]
    # fig = plt.figure(figsize =(10,7)) 
    # plt.pie(strength, labels = xaxis)
    # chart=FigureCanvasTkAgg(fig,frame3)
    # chart.get_tk_widget().pack()
    
    
    frame1.pack(fill="both",side="left")
    frame2.pack(fill="both",side="top")
    frame3.pack(fill="both",side="top")
    
    
    den1.mainloop()
def denim2():
    den2=tk.Toplevel()
    den2.geometry("1000x1000+0+0")
    den2.title("DENIM 2")
    
    frame2=tk.Frame(den2,height=400,width=500)
    frame2.config(background="misty rose")
    
    desc=tk.PhotoImage(file="mjeans2desc.gif")
    tk.Label(frame2,image=desc).pack()
    
    frame1=tk.Frame(den2,height=900,width=500)
    frame1.config(background="misty rose")
    
    d2=tk.PhotoImage(file="mjeans2.gif")
    tk.Label(frame1).pack()
    lab=tk.Label(frame1,
                 image=d2).pack()
    tk.Label(frame1).pack()
    tk.Label(frame1,
             text="Rs.500").pack()
    tk.Label(frame1).pack()
    
    
    b1s=tk.Button(frame1,
                  text="Add to cart",
                  highlightbackground="yellow",
                  command=insert,
                  bg="snow").pack()
    tk.Label(frame1).pack()
    
    press1aa=tk.Button(frame1,
                    text="GO to cart",
                    command=cart,
                    highlightbackground="yellow",
                    bg="snow").pack()
    
    def purchase(size):
        key="denim 2"
        value=[500,size]
        dict[key]=value
        l.append(value[0])
        
    tk.Label(frame1,text="Size:").pack(side="left")
    
    global size     
    
    size=tk.Button(frame1,
                  text="X small",
                  bg="snow",
                  command=lambda: purchase("  size: X small")).pack(padx=10,pady=5,side="left")
    
    size=tk.Button(frame1,
                    text="small",
                    bg="snow",
                    command=lambda: purchase("  size: small")).pack(padx=10,pady=10,side="left")
    size=tk.Button(frame1,
                    text="medium",
                    bg="snow",
                    command=lambda: purchase(" size: medium")).pack(padx=10,pady=15,side="left")
    size=tk.Button(frame1,
                    text="large",
                    bg="snow",
                    command=lambda: purchase(" size: large")).pack(padx=10,pady=20,side="left")
    size=tk.Button(frame1,
                   text="X large",
                   bg="snow",
                    command=lambda: purchase(" size: X large")).pack(padx=10,pady=25,side="left")
    size=tk.Button(frame1,
                   text="XX large",
                   bg="snow",
                    command=lambda: purchase(" size: XX large")).pack(padx=10,pady=25,side="left")
    
    global name
    global price
    global model
    global category
    global gender
    gender='M'
    name="denim2"
    price="Rs.500"
    model="G002"
    category="denims"
    
    global maincat
    maincat="men western wear"
    
    categories(model,category,maincat,gender)
    
    frame3=tk.Frame(den2,height=500,width=500)
    
    # query="SELECT * FROM products WHERE CATEGORY=%s"
    # value=category
    # cursor.execute(query,value)
    # connection.commit()
    # result=cursor.fetchall()
    
    # for i in range(len(result)):
    #     gl.append(result[i]['itemname'])

    
    # xaxis=["denim1","denim2","denim3","denim4"]
    # strength=[gl.count("denim1"),gl.count("denim2"),gl.count("denim3"),gl.count("denim4")]
    # fig = plt.figure(figsize =(10,7)) 
    # plt.pie(strength, labels = xaxis)
    # chart=FigureCanvasTkAgg(fig,frame3)
    # chart.get_tk_widget().pack()
    
    
    frame1.pack(fill="both",side="left")
    frame2.pack(fill="both",side="top")
    frame3.pack(fill="both",side="top")
    
    
    den2.mainloop()
def denim3():
    den3=tk.Toplevel()
    den3.geometry("1000x1000+0+0")
    den3.title("DENIM 3")
    
    frame2=tk.Frame(den3,height=400,width=500)
    frame2.config(background="misty rose")
    
    desc=tk.PhotoImage(file="mjeans3desc.gif")
    tk.Label(frame2,image=desc).pack()
    
    frame1=tk.Frame(den3,height=900,width=500)
    frame1.config(background="misty rose")
    
    d3=tk.PhotoImage(file="mjeans3.gif")
    tk.Label(frame1).pack()
    lab=tk.Label(frame1,
                 image=d3).pack()
    
    tk.Label(frame1).pack()
    tk.Label(frame1,
             text="Rs.780").pack()
    tk.Label(frame1).pack()
    
    b1s=tk.Button(frame1,
                  text="Add to cart",
                  highlightbackground="yellow",
                  command=insert,
                  bg="snow").pack()
    
    tk.Label(frame1).pack()
    
    press1aa=tk.Button(frame1,
                    text="GO to cart",
                    command=cart,
                    highlightbackground="yellow",
                    bg="snow").pack()
    
    def purchase(size):
        key="denim3"
        value=[780,size]
        dict[key]=value
        l.append(value[0])
        
    tk.Label(frame1,text="Size:").pack(side="left")
        
    global size 
    
    size=tk.Button(frame1,
                  text="X small",
                  bg="snow",
                  command=lambda: purchase("  size: X small")).pack(padx=10,pady=5,side="left")
    
    size=tk.Button(frame1,
                    text="small",
                    bg="snow",
                    command=lambda: purchase("  size: small")).pack(padx=10,pady=10,side="left")
    size=tk.Button(frame1,
                    text="medium",
                    bg="snow",
                    command=lambda: purchase(" size: medium")).pack(padx=10,pady=15,side="left")
    size=tk.Button(frame1,
                    text="large",
                    bg="snow",
                    command=lambda: purchase(" size: large")).pack(padx=10,pady=20,side="left")
    size=tk.Button(frame1,
                   text="X large",
                   bg="snow",
                    command=lambda: purchase(" size: X large")).pack(padx=10,pady=25,side="left")
    size=tk.Button(frame1,
                   text="XX large",
                   bg="snow",
                    command=lambda: purchase(" size: XX large")).pack(padx=10,pady=25,side="left")
    
    global name
    global price
    global model
    global category
    global gender
    gender='M'
    name="denim3"
    price="Rs.780"
    model="G003"
    category="denims"
    
    global maincat
    maincat="men western wear"
    
    categories(model,category,maincat,gender)
    
    frame3=tk.Frame(den3,height=500,width=500)
    
    # query="SELECT * FROM products WHERE CATEGORY=%s"
    # value=category
    # cursor.execute(query,value)
    # connection.commit()
    # result=cursor.fetchall()
    
    # for i in range(len(result)):
    #     gl.append(result[i]['itemname'])

    
    # xaxis=["denim1","denim2","denim3","denim4"]
    # strength=[gl.count("denim1"),gl.count("denim2"),gl.count("denim3"),gl.count("denim4")]
    # fig = plt.figure(figsize =(10,7)) 
    # plt.pie(strength, labels = xaxis)
    # chart=FigureCanvasTkAgg(fig,frame3)
    # chart.get_tk_widget().pack()
    
    
    frame1.pack(fill="both",side="left")
    frame2.pack(fill="both",side="top")
    frame3.pack(fill="both",side="top")
    
    
    den3.mainloop()
def denim4():
    den4=tk.Toplevel()
    den4.geometry("1000x1000+0+0")
    den4.title("DENIM 4")
    
    frame2=tk.Frame(den4,height=400,width=500)
    frame2.config(background="misty rose")
    
    desc=tk.PhotoImage(file="mjeans4desc.gif")
    tk.Label(frame2,image=desc).pack()
    
    frame1=tk.Frame(den4,height=900,width=500)
    frame1.config(background="misty rose")
    
    d4=tk.PhotoImage(file="mjeans4.gif")
    tk.Label(frame1).pack()
    lab=tk.Label(frame1,
                 image=d4).pack()
    
    tk.Label(frame1).pack()
    tk.Label(frame1,
             text="Rs.900").pack()
    tk.Label(frame1).pack()
    
    b1s=tk.Button(frame1,
                  text="Add to cart",
                  highlightbackground="yellow",
                  command=insert,
                  bg="snow").pack()
    
    tk.Label(frame1).pack()
    press1aa=tk.Button(frame1,
                    text="GO to cart",
                    command=cart,
                    highlightbackground="yellow",
                    bg="snow").pack()
    
    def purchase(size):
        key="denim4"
        value=[900,size]
        dict[key]=value
        l.append(value[0])
        
    tk.Label(frame1,text="Size:").pack(side="left")
        
    global size 
    
    size=tk.Button(frame1,
                  text="X small",
                  bg="snow",
                  command=lambda: purchase("  size: X small")).pack(padx=10,pady=5,side="left")
    
    size=tk.Button(frame1,
                    text="small",
                    bg="snow",
                    command=lambda: purchase("  size: small")).pack(padx=10,pady=10,side="left")
    size=tk.Button(frame1,
                    text="medium",
                    bg="snow",
                    command=lambda: purchase(" size: medium")).pack(padx=10,pady=15,side="left")
    size=tk.Button(frame1,
                    text="large",
                    bg="snow",
                    command=lambda: purchase(" size: large")).pack(padx=10,pady=20,side="left")
    size=tk.Button(frame1,
                   text="X large",
                   bg="snow",
                    command=lambda: purchase(" size: X large")).pack(padx=10,pady=25,side="left")
    size=tk.Button(frame1,
                   text="XX large",
                   bg="snow",
                    command=lambda: purchase(" size: XX large")).pack(padx=10,pady=25,side="left")
    
    global name
    global price
    global model
    global category
    global gender
    gender='M'
    name="denim4"
    price="Rs.900"
    model="G004"
    category="denims"
    
    global maincat
    maincat="men western wear"
    
    categories(model,category,maincat,gender)
    
    frame3=tk.Frame(den4,height=500,width=500)
    
    # query="SELECT * FROM products WHERE CATEGORY=%s"
    # value=category
    # cursor.execute(query,value)
    # connection.commit()
    # result=cursor.fetchall()
    
    # for i in range(len(result)):
    #     gl.append(result[i]['itemname'])

    
    # xaxis=["denim1","denim2","denim3","denim4"]
    # strength=[gl.count("denim1"),gl.count("denim2"),gl.count("denim3"),gl.count("denim4")]
    # fig = plt.figure(figsize =(10,7)) 
    # plt.pie(strength, labels = xaxis)
    # chart=FigureCanvasTkAgg(fig,frame3)
    # chart.get_tk_widget().pack()
    
    
    frame1.pack(fill="both",side="left")
    frame2.pack(fill="both",side="top")
    frame3.pack(fill="both",side="top")
    den4.mainloop()
def denims():
    den=tk.Toplevel()
    den.geometry("1700x800+0+0")
    den.config(background="seashell3")
    den.title("DENIMS AND TROUSERS")
    
    m=tk.PhotoImage(file="mjeanscaption.gif")
    tk.Label(den,
             image=m).pack(side=tk.TOP)
    
    d1=tk.PhotoImage(file="mjeans1.gif")
    btd=tk.Button(den,
                text="denim1",
                image=d1,
                compound="top",
                command=denim1).pack(side=tk.LEFT)
    
    d2=tk.PhotoImage(file="mjeans2.gif")
    btd2=tk.Button(den,
                text="denim2",
                image=d2,
                compound="top",
                command=denim2).pack(side=tk.LEFT)
    
    d3=tk.PhotoImage(file="mjeans3.gif")
    btd3=tk.Button(den,
                text="denim3",
                image=d3,
                compound="top",
                command=denim3).pack(side=tk.LEFT)
    
    d4=tk.PhotoImage(file="mjeans4.gif")
    btd4=tk.Button(den,
                text="denim4",
                image=d4,
                compound="top",
                command=denim4).pack(side=tk.LEFT)

    den.mainloop()    
def ethinic1():
    met=tk.Toplevel()
    met.geometry("1000x1000+0+0")
    met.title("ETHINIC 1")
    
    frame2=tk.Frame(met,height=400,width=500)
    frame2.config(background="misty rose")
    desc=tk.PhotoImage(file="eth1desc.gif")
    tk.Label(frame2,image=desc).pack()
    
    frame1=tk.Frame(met,height=900,width=500)
    frame1.config(background="misty rose")
    
    e=tk.PhotoImage(file="eth1.gif")
    
    tk.Label(frame1).pack()
    lab=tk.Label(frame1,
                 image=e).pack()
    tk.Label(frame1).pack()
    tk.Label(frame1,
             text="Rs.1500").pack()
    
    tk.Label(frame1).pack()  
    
    b1s=tk.Button(frame1,
                  text="Add to cart",
                  highlightbackground="yellow",
                  command=insert,
                  bg="snow").pack()
    
    tk.Label(frame1).pack()
    
    press1aa=tk.Button(frame1,
                    text="GO to cart",
                    command=cart,
                    highlightbackground="yellow",
                    bg="snow").pack()
    
    def purchase(size):
        key="ethinic 1"
        value=[1500,size]
        dict[key]=value
        l.append(value[0])
        
    tk.Label(frame1,text="Size:").pack(side="left")
        
    global size 
    
    size=tk.Button(frame1,
                  text="X small",
                  bg="snow",
                  command=lambda: purchase("  size: X small")).pack(padx=10,pady=5,side="left")
    
    size=tk.Button(frame1,
                    text="small",
                    bg="snow",
                    command=lambda: purchase("  size: small")).pack(padx=10,pady=10,side="left")
    size=tk.Button(frame1,
                    text="medium",
                    bg="snow",
                    command=lambda: purchase(" size: medium")).pack(padx=10,pady=15,side="left")
    size=tk.Button(frame1,
                    text="large",
                    bg="snow",
                    command=lambda: purchase(" size: large")).pack(padx=10,pady=20,side="left")
    size=tk.Button(frame1,
                   text="X large",
                   bg="snow",
                    command=lambda: purchase(" size: X large")).pack(padx=10,pady=25,side="left")
    size=tk.Button(frame1,
                   text="XX large",
                   bg="snow",
                    command=lambda: purchase(" size: XX large")).pack(padx=10,pady=25,side="left")
    
    global name
    global price
    global model
    global category
    global gender
    gender='M'
    name="ethnic1"
    price="Rs.1500"
    model="H001"
    category="ethinic"
   
    global maincat
    maincat="men ethnic wear"
    
    categories(model,category,maincat,gender)
    
    frame3=tk.Frame(met,height=500,width=500)
    
    # query="SELECT * FROM products WHERE CATEGORY=%s"
    # value=category
    # cursor.execute(query,value)
    # connection.commit()
    # result=cursor.fetchall()
    
    # for i in range(len(result)):
    #     gl.append(result[i]['itemname'])

    
    # xaxis=["ethnic1","ethnic2","ethnic3","ethnic4"]
    # strength=[gl.count("ethnic1"),gl.count("ethnic2"),gl.count("ethnic3"),gl.count("ethnic4")]
    # fig = plt.figure(figsize =(10,7)) 
    # plt.pie(strength, labels = xaxis)
    # chart=FigureCanvasTkAgg(fig,frame3)
    # chart.get_tk_widget().pack()
    
    
    frame1.pack(fill="both",side="left")
    frame2.pack(fill="both",side="top")
    frame3.pack(fill="both",side="top")
    
    met.mainloop()    
def ethinic2():
    met1=tk.Toplevel()
    met1.geometry("1000x1000+0+0")
    met1.title("ETHINIC 2")
    
    frame2=tk.Frame(met1,height=400,width=500)
    frame2.config(background="misty rose")
    desc=tk.PhotoImage(file="eth2desc.gif")
    tk.Label(frame2,image=desc).pack()
    
    frame1=tk.Frame(met1,height=900,width=500)
    frame1.config(background="misty rose")
    
    e1=tk.PhotoImage(file="eth2.gif")
    tk.Label(frame1).pack()
    lab=tk.Label(frame1,
                 image=e1).pack()
    tk.Label(frame1).pack()
    tk.Label(frame1,
             text="Rs.980").pack()
    tk.Label(frame1).pack()
    
    b1s=tk.Button(frame1,
                  text="Add to cart",
                  highlightbackground="yellow",
                  command=insert,
                  bg="snow").pack()
    
    tk.Label(frame1).pack()
    
    press1aa=tk.Button(frame1,
                    text="GO to cart",
                    command=cart,
                    highlightbackground="yellow",
                    bg="snow").pack()
    
    def purchase(size):
        key="ethnic 2"
        value=[980,size]
        dict[key]=value
        l.append(value[0])
        
    tk.Label(frame1,text="Size:").pack(side="left")
    
    global size 
        
    size=tk.Button(frame1,
                  text="X small",
                  bg="snow",
                  command=lambda: purchase("  size: X small")).pack(padx=10,pady=5,side="left")
    
    size=tk.Button(frame1,
                    text="small",
                    bg="snow",
                    command=lambda: purchase("  size: small")).pack(padx=10,pady=10,side="left")
    size=tk.Button(frame1,
                    text="medium",
                    bg="snow",
                    command=lambda: purchase(" size: medium")).pack(padx=10,pady=15,side="left")
    size=tk.Button(frame1,
                    text="large",
                    bg="snow",
                    command=lambda: purchase(" size: large")).pack(padx=10,pady=20,side="left")
    size=tk.Button(frame1,
                   text="X large",
                   bg="snow",
                    command=lambda: purchase(" size: X large")).pack(padx=10,pady=25,side="left")
    size=tk.Button(frame1,
                   text="XX large",
                   bg="snow",
                    command=lambda: purchase(" size: XX large")).pack(padx=10,pady=25,side="left")
    
    global name
    global price
    global model
    global category
    global gender
    gender='M'
    name="ethnic2"
    price="Rs.980"
    model="H002"
    category="ethinic"
    
    global maincat
    maincat="men ethnic wear"
    
    categories(model,category,maincat,gender)
    
    frame3=tk.Frame(met1,height=500,width=500)
    
    # query="SELECT * FROM products WHERE CATEGORY=%s"
    # value=category
    # cursor.execute(query,value)
    # connection.commit()
    # result=cursor.fetchall()
    
    # for i in range(len(result)):
    #     gl.append(result[i]['itemname'])

    
    # xaxis=["ethnic1","ethnic2","ethnic3","ethnic4"]
    # strength=[gl.count("ethnic1"),gl.count("ethnic2"),gl.count("ethnic3"),gl.count("ethnic4")]
    # fig = plt.figure(figsize =(10,7)) 
    # plt.pie(strength, labels = xaxis)
    # chart=FigureCanvasTkAgg(fig,frame3)
    # chart.get_tk_widget().pack()
    
    
    frame1.pack(fill="both",side="left")
    frame2.pack(fill="both",side="top")
    frame3.pack(fill="both",side="top")
    
    met1.mainloop()    
def ethinic3():
    met2=tk.Toplevel()
    met2.geometry("1000x1000+0+0")
    met2.title("ETHINIC 3")
    
    frame2=tk.Frame(met2,height=400,width=500)
    frame2.config(background="misty rose")
    desc=tk.PhotoImage(file="eth3desc.gif")
    tk.Label(frame2,image=desc).pack()
    
    frame1=tk.Frame(met2,height=900,width=500)
    frame1.config(background="misty rose")
    
    e2=tk.PhotoImage(file="eth3.gif")
    
    tk.Label(frame1).pack()
    lab=tk.Label(frame1,
                 image=e2).pack()
    tk.Label(frame1).pack()
    tk.Label(frame1,
             text="Rs.780").pack()

    tk.Label(frame1).pack()
    
    b1s=tk.Button(frame1,
                  text="Add to cart",
                  highlightbackground="yellow",
                  command=insert,
                  bg="snow").pack()
    
    tk.Label(frame1).pack()
    
    press1aa=tk.Button(frame1,
                    text="GO to cart",
                    command=cart,
                    highlightbackground="yellow",
                    bg="snow").pack()
    
    def purchase(size):
        key="ethnic 3"
        value=[780,size]
        dict[key]=value
        l.append(value[0])
        
    tk.Label(frame1,text="Size:").pack(side="left")
        
    global size 
    
    size=tk.Button(frame1,
                  text="X small",
                  bg="snow",
                  command=lambda: purchase("  size: X small")).pack(padx=10,pady=5,side="left")
    
    size=tk.Button(frame1,
                    text="small",
                    bg="snow",
                    command=lambda: purchase("  size: small")).pack(padx=10,pady=10,side="left")
    size=tk.Button(frame1,
                    text="medium",
                    bg="snow",
                    command=lambda: purchase(" size: medium")).pack(padx=10,pady=15,side="left")
    size=tk.Button(frame1,
                    text="large",
                    bg="snow",
                    command=lambda: purchase(" size: large")).pack(padx=10,pady=20,side="left")
    size=tk.Button(frame1,
                   text="X large",
                   bg="snow",
                    command=lambda: purchase(" size: X large")).pack(padx=10,pady=25,side="left")
    size=tk.Button(frame1,
                   text="XX large",
                   bg="snow",
                    command=lambda: purchase(" size: XX large")).pack(padx=10,pady=25,side="left")
    
    global name
    global price
    global model
    global category
    global gender
    gender='M'
    name="ethnic3"
    price="Rs.780"
    model="H003"
    category="ethinic"
    
    global maincat
    maincat="men ethnic wear"
    
    categories(model,category,maincat,gender)
    
    frame3=tk.Frame(met2,height=500,width=500)
    
    # query="SELECT * FROM products WHERE CATEGORY=%s"
    # value=category
    # cursor.execute(query,value)
    # connection.commit()
    # result=cursor.fetchall()
    
    # for i in range(len(result)):
    #     gl.append(result[i]['itemname'])

    
    # xaxis=["ethnic1","ethnic2","ethnic3","ethnic4"]
    # strength=[gl.count("ethnic1"),gl.count("ethnic2"),gl.count("ethnic3"),gl.count("ethnic4")]
    # fig = plt.figure(figsize =(10,7))  
    # plt.pie(strength, labels = xaxis)
    # chart=FigureCanvasTkAgg(fig,frame3)
    # chart.get_tk_widget().pack()
    
    
    frame1.pack(fill="both",side="left")
    frame2.pack(fill="both",side="top")
    frame3.pack(fill="both",side="top")
    met2.mainloop()   
def ethinic4():
    met3=tk.Toplevel()
    met3.geometry("1000x1000+0+0")
    met3.title("ETHINIC 4")
    
    frame2=tk.Frame(met3,height=400,width=500)
    frame2.config(background="misty rose")
    desc=tk.PhotoImage(file="eth4desc.gif")
    tk.Label(frame2,image=desc).pack()
    
    frame1=tk.Frame(met3,height=900,width=500)
    frame1.config(background="misty rose")
    
    e3=tk.PhotoImage(file="eth4.gif")
    
    tk.Label(frame1).pack()
    lab=tk.Label(frame1,
                 image=e3).pack()
    
    tk.Label(frame1).pack()
    tk.Label(frame1,
             text="Rs.645").pack()
    
    tk.Label(frame1).pack()
    
    b1s=tk.Button(frame1,
                  text="Add to cart",
                  highlightbackground="yellow",
                  command=insert,
                  bg="snow").pack()
    tk.Label(frame1).pack()

    press1aa=tk.Button(frame1,
                    text="GO to cart",
                    command=cart,
                    highlightbackground="yellow",
                    bg="snow").pack()
    
    def purchase(size):
        key="ethnic 4"
        value=[645,size]
        dict[key]=value
        l.append(value[0])
        
    tk.Label(frame1,text="Size:").pack(side="left")
        
    global size 
    
    size=tk.Button(frame1,
                  text="X small",
                  bg="snow",
                  command=lambda: purchase("  size: X small")).pack(padx=10,pady=5,side="left")
    
    size=tk.Button(frame1,
                    text="small",
                    bg="snow",
                    command=lambda: purchase("  size: small")).pack(padx=10,pady=10,side="left")
    size=tk.Button(frame1,
                    text="medium",
                    bg="snow",
                    command=lambda: purchase(" size: medium")).pack(padx=10,pady=15,side="left")
    size=tk.Button(frame1,
                    text="large",
                    bg="snow",
                    command=lambda: purchase(" size: large")).pack(padx=10,pady=20,side="left")
    size=tk.Button(frame1,
                   text="X large",
                   bg="snow",
                    command=lambda: purchase(" size: X large")).pack(padx=10,pady=25,side="left")
    size=tk.Button(frame1,
                   text="XX large",
                   bg="snow",
                    command=lambda: purchase(" size: XX large")).pack(padx=10,pady=25,side="left")
    
    global name
    global price
    global model
    global category
    global gender
    gender='M'
    name="ethnic4"
    price="Rs.645"
    model="H004"
    category="ethinic"
    
    global maincat
    maincat="men ethnic wear"
    
    categories(model,category,maincat,gender)
    
    frame3=tk.Frame(met3,height=500,width=500)
    
    # query="SELECT * FROM products WHERE CATEGORY=%s"
    # value=category
    # cursor.execute(query,value)
    # connection.commit()
    # result=cursor.fetchall()
    
    # for i in range(len(result)):
    #     gl.append(result[i]['itemname'])

    
    # xaxis=["ethnic1","ethnic2","ethnic3","ethnic4"]
    # strength=[gl.count("ethnic1"),gl.count("ethnic2"),gl.count("ethnic3"),gl.count("ethnic4")]
    # fig = plt.figure(figsize =(10,7))  
    # plt.pie(strength, labels = xaxis)
    # chart=FigureCanvasTkAgg(fig,frame3)
    # chart.get_tk_widget().pack()
    
    
    frame1.pack(fill="both",side="left")
    frame2.pack(fill="both",side="top")
    frame3.pack(fill="both",side="top")

    met3.mainloop()  
def men_kurtas():
    wink=tk.Toplevel()
    wink.geometry("1700x800+0+0")
    wink.config(background="seashell3")
    wink.title("KURTA SETS")
    
    m=tk.PhotoImage(file="ethcaption.gif")
    tk.Label(wink,
             image=m).pack(side=tk.TOP)
    
    e=tk.PhotoImage(file="eth1.gif")
    et=tk.Button(wink,
                 text="ethinic 1",
                 image=e,
                 compound="top",
                 command=ethinic1).pack(side=tk.LEFT)
        
    e1=tk.PhotoImage(file="eth2.gif")
    et1=tk.Button(wink,
                  text="ethinic 2",
                  image=e1,
                  compound="top",
                  command=ethinic2).pack(side=tk.LEFT)
        
    e2=tk.PhotoImage(file="eth3.gif")
    et2=tk.Button(wink,
                  text="ethinic 3",
                  image=e2,
                  compound="top",
                  command=ethinic3).pack(side=tk.LEFT)
        
    e3=tk.PhotoImage(file="eth4.gif")
    et3=tk.Button(wink,
                  text="ethinic 4",
                  image=e3,
                  compound="top",
                  command=ethinic4).pack(side=tk.LEFT)
        
    wink.mainloop()  
def women_fashion():
    
    screen=tk.Toplevel()
    screen.geometry("1700x800+0+0")
    screen.title("STYLES FOR HER")
    screen.config(background="pale turquoise")
    frame=tk.Frame(screen,height=900,width=300)
    frame.config(background="aquamarine2")
    def women_western():
        
        screen3=tk.Frame(screen,height=900,width=1000)
        screen3.config(background="pale turquoise")
        
        
        pic=tk.PhotoImage(file="tee.gif")
        tk.Label(screen3,
                 text="WOMEN'S WESTERN:-",
                 bg="aquamarine").pack()
    
        ww=tk.Button(screen3,
                     text="tops & sweatshirts",
                     image=pic,
                     compound="right",
                     command=tops,
                     bg="peach puff").pack(side="top")
        
        pic1=tk.PhotoImage(file="dress.gif")
        ww1=tk.Button(screen3,
                     text="dresses and gowns",
                     image=pic1,
                     compound="right",
                     command=dresses,
                     bg="peach puff").pack(side="top")
        
        pic2=tk.PhotoImage(file="jeans.gif")
        ww2=tk.Button(screen3,
                     text="denims & trousers",
                      image=pic2,
                      compound="right",
                      command=jeans,
                      bg="peach puff").pack(side="top")
        
        screen3.pack(fill="both",side="left",padx=150)
        screen3.mainloop()
    
    
    def women_ethinic():
        screen7=tk.Frame(screen,height=900,width=1000)
        screen7.config(background="pale turquoise")
        
        khome=tk.PhotoImage(file="suit.gif")
        tk.Label(screen7,
                 text="WOMEN'S ETHINIC:-",
                 bg="aquamarine").pack()
    
        we=tk.Button(screen7,
                     text="kurtas and suit sets",
                     image=khome,
                     compound="right",
                     command=kurta,
                     bg="peach puff").pack(side="top")
        
        lhome=tk.PhotoImage(file="lehenga.gif")
        we2=tk.Button(screen7,
                      text="sarees & lehengas",
                      image=lhome,
                      compound="right",
                      command=lehenga,
                      bg="peach puff").pack(side="top")
        
        screen7.pack(fill="both",side="left",padx=150)
        screen7.mainloop()
    
    img3=tk.PhotoImage(file="western wear.gif")
    tk.Label(frame,
             text="WOMEN:-").pack(side="top")
    
    wf=tk.Button(frame,
                 text="western wear",
                 fg="dark green",
                 image=img3,
                 compound="right",
                 command=women_western).pack(side="top")
    
    
    img4=tk.PhotoImage(file="wew.gif")
    wf1=tk.Button(frame,
                  text="ethinic wear",
                  fg="dark green",
                  image=img4,
                  compound="right",
                  command=women_ethinic).pack(side="left")
    
    frame.pack(fill="both",side="left")
    screen.mainloop() 
def men_fashion():
    screen1=tk.Toplevel()
    screen1.geometry("1700x800+0+0")
    screen1.config(background="pale turquoise")
    screen1.title("STYLES FOR HIM")
    frame=tk.Frame(screen1,height=900,width=300)
    frame.config(background="aquamarine2")
    
    def men_western():
        
        screen4=tk.Frame(screen1,height=900,width=1000)
        screen4.config(background="pale turquoise")
        
        d=tk.PhotoImage(file="shirtss.gif")
        tk.Label(screen4,
                 text="MEN'S WESTERN:-",
                 bg="aquamarine").pack()
        
        mw=tk.Button(screen4,
                     text="shirts & T-shirts",
                     image=d,
                     compound="right",
                     command=shirt,
                     bg="peach puff").pack(side="top")
        
        dd=tk.PhotoImage(file="jeans.gif")
        mw2=tk.Button(screen4,
                     text="denims & trousers",
                     image=dd,
                     compound="right",
                     command=denims,
                     bg="peach puff").pack(side="top")
        
        screen4.pack(fill="both",side="left",padx=150)
        screen4.mainloop()
        
    def men_ethinic():
        screen=tk.Frame(screen1,height=900,width=1000)
        screen.config(background="pale turquoise")
        
        mkhome=tk.PhotoImage(file="menkurta.gif")
        tk.Label(screen,
                 text="MEN'S ETHINIC:-",
                 bg="aquamarine").pack()
    
        we=tk.Button(screen,
                     text="kurta sets",
                     image=mkhome,
                     compound="right",
                     command=men_kurtas,
                     bg="peach puff").pack(side="top")
        
        screen.pack(fill="both",side="left",padx=150)
        screen.mainloop()
        
    img7=tk.PhotoImage(file="mww.gif")
    tk.Label(frame,
             text="MEN:-").pack()
    mf=tk.Button(frame,
                 text="western wear",
                 fg="dark green",
                 image=img7,
                 compound="right",
                 command=men_western).pack(side="top")
    
    imgg8=tk.PhotoImage(file="mew.gif")
    mf1=tk.Button(frame,
                 text="ethinic wear",
                 fg="dark green",
                 image=imgg8,
                 compound="right",
                 command=men_ethinic).pack(side="left")
    frame.pack(fill="both",side="left")
    screen1.mainloop()
def fashion():
    window=tk.Toplevel()
    window.geometry("1000x800")
    window.config(bg="peach puff")
    window.title("WHAT WOULD YOU LIKE TO SHOP FOR ?")
    heading=tk.PhotoImage(file="shopbycategory.gif")
    tk.Label(window,image=heading).pack(side=tk.TOP)
    img=tk.PhotoImage(file="fashion.gif")
    
    bt=tk.Button(window,
                 text="WOMEN",
                 font=50,
                 height=300,
                 width=400,
                 image=img,
                 fg="dark blue",
                 bg="plum2",
                 compound="bottom",
                 command=women_fashion).pack(side=tk.LEFT)
    
    img2=tk.PhotoImage(file="mf.gif")
    bt1=tk.Button(window,
                 text="MEN",
                 font=50,
                 height=300,
                 width=400,
                 image=img2,
                 fg="dark blue",
                 bg="plum2",
                 compound="bottom",
                 command=men_fashion).pack(side=tk.RIGHT)
    window.mainloop()

cover=tk.PhotoImage(file="coverpage.gif")
root.title("WELCOME TO MY E-COMMERCE WEBSITE MANAGEMENT SYSTEM")
b1=tk.Button(frame,
             height=3000,
             width=2000,
             text="START",
             image=cover,
             fg="red",
             bg="light green",
             command=fashion).pack(padx=200,pady=50)

root.mainloop()
cursor.close()
connection.close()