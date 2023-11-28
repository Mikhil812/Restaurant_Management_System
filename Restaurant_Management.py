from tkinter import *
import sqlite3 
import time
import random
import tkinter.font as tkFont
import matplotlib.pyplot as plt

# Database thingy ----------------------------------
con = sqlite3.connect('Hotel_Management.db')
cur = con.cursor()
# cur.execute('CREATE TABLE ItemandCost(Item TEXT,Cost INTEGER)')
# cur.execute('CREATE TABLE SelectedOrder(CustomerID INTEGER,TableNo INTEGER)')

item_list = [('Chicken Tikka ',200),('Butter Chicken',150),('Methi Paratha ',30),('Roti Roti     ',20),('Steam Rice     ',120)]
food_items = []
cost_items = []
for i in item_list:
    food_items.append(i[0])
    cost_items.append(i[1])
    cur.execute('INSERT INTO ItemandCost VALUES(?,?)',(i[0],i[1]))

# print(food_items)
# print(cost_items)

customer_id_list = []
table_no_list = []
cost_list = []
def add():
    global cost_list
    global item_selected
    choice = str(item_selected.get())
    
    for i in range(len(food_items)):
        if choice == food_items[i]:
            cost_list.append(cost_items[i])
    
    cur.execute('SELECT Item ,Cost FROM ItemandCost WHERE Item = ?',(choice,))
    store = cur.fetchall()

    new_risit = text_receipt.get('0.0',END)
    text_receipt.delete('0.0',END)

    new_risit = new_risit + '   ' + store[0][0] + '          ' + str(store[0][1]) 
    text_receipt.insert('0.0',new_risit)

def receipt():
    global cost_list

    cur.execute('INSERT INTO SelectedOrder VALUES(?,?)',(entry_customer_id.get(),entry_table_no.get()))
    customer_id_list.append(int(entry_customer_id.get()))
    table_no_list.append(int(entry_table_no.get()))

    total_sum = sum(cost_list)
    text_receipt.insert(END,'\n-------------------------------------------------')
    text_receipt.insert('0.0','\t\tItem Added : \t\t\t Cost :\n')
    text_receipt.insert('0.0','-------------------------------------------------')

    text_receipt.insert(END,'\n-------------------------------------------------')
    text_receipt.insert(END,'\n\t\t\tTOTAL : ' + str(total_sum) + ' Rs')
    text_receipt.insert(END,'\n-------------------------------------------------')
    text_receipt.insert(END,'\t\tService Tax (10%) : ' + str(0.1*total_sum) + ' Rs')
    text_receipt.insert(END,'\n\tGST (15%)         : ' + str(0.15*total_sum) + ' Rs')
    text_receipt.insert(END,'\n-------------------------------------------------')
    text_receipt.insert(END,'\n\n\t\t\tBill : ' + str(total_sum + (0.1*total_sum) + (0.15*total_sum)) + ' Rs')
    text_receipt.insert(END,'\n-------------------------------------------------')

def close():
    window.destroy()

def delete():
    global food_items
    global cost_items
    global cost_list

    print(cost_list)

    store = text_receipt.get('0.0',END)
    text_receipt.delete('0.0',END)

    delete_list = store.split('\n')
    
    for i in range(0,len(food_items)):
        if food_items[i] in delete_list[-2]:
            cost_list.remove(cost_items[i])
    print(cost_list)
    # del delete_list[-1]
    del delete_list[-2]

    str = "\n ".join(delete_list)
    print(str)
    text_receipt.insert('0.0',str)  

def new():
    global cost_list
    global date

    cost_list = []
    entry_current_date.delete(0,END)
    entry_customer_id.delete(0,END)
    entry_table_no.delete(0,END)
    text_receipt.delete('0.0',END)

    entry_current_date.insert(END,date)
    entry_customer_id.insert(0,str(random.randint(90,100)))
    entry_table_no.insert(0,str(random.randint(1,10)))

