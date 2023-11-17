import tkinter as tk
import datetime
from functools import partial
import pymysql

def main(connection,cursor,user_id):
    global l
    global pay
    global gl
    global dict
    global order_id
    pay=[]
    gl=[]#graph list
    dict={}
    l=[]

    root=tk.Tk()
    root.geometry("1600x800+0+0")
    root.configure (bg="turquoise")

    frame=tk.Frame(root).pack()
    cover=tk.PhotoImage(file="./images/coverpage.gif")
    root.title("ONLINE SHOPPING WEBSITE")
    cursor.execute("delete from cart_items;")
    b1=tk.Button(frame,height=3000,width=2000,text="START",image=cover,fg="red",bg="light green",command=partial(fashion,connection,cursor)).pack(padx=200,pady=50)
    insert_later(connection,cursor,user_id)
    root.mainloop()

def get_next_order_id(cursor):
    # Function to get the next order ID based on the current maximum order ID in the database
    cursor.execute("SELECT MAX(Order_ID) FROM Orders")
    result = cursor.fetchone()[0]
    if result:
        next_order_id = int(result[1:]) + 1
    else:
        next_order_id = 1
    return f'O{next_order_id:03}'
        
def insert_order(order_id, eta,connection,cursor): 
    # Function to insert values into the Orders table
    payment_id = ''
    user_id = ''
    insert_orders_query = f"""
        INSERT INTO Orders(Order_ID, ETA)
        VALUES('{order_id}', '{eta}');
    """
    cursor.execute(insert_orders_query)
    connection.commit()



def debcred(connection,cursor):
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
                 command=partial(final,connection,cursor))
    
    go.grid(row=3, column=1)

    masterss.mainloop()
#input gift card information
def giftcard(connection,cursor):
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
                 command=partial(final,connection,cursor))
    
    go.grid(row=3, column=1)

    masters.mainloop()

def final(connection,cursor):
    final = tk.Tk()
    final.geometry("500x500+0+0")
    final.config(bg="aqua")
    final.title("THANK YOU !!")
    current_date = datetime.datetime.now().date()
    eta = current_date + datetime.timedelta(days=5)
    eta_str = eta.strftime('%Y-%m-%d')
    order_id= get_next_order_id(cursor)

    insert_order(order_id,eta_str,connection,cursor)
    
    message= "Thank you for shopping with us \nYour order will be delivered on,",eta_str,"\n\nPLEASE DO VISIT US AGAIN "
    msg = tk.Message(final, text = message)
    msg.config(bg='aqua', font=('times', 24, 'italic'))
    msg.pack()
    tk.mainloop() 


def fashion(connection,cursor):
    window=tk.Toplevel()
    window.geometry("1000x800")
    window.config(bg="peach puff")
    window.title("WHAT WOULD YOU LIKE TO SHOP FOR ?")
    heading=tk.PhotoImage(file="./images/shopbycategory.gif")
    tk.Label(window,image=heading).pack(side=tk.TOP)
    img=tk.PhotoImage(file="./images/fashion.gif")
    bt=tk.Button(window,text="WOMEN",font=50,height=300,width=400,image=img,fg="dark blue",bg="plum2",compound="bottom",command=partial(women_fashion,connection,cursor)).pack(side=tk.LEFT)
    img2=tk.PhotoImage(file="./images/mf.gif")
    bt1=tk.Button(window,text="MEN",font=50,height=300,width=400,image=img2,fg="dark blue",bg="plum2",compound="bottom",command=partial(men_fashion,connection,cursor)).pack(side=tk.RIGHT)
    window.mainloop()


def men_western(connection,cursor,screen1): 
    screen4=tk.Frame(screen1,height=900,width=1000)
    screen4.config(background="pale turquoise")
    d=tk.PhotoImage(file="./images/shirtss.gif")
    tk.Label(screen4,text="MEN'S WESTERN:-",bg="aquamarine").pack()
    mw=tk.Button(screen4,text="shirts & T-shirts",image=d,compound="right",command=partial(shirt,connection,cursor),bg="peach puff").pack(side="top")
    dd=tk.PhotoImage(file="./images/jeans.gif")
    mw2=tk.Button(screen4,text="denims & trousers",image=dd,compound="right",command=partial(denims,connection,cursor),bg="peach puff").pack(side="top")
    screen4.pack(fill="both",side="left",padx=150)
    screen4.mainloop()
    

