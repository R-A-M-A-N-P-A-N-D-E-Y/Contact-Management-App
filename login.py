from tkinter import *
from tkinter.ttk import *
from PIL import ImageTk, Image
from tkinter import messagebox
from sqlite3 import *
import home


class LoginWindow(Tk):

    def __init__(self, *args, **kwargs):
        Tk.__init__(self, *args, **kwargs)

        self.title("Login")
        self.geometry("400x500")

        Icon = PhotoImage(file="Images/user.png")
        self.iconphoto(False, Icon)

        s = Style()
        s.configure('Header.TFrame', background='#935ac4')

        header_frame = Frame(self, style='Header.TFrame')
        header_frame.pack(fill=X)

        s.configure('Header.TLabel', background='#935ac4', foreground='white', font=('Arial', 25))

        header_label = Label(header_frame, text="My Contact Book", style='Header.TLabel')
        header_label.pack(pady=10)

        s.configure('Content.TFrame', background='white')

        content_frame = Frame(self, style='Content.TFrame')
        content_frame.pack(fill=BOTH, expand=True)

        self.login_frame = Frame(content_frame, style='Content.TFrame')
        self.login_frame.place(relx=.5, rely=.5, anchor=CENTER)

        s.configure('Login.TLabel', background='white', font=('Arial', 15))

        img = (Image.open("Images/user1.png"))
        resized_image = img.resize((80, 70))
        content_frame.user = ImageTk.PhotoImage(resized_image)
        login_user = Label(self.login_frame, image=content_frame.user, background='white', foreground='white',
                           style='Login.TLabel')
        login_user.image = content_frame.user
        login_user.grid(row=0, column=1, pady=10)

        login_label = Label(self.login_frame, text='Login', background='white', foreground="#935ac4", font=('Arial', 20))
        login_label.grid(row=1, column=1, pady=10)

        img = (Image.open("Images/user.png"))
        resized_image = img.resize((25, 25))
        content_frame.user = ImageTk.PhotoImage(resized_image)
        username_label = Label(self.login_frame, image=content_frame.user, background='white', foreground='white')
        username_label.grid(row=2, column=0, pady=5, padx=3)

        self.username_entry = Entry(self.login_frame, font=('Arial', 15), width=12)
        self.username_entry.grid(row=2, column=1, pady=5)

        img = (Image.open("Images/lock.png"))
        resized_image = img.resize((25, 25))
        content_frame.lock = ImageTk.PhotoImage(resized_image)
        password_label = Label(self.login_frame, image=content_frame.lock, background='white', foreground='white',
                               style='Login.TLabel')
        password_label.grid(row=3, column=0, pady=5, padx=3)

        s.configure('Login.TButton', foreground='#935ac4', font=('Arial', 15))

        self.password_entry = Entry(self.login_frame, font=('Arial', 15), width=12)
        self.password_entry.grid(row=3, column=1, pady=5)

        login_button = Button(self.login_frame, text="Login", style='Login.TButton', command=self.login_button_click)
        login_button.grid(row=4, column=1, pady=5)
        login_button.bind('<Return>')

        # ========= show/hide password ==================================================================
        self.show_image = ImageTk.PhotoImage(file='images/show.png')

        self.hide_image = ImageTk.PhotoImage(file='images/hide.png')

        show_button = Button(self.login_frame, image=self.show_image, command=self.show)
        self.password_entry.config(show='*')
        show_button.grid(row=3, column=2, padx=5)

    def show(self):
        hide_button = Button(self.login_frame, image=self.hide_image, command=self.hide)
        hide_button.grid(row=3, column=2)
        self.password_entry.config(show='')

    def hide(self):
        show_button = Button(self.login_frame, image=self.show_image, command=self.show)
        show_button.grid(row=3, column=2)
        self.password_entry.config(show='*')

    def login_button_click(self, event = None):
        con = connect('Contacts.db')
        cur = con.cursor()
        cur.execute("select * from Login where Username = ? and Password = ?", (self.username_entry.get(), self.password_entry.get()))
        row = cur.fetchone()
        if row is not None:
            # messagebox.showinfo("Success Message", "Logged in successfully")
            self.destroy()
            home.HomeWindow()
        else:
            messagebox.showerror("Error Message", "Incorrect username/password")


if __name__ == "__main__":
    login = LoginWindow()
    login.mainloop()
