from tkinter import *
from tkinter.ttk import *
from PIL import ImageTk, Image
import login
import changepassword
import managecontact


class HomeWindow(Tk):

    def __init__(self, *args, **kwargs):
        Tk.__init__(self, *args, **kwargs)

        self.title("Home")
        self.state('zoomed')
        Icon = PhotoImage(file="Images/user.png")
        self.iconphoto(False, Icon)

        s = Style()
        s.configure('Header.TFrame', background="#935ac4")

        header_frame = Frame(self, style='Header.TFrame')
        header_frame.pack(fill=X)

        s.configure('Header.TLabel', background="#935ac4", foreground='white', font=('Arial', 25))

        header_label = Label(header_frame, text='My Contact Book', style='Header.TLabel')
        header_label.pack(pady=10)

        navigation_frame = Frame(self, style='Header.TFrame')
        navigation_frame.pack(side=RIGHT, fill=Y)

        s.configure('Navigation.TButton', background="#935ac4", foreground='#935ac4', width=20, font=('Arial', 15))

        manage_contact_button = Button(navigation_frame, text='Manage Contacts', style='Navigation.TButton', command=self.manage_contacts_button_click)
        manage_contact_button.pack(ipady=10, pady=1)

        change_password_button = Button(navigation_frame, text='Change Password', style='Navigation.TButton', command=self.change_password_button_click)
        change_password_button.pack(ipady=10, pady=1)

        logout_button = Button(navigation_frame, text='Logout', style='Navigation.TButton', command=self.logout_button_click)
        logout_button.pack(ipady=10, pady=1)

        s.configure('Navigation.TFrame', background="white")

        self.content_frame = Frame(self, style='Navigation.TFrame')
        self.content_frame.pack(fill=BOTH, expand=TRUE)

        managecontact.ManageContactsFrame(self.content_frame)

    def logout_button_click(self):
        self.destroy()
        login.LoginWindow()

    def change_password_button_click(self):
        for inner_frame in self.content_frame.winfo_children():
            inner_frame.destroy()
        changepassword.ChangePasswordFrame(self.content_frame)

    def manage_contacts_button_click(self):
        for inner_frame in self.content_frame.winfo_children():
            inner_frame.destroy()
        managecontact.ManageContactsFrame(self.content_frame)


if __name__ == "__main__":
    home = HomeWindow()
    home.mainloop()