def men_ethnic(connection,cursor,screen1):
    screen=tk.Frame(screen1,height=900,width=1000)
    screen.config(background="pale turquoise")
    mkhome=tk.PhotoImage(file="./images/menkurta.gif")
    tk.Label(screen,text="MEN'S ETHNIC:-",bg="aquamarine").pack()
    we=tk.Button(screen,text="kurta sets",image=mkhome,compound="right",command=partial(men_kurtas,connection,cursor),bg="peach puff").pack(side="top")
    screen.pack(fill="both",side="left",padx=150)
    screen.mainloop()


def men_fashion(connection,cursor):
    screen1=tk.Toplevel()
    screen1.geometry("1700x800+0+0")
    screen1.config(background="pale turquoise")
    screen1.title("STYLES FOR HIM")
    frame=tk.Frame(screen1,height=900,width=300)
    frame.config(background="aquamarine2")   
    img7=tk.PhotoImage(file="./images/mww.gif")
    tk.Label(frame,text="MEN:-").pack()
    mf=tk.Button(frame,text="western wear",fg="dark green",image=img7,compound="right",command=partial(men_western,connection,cursor,screen1)).pack(side="top")
    imgg8=tk.PhotoImage(file="./images/mew.gif")
    mf1=tk.Button(frame,text="ethnic wear",fg="dark green",image=imgg8,compound="right",command=partial(men_ethnic,connection,cursor,screen1)).pack(side="left")
    frame.pack(fill="both",side="left")
    screen1.mainloop()


def women_western(connection,cursor,screen):
    screen3=tk.Frame(screen,height=900,width=1000)
    screen3.config(background="pale turquoise")
    pic=tk.PhotoImage(file="./images/tee.gif")
    tk.Label(screen3,text="WOMEN'S WESTERN:-",bg="aquamarine").pack()
    ww=tk.Button(screen3,text="tops & sweatshirts",image=pic,compound="right",command=partial(tops,connection,cursor),bg="peach puff").pack(side="top")
    pic1=tk.PhotoImage(file="./images/dress.gif")
    ww1=tk.Button(screen3,text="dresses and gowns",image=pic1,compound="right",command=partial(dresses,connection,cursor),bg="peach puff").pack(side="top")
    pic2=tk.PhotoImage(file="./images/jeans.gif")
    ww2=tk.Button(screen3,text="denims & trousers",image=pic2,compound="right",command=partial(jeans,connection,cursor),bg="peach puff").pack(side="top")
    screen3.pack(fill="both",side="left",padx=150)
    screen3.mainloop()
    
    
def women_ethnic(connection,cursor,screen):
    screen7=tk.Frame(screen,height=900,width=1000)
    screen7.config(background="pale turquoise")
    khome=tk.PhotoImage(file="./images/suit.gif")
    tk.Label(screen7,text="WOMEN'S ETHNIC:-",bg="aquamarine").pack()
    we=tk.Button(screen7,text="kurtas and suit sets",image=khome,compound="right",command=partial(kurta,connection,cursor),bg="peach puff").pack(side="top")
    lhome=tk.PhotoImage(file="./images/lehenga.gif")
    we2=tk.Button(screen7,text="sarees & lehengas",image=lhome,compound="right",command=partial(lehenga,connection,cursor),bg="peach puff").pack(side="top")
    screen7.pack(fill="both",side="left",padx=150)
    screen7.mainloop()

def women_fashion(connection,cursor):
    screen=tk.Toplevel()
    screen.geometry("1700x800+0+0")
    screen.title("STYLES FOR HER")
    screen.config(background="pale turquoise")
    frame=tk.Frame(screen,height=900,width=300)
    frame.config(background="aquamarine2")
    img3=tk.PhotoImage(file="./images/western wear.gif")
    tk.Label(frame,text="WOMEN:-").pack(side="top")
    wf=tk.Button(frame,text="western wear",fg="dark green",image=img3,compound="right",command=partial(women_western,connection,cursor,screen)).pack(side="top") 
    img4=tk.PhotoImage(file="./images/wew.gif")
    wf1=tk.Button(frame,text="ethnic wear",fg="dark green",image=img4,compound="right",command=partial(women_ethnic,connection,cursor,screen)).pack(side="left")
    frame.pack(fill="both",side="left")
    screen.mainloop() 


