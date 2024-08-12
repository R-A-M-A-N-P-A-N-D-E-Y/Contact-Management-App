from tkinter import *
from tkinter.ttk import *
from sqlite3 import *
from tkinter import messagebox


class ManageContactsFrame(Frame):

    def __init__(self, parent):
        Frame.__init__(self, parent)

        s = Style()
        s.configure('TFrame', background='white')
        s.configure('TLabel', background='white', font=('Arial', 15))
        s.configure('TButton', font=('Arial', 15))
        s.configure('Treeview.Heading', font=('Arial', 15))
        s.configure('Treeview', font=('Arial', 14), rowheight=25)

        self.update_delete_contact_frame = Frame(self)

        self.pack(fill=BOTH, expand=True)

        self.con = connect('Contacts.db')
        self.cur = self.con.cursor()

        self.create_view_all_contacts_frame()

    def fill_contacts_treeview(self):
        for contact in self.contact_treeview.get_children():
            self.contact_treeview.delete(contact)

        contacts = self.cur.fetchall()
        for contact in contacts:
            self.contact_treeview.insert('', END, values=contact)

    def create_view_all_contacts_frame(self):
        self.view_all_contact_frame = Frame(self)
        self.view_all_contact_frame.place(relx=.5, rely=.5, anchor=CENTER)

        add_new_contact_button = Button(self.view_all_contact_frame, text='Add New Contact',
                                        command=self.add_new_contact_button_click)
        add_new_contact_button.grid(row=0, column=3, sticky=E, pady=25)

        search_name_label = Label(self.view_all_contact_frame, text='Name :')
        search_name_label.grid(row=1, column=0)

        self.search_name_entry = Entry(self.view_all_contact_frame, font=('Arial', 15), width=32)
        self.search_name_entry.grid(row=1, column=1, pady=10)
        self.search_name_entry.bind('<KeyRelease>', self.name_entry_key_release)

        search_phone_no_label = Label(self.view_all_contact_frame, text='Phone no. :')
        search_phone_no_label.grid(row=1, column=2)

        self.search_phone_no_entry = Entry(self.view_all_contact_frame, font=('Arial', 15), width=32)
        self.search_phone_no_entry.grid(row=1, column=3, pady=10)
        self.search_phone_no_entry.bind('<KeyRelease>', self.phone_no_entry_key_release)

        self.contact_treeview = Treeview(self.view_all_contact_frame,
                                         columns=('name', 'phone_no', 'email_id', 'address'),
                                         show='headings')
        self.contact_treeview.heading('name', text='Name', anchor=W)
        self.contact_treeview.heading('phone_no', text='Phone Number', anchor=W)
        self.contact_treeview.heading('email_id', text='Email Id', anchor=W)
        self.contact_treeview.heading('address', text='Address', anchor=W)
        self.contact_treeview.column('name', width=250)
        self.contact_treeview.column('phone_no', width=200)
        self.contact_treeview.column('email_id', width=250)
        self.contact_treeview.column('address', width=200)
        self.contact_treeview.bind('<<TreeviewSelect>>', self.contacts_treeview_row_selection)

        self.cur.execute('select * from Contact')
        self.fill_contacts_treeview()

        self.contact_treeview.grid(row=2, column=0, columnspan=4)

    def add_new_contact_button_click(self):
        self.view_all_contact_frame.destroy()

        self.add_new_contact_frame = Frame(self)
        self.add_new_contact_frame.place(relx=.5, rely=.5, anchor=CENTER)

        name_label = Label(self.add_new_contact_frame, text='Name :')
        name_label.grid(row=0, column=0, sticky=E)

        self.name_entry = Entry(self.add_new_contact_frame, width=30, font=('Arial', 15))
        self.name_entry.grid(row=0, column=1, pady=5)

        phone_no_label = Label(self.add_new_contact_frame, text='Phone no. :')
        phone_no_label.grid(row=1, column=0, sticky=E)

        self.phone_no_entry = Entry(self.add_new_contact_frame, width=30, font=('Arial', 15))
        self.phone_no_entry.grid(row=1, column=1, pady=5)

        email_id_label = Label(self.add_new_contact_frame, text='Email Id :')
        email_id_label.grid(row=2, column=0, sticky=E)

        self.email_id_entry = Entry(self.add_new_contact_frame, width=30, font=('Arial', 15))
        self.email_id_entry.grid(row=2, column=1, pady=5)

        address_label = Label(self.add_new_contact_frame, text='Address :')
        address_label.grid(row=3, column=0, sticky=E)

        self.address_entry = Entry(self.add_new_contact_frame, width=30, font=('Arial', 15))
        self.address_entry.grid(row=3, column=1, pady=5)

        add_button = Button(self.add_new_contact_frame, text='Add', width=30, command=self.add_button_click)
        add_button.grid(row=4, column=1, pady=5)

    def add_button_click(self):
        self.cur.execute('select * from Contact where EmailId = ?', (self.email_id_entry.get(),))
        contact = self.cur.fetchone()

        if contact is None:
            self.cur.execute('insert into Contact (Name, PhoneNumber, EmailId, Address) values (?, ?, ?, ?)',
                             (self.name_entry.get(), self.phone_no_entry.get(), self.email_id_entry.get(),
                              self.address_entry.get()))
            self.con.commit()
            messagebox.showinfo('Success Message', 'Contact details added successfully.')
            self.add_new_contact_frame.destroy()
            self.create_view_all_contacts_frame()
        else:
            messagebox.showerror('Error Message', 'Contact details are already added')

        self.add_new_contact_frame.destroy()
        self.create_view_all_contacts_frame()

    def name_entry_key_release(self, event):
        self.cur.execute('select * from Contact where Name like ?', ('%' + self.search_name_entry.get() + '%',))
        self.fill_contacts_treeview()

    def phone_no_entry_key_release(self, event):
        self.cur.execute('select * from Contact where PhoneNumber like ?', ('%' + self.search_phone_no_entry.get() + '%',))
        self.fill_contacts_treeview()

    def contacts_treeview_row_selection(self, event):
        contact = self.contact_treeview.item(self.contact_treeview.selection())['values']
        self.view_all_contact_frame.destroy()

        self.update_delete_contact_frame = Frame(self)
        self.update_delete_contact_frame.place(relx=.5, rely=.5, anchor=CENTER)

        name_label = Label(self.update_delete_contact_frame, text='Name :')
        name_label.grid(row=0, column=0, sticky=E)

        self.name_entry = Entry(self.update_delete_contact_frame, width=30, font=('Arial', 15))
        self.name_entry.grid(row=0, column=1, pady=5)
        self.name_entry.insert(END, contact[0])

        phone_no_label = Label(self.update_delete_contact_frame, text='Phone no. :')
        phone_no_label.grid(row=1, column=0, sticky=E)

        self.phone_no_entry = Entry(self.update_delete_contact_frame, width=30, font=('Arial', 15))
        self.phone_no_entry.grid(row=1, column=1, pady=5)
        self.phone_no_entry.insert(END, contact[1])

        email_id_label = Label(self.update_delete_contact_frame, text='Email Id :')
        email_id_label.grid(row=2, column=0, sticky=E)

        self.email_id_entry = Entry(self.update_delete_contact_frame, width=30, font=('Arial', 15))
        self.email_id_entry.grid(row=2, column=1, pady=5)
        self.old_email_id = contact[2]
        self.email_id_entry.insert(END, contact[2])

        address_label = Label(self.update_delete_contact_frame, text='Address :')
        address_label.grid(row=3, column=0, sticky=E)

        self.address_entry = Entry(self.update_delete_contact_frame, width=30, font=('Arial', 15))
        self.address_entry.grid(row=3, column=1, pady=5)
        self.address_entry.insert(END, contact[3])

        update_button = Button(self.update_delete_contact_frame, text='Update', width=30,
                               command=self.update_button_click)
        update_button.grid(row=4, column=1, pady=5)

        delete_button = Button(self.update_delete_contact_frame, text='Delete', width=30, command=self.delete_button_click)
        delete_button.grid(row=5, column=1, pady=5)

    def update_button_click(self):
        self.cur.execute('update Contact set Name = ?, PhoneNumber = ?, EmailId = ?, Address = ? where EmailId = ?',
                         (self.name_entry.get(), self.phone_no_entry.get(), self.email_id_entry.get(),
                          self.address_entry.get(), self.old_email_id))
        self.con.commit()
        messagebox.showinfo('Success Message', 'Contact details updated.')
        self.update_delete_contact_frame.destroy()
        self.create_view_all_contacts_frame()

    def delete_button_click(self):
        if messagebox.askquestion('Confirmation Message', 'Are you sure to delete?') == 'yes':
            self.cur.execute('delete from Contact where EmailId = ?', (self.old_email_id,))
            self.con.commit()
            messagebox.showinfo('Success Message', 'Contact details deleted.')
        self.update_delete_contact_frame.destroy()
        self.create_view_all_contacts_frame()