def graph():
    global customer_id_list
    global table_no_list

    print(customer_id_list)
    print(table_no_list)   

    plt.title('Stats',fontdict = {'family':'serif','size':20,'color':'b'})
    plt.xlabel("Customer Id's",fontdict = {'family':'serif','size':20,'color':'b'})
    plt.ylabel("Table Number's",fontdict = {'family':'serif','size':20,'color':'b'})
    plt.xlim(90,102)
    plt.ylim(0,12)
    plt.plot(customer_id_list,table_no_list,marker = 'o')
    plt.grid(axis='both')
    plt.show()

window = Tk()
window.geometry('1000x700')
window.resizable(0,0)

# Welcome to Mini Punjab
label_1 = Label(window,text = "Welcome to Mini Punjab",font = ('arial',30),justify=CENTER)
label_1.pack()

# Menu Frame (First Frame) --------------------------
frame_menu = Frame(window,bg = 'pink')
frame_menu.place(x = 0,y=50,height=400,width=500)

label_menu = Label(frame_menu,text = "Menu",font = ('arial',38))
label_menu.place(x = 20,y = 10)

item_selected = StringVar()
item_selected.set('Select an item : ')

helv18 = tkFont.Font(family='Helvetica', size=18)
option_menu = OptionMenu(frame_menu,item_selected,*food_items)
option_menu.config(font=helv18)
option_menu.place(x = 220,y = 16)


# Display Frame (Second Frame) ------------------------
frame_disp = Frame(window,bg = 'light green')
frame_disp.place(x = 500,y = 50,height=700,width = 500)

label_customer_id = Label(frame_disp,text = "Customer Id : ",font = ('arial',15))
label_customer_id.place(x = 10,y = 10)

entry_customer_id = Entry(frame_disp)        
entry_customer_id.place(x = 250,y = 12.5)
entry_customer_id.config(width=30,justify=CENTER)
entry_customer_id.insert(0,str(random.randint(90,100)))

label_table_no = Label(frame_disp,text = "Table No.     : ",font = ('arial',15))
label_table_no.place(x = 10,y = 50)

entry_table_no = Entry(frame_disp)        
entry_table_no.place(x = 250,y = 55)
entry_table_no.config(width=30,justify=CENTER)
entry_table_no.insert(0,str(random.randint(1,10)))

label_date = Label(frame_disp,text='Date            : ',font = ('arial',15))
label_date.place(x = 10, y = 90)

date = time.strftime('%d/%m/%Y')
entry_current_date = Entry(frame_disp)
entry_current_date.insert(END,date)
entry_current_date.config(width=30,justify=CENTER)
entry_current_date.place(x = 250,y = 96)

button_receipt = Button(frame_disp,text = 'Receipt        : ',font = ('arial',15),width=11,command=receipt)    # Can be made a button
button_receipt.place(x = 10,y = 130)

text_receipt = Text(frame_disp)
text_receipt.place(x = 50,y = 185,height=350,width=400)

button_add = Button(frame_disp,text = 'Add',font = ('arial',15),command=add)
button_add.place(x = 30,y = 565)

button_delete = Button(frame_disp,text = 'Delete',font = ('arial',15),command=delete)
button_delete.place(x = 130,y = 565)

payment_option_selected = StringVar()
payment_option_selected.set('Pay by : ')
payment_options_list = ['Cash','Debit Card','Credit Card','Gpay','Cheque']
menu_payment = OptionMenu(frame_disp,payment_option_selected,*payment_options_list)
menu_payment.config(height=2)
menu_payment.place(x = 250,y = 560)

button_close = Button(frame_disp,text = 'Close',font = ('arial',15),command = close)
button_close.place(x = 400,y=560)

# Analysis Frame (Third Frame)
anal_frame = Frame(window,bg = "light blue")
anal_frame.place(x = 0,y = 350,height=350,width=500)

button_new = Button(anal_frame,text = 'New',font = ('arial',15),width=11,command=new)
button_new.place(x = 20,y = 10)

button_graph = Button(anal_frame,text = 'Analysis',font = ('arial',15),width=11,command=graph)
button_graph.place(x = 300,y = 10)

text_stats = Text(anal_frame)
text_stats.config(height = 15,width = 50)
text_stats.place(x = 30,y = 80)

window.mainloop()