def tops(connection,cursor):
    wink=tk.Toplevel()
    wink.geometry("1700x800+0+0")
    wink.config(background="seashell3")
    wink.title("TOPS,TEES AND SWEATSHIRTS")
    frame1=tk.Frame(wink,height=400,width=850)
    frame2=tk.Frame(wink,height=400,width=850)
    disp=tk.PhotoImage(file="./images/top1a.gif")
    btop=tk.Button(frame1,text="top1",image=disp,compound="top",command=partial(clothing_component,connection,cursor,"TOP 1","./images/top1adesc.gif","./images/top1a.gif",600,"top1","A001","tops","F","women western wear")).pack(side=tk.LEFT)
    disp1=tk.PhotoImage(file="./images/top2a.gif")
    btop1=tk.Button(frame1,text="top2",image=disp1,compound="top",command=partial(clothing_component,connection,cursor,"TOP 2","./images/top2adesc.gif","./images/top2a.gif",500,"top2","A002","tops","F","women western wear")).pack(side=tk.LEFT)
    disp2=tk.PhotoImage(file="./images/top3a.gif")
    btop2=tk.Button(frame1,text="top3",image=disp2,compound="top",command=partial(clothing_component,connection,cursor,"TOP 3","./images/top3adesc.gif","./images/top3a.gif",650,"top3","A003","tops","F","women western wear")).pack(side=tk.LEFT)
    disp3=tk.PhotoImage(file="./images/top4a.gif")
    btop3=tk.Button(frame2,text="top4",image=disp3,compound="top",command=partial(clothing_component,connection,cursor,"TOP 4","./images/top4adesc.gif","./images/top4a.gif",600,"top4","A004","tops","F","women western wear")).pack(side=tk.LEFT)
    disp4=tk.PhotoImage(file="./images/top5a.gif")
    btop4=tk.Button(frame2,text="top5",image=disp4,compound="top",command=partial(clothing_component,connection,cursor,"TOP 5","./images/top5adesc.gif","./images/top5a.gif",400,"top5","A005","tops","F","women western wear")).pack(side=tk.LEFT)
    frame1.pack(side="top",padx=200)
    frame2.pack(side="top",padx=400)
    wink.mainloop() 


def dresses(connection,cursor):
    choice2=tk.Toplevel()
    choice2.geometry("1700x800+0+0")
    choice2.config(background="seashell3")
    choice2.title("DRESSES AND GOWNS")
    m=tk.PhotoImage(file="./images/dresscaption.gif")
    tk.Label(choice2,image=m).pack(side=tk.TOP)
    dispa=tk.PhotoImage(file="./images/dress1a.gif")
    btopa=tk.Button(choice2,text="dress1",image=dispa,compound="top",command=partial(clothing_component,connection,cursor,"DRESS 1","./images/dress1adesc.gif","./images/dress1a.gif",900,"dress1","B001","dresses","F","women western wear")).pack(side=tk.LEFT)
    dispb=tk.PhotoImage(file="./images/dress2a.gif")
    btopb=tk.Button(choice2,text="dress2",image=dispb,compound="top",command=partial(clothing_component,connection,cursor,"DRESS 2","./images/dress2adesc.gif","./images/dress2a.gif",700,"dress2","B002","dresses","F","women western wear")).pack(side=tk.LEFT)
    dispc=tk.PhotoImage(file="./images/dress3a.gif")
    btopc=tk.Button(choice2,text="dress3",image=dispc,compound="top",command=partial(clothing_component,connection,cursor,"DRESS 3","./images/dress3adesc.gif","./images/dress3a.gif",800,"dress3","B003","dresses","F","women western wear")).pack(side=tk.LEFT)
    dispd=tk.PhotoImage(file="./images/dress4a.gif")
    btopd=tk.Button(choice2,text="dress4",image=dispd,compound="top",command=partial(clothing_component,connection,cursor,"DRESS 4","./images/dress4adesc.gif","./images/dress4a.gif",800,"dress4","B004","dresses","F","women western wear")).pack(side=tk.LEFT)
    choice2.mainloop()

