import tkinter as tk
from tkinter import ttk, messagebox
import mysql.connector as mysql

conn =mysql.connect(host="localhost",user="root",password="",database="mysqldb")
cursor = conn.cursor()

def dbconnect():
    cursor.execute("create table if not exists student(id INT, name TEXT, age INT, mbl TEXT)")
    messagebox.showinfo("Sucess", "Table Created Succesfully")

def add_new():
    eid.delete(0,tk.END)
    ename.delete(0,tk.END)
    eage.delete(0,tk.END)
    embl.delete(0,tk.END)
    eid.focus()

    ins.config(state=tk.NORMAL)
    upd.config(state=tk.DISABLED)
    dele.config(state=tk.DISABLED)
def insert_data():
    id = eid.get()
    name =ename.get()
    age = eage.get()
    mbl = embl.get()

    if id=="" or name=="" or age=="" or mbl=="":
        messagebox("Mendatory", "All fields are mendotary")
    
    else:
        cursor.execute("Insert into student(id,name,age,mbl)values(%s,%s,%s,%s)",(id,name,age,mbl))
        conn.commit()
        messagebox.showinfo("Insert Success","Record Inserted Sucess")
    display_data()
    add_new()

def to_upper(event):
    falg = ename.get()
    ename.delete(0,tk.END)
    ename.insert(0, falg.upper())

def to_digit(event):
    mobile = embl.get()

    if not mobile.isdigit or len(mobile)!=10:
            messagebox.showerror("Error","mobile number must be 10 digits")
            embl.select_range(0,tk.END)
            embl.focus_set()

        
def display_data():
    for row in tree.get_children():
        tree.delete(row)
    
    cursor.execute("Select *from Student")

    for row in cursor.fetchall():
        tree.insert("",tk.END,values=row)

def select_data(event):
    selected = tree.focus()
    values = tree.item(selected,"values")

    eid.delete(0,tk.END)
    ename.delete(0,tk.END)
    eage.delete(0,tk.END)
    embl.delete(0,tk.END)

    eid.insert(0, values[0])
    ename.insert(0, values[1])
    eage.insert(0, values[2])
    embl.insert(0, values[3])

    cbtn.config(state=tk.NORMAL)
    ins.config(state=tk.DISABLED)
    #dele.config(state=tk.DISABLED)

def update_data():
    selected = tree.focus()

    id = tree.item(selected,"values")[0]
    name = ename.get().strip()
    age = eage.get().strip()
    mbl=embl.get().strip()

    cursor.execute("Update student SET name=%s, age=%s, mbl=%s where id=%s",(name,age,mbl,id))
    conn.commit()
    messagebox.showinfo("Updated","Update Success")
    display_data()

def delete_data():
    selecetd = tree.focus()

    id = tree.item(selecetd,"values")[0]

    cursor.execute("Delete from student where id=%s",(id,))
    messagebox.showinfo("Deleted","Delete Success")
    display_data()

root = tk.Tk()
root.geometry("500x500")
frame=tk.Frame(root)
frame.pack(pady=20)
lid = tk.Label(frame, text="Enter Student ID:").pack(side='left', padx=10)
eid = tk.Entry(frame, width=10)
eid.pack(side="left", padx=5)
lname = tk.Label(frame, text="Enter Student Name:").pack(side='left', padx=10)
ename = tk.Entry(frame, width=15)
ename.pack(side="left", padx=5)
frame2=tk.Frame(root)
frame2.pack(pady=20)
lage = tk.Label(frame2, text="Enter Student Age:").pack(side='left', padx=10)
eage = tk.Entry(frame2, width=10)
eage.pack(side="left", padx=5)
lmbl = tk.Label(frame2, text="Enter Student Mobile:").pack(side='left', padx=10)
embl = tk.Entry(frame2, width=15)
embl.pack(side="left", padx=5)
frame1 = tk.Frame(root)
frame1.pack(pady=20)
cbtn = tk.Button(frame1, command=add_new, text="Add New", width=15)
cbtn.pack(side="left", padx=5)
ins = tk.Button(frame1, command=insert_data, text="Insert", width=15)
ins.pack(side="left", padx=5)
upd = tk.Button(frame1, command=update_data, text="Update", width=15)
upd.pack(side="left", padx=5)
dele = tk.Button(frame1, command=delete_data, text="Delete", width=15)
dele.pack(side="left", padx=5)

tree_frame = ttk.LabelFrame(root, text="Student Records")
tree_frame.pack()
cols=("Student ID", "Name","Age","Mobile")
tree = ttk.Treeview(tree_frame, columns=cols, show='headings')

for col in cols:
    tree.heading(col, text=col)
    tree.column(col, width=80)
tree.pack(padx=20, pady=20)
display_data()

ename.bind("<FocusOut>", to_upper)
embl.bind("<FocusOut>", to_digit)
tree.bind("<ButtonRelease-1>", select_data)

cbtn.config(state=tk.DISABLED)
root.mainloop()