def jeans(connection,cursor):
    choice3=tk.Toplevel()
    choice3.geometry("1700x800")
    choice3.config(background="seashell3")
    choice3.title("DENIMS AND TROUSERS")
    m=tk.PhotoImage(file="./images/jeanscaption.gif")
    tk.Label(choice3,image=m).pack(side=tk.TOP)
    disp6=tk.PhotoImage(file="./images/jeans1a.gif")
    btop6=tk.Button(choice3,text="jeans 1",image=disp6,compound="top",command=partial(clothing_component,connection,cursor,"JEANS 1","./images/jeans1adesc.gif","./images/jeans1a.gif",800,"jeans1","C001","jeans","F","women western wear")).pack(side=tk.LEFT)
    disp7=tk.PhotoImage(file="./images/jeans2a.gif")
    btop7=tk.Button(choice3,text="jeans2",image=disp7,compound="top",command=partial(clothing_component,connection,cursor,"JEANS 2","./images/jeans2adesc.gif","./images/jeans2a.gif",1050,"jeans2","C002","jeans","F","women western wear")).pack(side=tk.LEFT)
    disp8=tk.PhotoImage(file="./images/jeans3a.gif")
    btop8=tk.Button(choice3,text="jeans3",image=disp8,compound="top",command=partial(clothing_component,connection,cursor,"JEANS 3","./images/jeans3adesc.gif","./images/jeans3a.gif",900,"jeans3","C003","jeans","F","women western wear")).pack(side=tk.LEFT)
    disp10=tk.PhotoImage(file="./images/jeans5a.gif")
    btop10=tk.Button(choice3,text="jeans4",image=disp10,compound="top",command=partial(clothing_component,connection,cursor,"JEANS 4","./images/jeans4adesc.gif","./images/jeans4a.gif",1000,"jeans4","C004","jeans","F","women western wear")).pack(side=tk.LEFT)
    choice3.mainloop()

def kurta(connection,cursor):
    kurti=tk.Toplevel()
    kurti.geometry("1700x800+0+0")
    kurti.config(background="seashell3")
    kurti.title("KURTAS AND SUIT SETS")
    m=tk.PhotoImage(file="./images/kurtacaption.gif")
    tk.Label(kurti,image=m).pack(side=tk.TOP)
    k1=tk.PhotoImage(file="./images/kurta1.gif")
    kt1=tk.Button(kurti,text="kurta 1",image=k1,compound="top",command=partial(clothing_component,connection,cursor,"KURTA 1","./images/kurta1adesc.gif","./images/kurta1a.gif",900,"kurta1","D001","kurtas","F","women ethnic wear")).pack(side=tk.LEFT)
    k2=tk.PhotoImage(file="./images/kurta2.gif")
    kt2=tk.Button(kurti,text="kurta 2",image=k2,compound="top",command=partial(clothing_component,connection,cursor,"KURTA 2","./images/kurta2adesc.gif","./images/kurta2a.gif",600,"kurta2","D002","kurtas","F","women ethnic wear")).pack(side=tk.LEFT)
    k3=tk.PhotoImage(file="./images/kurta3.gif")
    kt3=tk.Button(kurti,text="kurta 3",image=k3,compound="top",command=partial(clothing_component,connection,cursor,"KURTA 3","./images/kurta3adesc.gif","./images/kurta3a.gif",800,"kurta3","D003","kurtas","F","women ethnic wear")).pack(side=tk.LEFT)
    k4=tk.PhotoImage(file="./images/kurta4.gif")
    kt4=tk.Button(kurti,text="kurta 4",image=k4,compound="top",command=partial(clothing_component,connection,cursor,"KURTA 4","./images/kurta4adesc.gif","./images/kurta4a.gif",1000,"kurta4","D004","kurtas","F","women ethnic wear")).pack(side=tk.LEFT)
    kurti.mainloop() 

def lehenga(connection,cursor):
    l=tk.Toplevel()
    l.geometry("1700x800+0+0")
    l.config(background="seashell3")
    l.title("SAREES AND LEHENGAS")
    m=tk.PhotoImage(file="./images/lehengacaption.gif")
    tk.Label(l,image=m).pack(side=tk.TOP)
    l1=tk.PhotoImage(file="./images/lehenga1.gif")
    ln1=tk.Button(l,text="lehenga 1",image=l1,compound="top",command=partial(clothing_component,connection,cursor,"LEHENGA 1","./images/lehenga1desc.gif","./images/lehenga1.gif",3000,"lehenga1","E001","lehengas","F","women ethnic wear")).pack(side=tk.LEFT)
    l2=tk.PhotoImage(file="./images/lehenga2.gif")
    ln2=tk.Button(l,text="lehenga 2",image=l2,compound="top",command=partial(clothing_component,connection,cursor,"LEHENGA 2","./images/lehenga2desc.gif","./images/lehenga2.gif",5000,"lehenga2","E002","lehengas","F","women ethnic wear")).pack(side=tk.LEFT)
    l3=tk.PhotoImage(file="./images/saree1.gif")
    ln3=tk.Button(l,text="saree 1",image=l3,compound="top",command=(clothing_component,connection,cursor,"SAREE 1","./images/saree1desc.gif","./images/saree1.gif",4000,"saree1","E003","lehengas","F","women ethnic wear")).pack(side=tk.LEFT)
    l4=tk.PhotoImage(file="./images/saree2.gif")
    ln4=tk.Button(l,text="saree 2",image=l4,compound="top",command=(clothing_component,connection,cursor,"SAREE 2","./images/saree2desc.gif","./images/saree2.gif",3000,"saree2","E004","lehengas","F","women ethnic wear")).pack(side=tk.LEFT)
    l.mainloop() 

def men_kurtas(connection,cursor):
    wink=tk.Toplevel()
    wink.geometry("1700x800+0+0")
    wink.config(background="seashell3")
    wink.title("KURTA SETS")
    m=tk.PhotoImage(file="./images/ethcaption.gif")
    tk.Label(wink,image=m).pack(side=tk.TOP)
    e=tk.PhotoImage(file="./images/eth1.gif")
    et=tk.Button(wink,text="ethnic 1",image=e,compound="top",command=partial(clothing_component,connection,cursor,"ETHNIC 1","./images/eth1desc.gif","./images/eth1.gif",1500,"ethnic1","H001","ethnic","M","men ethnic wear")).pack(side=tk.LEFT)
    e1=tk.PhotoImage(file="./images/eth2.gif")
    et1=tk.Button(wink,text="ethnic 2",image=e1,compound="top",command=partial(clothing_component,connection,cursor,"ETHNIC 2","./images/eth2desc.gif","./images/eth2.gif",980,"ethnic2","H002","ethnic","M","men ethnic wear")).pack(side=tk.LEFT)
    e2=tk.PhotoImage(file="./images/eth3.gif")
    et2=tk.Button(wink,text="ethnic 3",image=e2,compound="top",command=partial(clothing_component,connection,cursor,"ETHNIC 3","./images/eth3desc.gif","./images/eth3.gif",780,"ethnic3","H003","ethnic","M","men ethnic wear")).pack(side=tk.LEFT)
    e3=tk.PhotoImage(file="./images/eth4.gif")
    et3=tk.Button(wink,text="ethnic 4",image=e3,compound="top",command=partial(clothing_component,connection,cursor,"ETHNIC 4","./images/eth4desc.gif","./images/eth4.gif",1000,"ethnic1","H004","ethnic","M","men ethnic wear")).pack(side=tk.LEFT)
    wink.mainloop()  

def shirt(connection,cursor):
    tee=tk.Toplevel()
    tee.geometry("1700x800+0+0")
    tee.config(background="seashell3")
    tee.title("SHIRTS AND T-SHIRTS")
    m=tk.PhotoImage(file="./images/shirtcaption.gif")
    tk.Label(tee,image=m).pack(side=tk.TOP)
    e=tk.PhotoImage(file="./images/shirt1.gif")
    et=tk.Button(tee,text="shirt 1",image=e,compound="top",command=partial(clothing_component,connection,cursor,"SHIRT 1","./images/shirt1desc.gif","./images/shirt1.gif",1500,"shirt1","F001","shirts","M","men western wear")).pack(side=tk.LEFT)
    e1=tk.PhotoImage(file="./images/shirt2.gif")
    et1=tk.Button(tee,text="shirt 2",image=e1,compound="top",command=partial(clothing_component,connection,cursor,"SHIRT 2","./images/shirt2desc.gif","./images/shirt2.gif",900,"shirt2","F002","shirts","M","men western wear")).pack(side=tk.LEFT)
    e2=tk.PhotoImage(file="./images/shirt3.gif")
    et2=tk.Button(tee,text="shirt 3",image=e2,compound="top",command=partial(clothing_component,connection,cursor,"SHIRT 3","./images/shirt3desc.gif","./images/shirt3.gif",650,"shirt3","F003","shirts","M","men western wear")).pack(side=tk.LEFT)
    e3=tk.PhotoImage(file="./images/shirt4.gif")
    et3=tk.Button(tee,text="shirt 4",image=e3,compound="top",command=partial(clothing_component,connection,cursor,"SHIRT 4","./images/shirt4desc.gif","./images/shirt4.gif",700,"shirt1","F004","shirts","M","men western wear")).pack(side=tk.LEFT)
    tee.mainloop() 

def denims(connection,cursor):
    tee=tk.Toplevel()
    tee.geometry("1700x800+0+0")
    tee.config(background="seashell3")
    tee.title("DENIMS AND TROUSERS")
    m=tk.PhotoImage(file="./images/mjeanscaption.gif")
    tk.Label(tee,image=m).pack(side=tk.TOP)
    e=tk.PhotoImage(file="./images/mjeans1.gif")
    et=tk.Button(tee,text="denim 1",image=e,compound="top",command=partial(clothing_component,connection,cursor,"DENIM 1","./images/mjeans1desc.gif","./images/mjeans1.gif",650,"denim1","G001","denims","M","men western wear")).pack(side=tk.LEFT)
    e1=tk.PhotoImage(file="./images/mjeans2.gif")
    et1=tk.Button(tee,text="denim 2",image=e1,compound="top",command=partial(clothing_component,connection,cursor,"DENIM 2","./images/mjeans2desc.gif","./images/mjeans2.gif",900,"denim2","G002","denims","M","men western wear")).pack(side=tk.LEFT)
    e2=tk.PhotoImage(file="./images/mjeans3.gif")
    et2=tk.Button(tee,text="denim 3",image=e2,compound="top",command=partial(clothing_component,connection,cursor,"DENIM 3","./images/mjeans3desc.gif","./images/mjeans3.gif",1000,"denim3","G003","denims","M","men western wear")).pack(side=tk.LEFT)
    e3=tk.PhotoImage(file="../images/mjeans4.gif")
    et3=tk.Button(tee,text="denim 4",image=e3,compound="top",command=partial(clothing_component,connection,cursor,"DENIM 4","./images/mjeans4desc.gif","./images/mjeans4.gif",700,"denim4","G004","denims","M","men western wear")).pack(side=tk.LEFT)
    tee.mainloop() 


def purchase(size,amount,key,):
    value=[amount,size]
    dict[key]=value
    l.append(value[0])

def clothing_component(connection,cursor,title,img_desc,img_fit,amount,name,model,category,gender,maincat):
    met3=tk.Toplevel()
    met3.geometry("1000x1000+0+0")
    met3.title(title)
    frame2=tk.Frame(met3,height=400,width=500)
    frame2.config(background="misty rose")
    desc=tk.PhotoImage(file=img_desc)
    tk.Label(frame2,image=desc).pack()
    frame1=tk.Frame(met3,height=900,width=500)
    frame1.config(background="misty rose")
    e3=tk.PhotoImage(file=img_fit)
    tk.Label(frame1).pack()
    lab=tk.Label(frame1,image=e3).pack()
    tk.Label(frame1).pack()
    tk.Label(frame1,text="Rs."+str(amount)).pack()
    tk.Label(frame1).pack()
    b1s=tk.Button(frame1,text="Add to cart",highlightbackground="yellow",command=partial(product,connection,cursor,name,amount,model,category),bg="snow").pack()
    tk.Label(frame1).pack()
    press1aa=tk.Button(frame1,text="GO to cart",command=partial(cart,connection,cursor),highlightbackground="yellow",bg="snow").pack()
    tk.Label(frame1,text="Size:").pack(side="left")
    global size 
    size=tk.Button(frame1,text="X small",bg="snow",command=partial(purchase,"  size: X small",amount,name)).pack(padx=10,pady=5,side="left")
    size=tk.Button(frame1,text="small",bg="snow",command=partial(purchase,"  size: small",amount,name)).pack(padx=10,pady=10,side="left")
    size=tk.Button(frame1,text="medium",bg="snow",command=partial(purchase," size: medium",amount,name)).pack(padx=10,pady=15,side="left")
    size=tk.Button(frame1,text="large",bg="snow",command=partial(purchase," size: large",amount,name)).pack(padx=10,pady=20,side="left")
    size=tk.Button(frame1,text="X large",bg="snow",command=partial(purchase," size: X large",amount,name)).pack(padx=10,pady=25,side="left")
    size=tk.Button(frame1,text="XX large",bg="snow", command=partial(purchase," size: XX large",amount,name)).pack(padx=10,pady=25,side="left")
    categories(model,category,maincat,gender,connection,cursor)
    frame3=tk.Frame(met3,height=500,width=500)
    frame1.pack(fill="both",side="left")
    frame2.pack(fill="both",side="top")
    frame3.pack(fill="both",side="top")
    met3.mainloop() 

def categories(model,category,maincat,gender,connection,cursor):
    try:
        read_query="insert into categories(category_id, sub_category, category, gender) values(%s,%s,%s,%s)"
        values=(model,category,maincat,gender)
        cursor.execute(read_query,values)
        connection.commit()
        print("new record inserted") 

    except pymysql.Error:
        print("Already exists")


def cart(connection,cursor):
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
                  command=partial(pay_method,connection,cursor)).pack()
    

def payment_db(connection,cursor,mode,func):
    read_query="insert into payment_info(mode_of_payment,total) values(%s,%s)"
    values=(mode,add)
    cursor.execute(read_query,values)
    connection.commit()
    print("payment method inserted")
    func(connection,cursor)

def insert_later(connection,cursor,user_id):
    payment_id_finder = "select max(payment_id) from payment_info"
    cursor.execute(payment_id_finder)
    payment_id=cursor.fetchone()
    print("payment_id: ",payment_id)
    update1 = "update Orders set payment_id=%s where order_id=%s"
    values1=(payment_id,order_id)
    cursor.execute(update1,values1)
    connection.commit()
    update2 = "update Orders set user_id=%s where order_id=%s"
    values2=(user_id,order_id)
    cursor.execute(update1,values1)
    connection.commit()
    


def payment_window(connection,cursor,txt,pm,v,mode,func,val):
    tk.Radiobutton(pm, 
                  text= txt,
                  padx = 20, 
                  variable=v, 
                  value=val,
                  command=partial(payment_db,connection,cursor,mode,func)).pack(anchor=tk.W)
    
def pay_method(connection,cursor):
    pm = tk.Tk()
    pm.geometry("500x500+0+0")
    pm.config(bg="RosyBrown1")
    pm.title("PAYMENT METHOD")
    
    v = tk.IntVar()
    tk.Label(pm, 
            text="payment method:-",
            justify = tk.LEFT,
            padx = 20).pack()
    
    pay = payment_window(connection,cursor,"debit card",pm,v,mode = "debit card", func = debcred,val=1)
    pay = payment_window(connection,cursor,"credit card",pm,v,mode = "credit card", func = debcred,val=2)
    pay = payment_window(connection,cursor,"gift card balance",pm,v,mode = "gift card", func =giftcard,val=3)
    pay = payment_window(connection,cursor,"cash on delivery",pm,v,mode = "debit card", func = final,val=4)




def product(connection,cursor,name,amount,model,category):
    read_query="insert into products(itemname,price,category_id,product_description) values(%s,%s,%s,%s)"
    values=(name,amount,model,category)
    cursor.execute(read_query,values)
    connection.commit()
    print("new record inserted")


