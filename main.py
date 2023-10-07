from tkinter import *
from tkinter import messagebox
import random
import pyperclip
import json


# ---------------------------- PASSWORD GENERATOR ------------------------------- #
def generate_password():
    letters = ['a', 'b', 'c', 'd', 'e', 'f', 'g', 'h', 'i', 'j', 'k', 'l', 'm', 'n', 'o', 'p', 'q', 'r', 's', 't', 'u',
               'v', 'w', 'x', 'y', 'z', 'A', 'B', 'C', 'D', 'E', 'F', 'G', 'H', 'I', 'J', 'K', 'L', 'M', 'N', 'O', 'P',
               'Q', 'R', 'S', 'T', 'U', 'V', 'W', 'X', 'Y', 'Z']
    numbers = ['0', '1', '2', '3', '4', '5', '6', '7', '8', '9']
    symbols = ['!', '#', '$', '%', '&', '(', ')', '*', '+']

    nr_letters = random.randint(8, 10)
    nr_symbols = random.randint(2, 4)
    nr_numbers = random.randint(2, 4)

    password_list = ([random.choice(letters) for _ in range(nr_letters)] +
                     [random.choice(symbols) for _ in range(nr_symbols)] +
                     [random.choice(numbers) for _ in range(nr_numbers)])

    random.shuffle(password_list)

    password = "".join(password_list)

    password_input.insert(0, password)
    pyperclip.copy(password)


# ---------------------------- SAVE PASSWORD ------------------------------- #


def save_password():
    website = website_input.get().capitalize()
    email = username_input.get()
    password = password_input.get()
    new_data = {
        website: {
            "email": email,
            "password": password,
        }
    }

    if len(website) == 0 or len(password) == 0:
        messagebox.showerror(title="Ooops", message="Please dont leave any fields empty!")
    else:
        try:
            # look for the json file
            with open("data.json", mode="r") as data_file:
                # Reading old data
                data = json.load(data_file)

        except FileNotFoundError:
            # if th efile is not yet created, create one
            with open("data.json", mode="w") as data_file:
                # Saving updated data:
                json.dump(new_data, data_file, indent=4)
        else:
            # Updating old data with new data:
            data.update(new_data)

            with open("data.json", mode="w") as data_file:
                # Saving updated data:
                json.dump(data, data_file, indent=4)

        finally:

            website_input.delete(0, END)
            password_input.delete(0, END)


# -----------------------------SEARCH FUNCTION-------------------------- #


def find_password():
    website = website_input.get().capitalize()
    try:
        with open("data.json", "r") as data_file:
            data = json.load(data_file)

    except FileNotFoundError:
        messagebox.showerror(title="Error", message="No Data File Found.")

    else:
        if website in data:
            email = data[website]["email"]
            password = data[website]["password"]
            pyperclip.copy(password)
            messagebox.showinfo(title=f"{website}", message=f"Email: {email}\nPassword: {password}")

        else:
            messagebox.showerror(title="Error", message=f"No details for {website} exist.")

        website_input.delete(0, END)

    finally:
        website_input.delete(0, END)


# ---------------------------- UI SETUP ------------------------------- #

window = Tk()
window.title("Password Manager")
window.config(padx=50, pady=50)

canvas = Canvas(width=200, height=200)
logo = PhotoImage(file="logo.png")
canvas.create_image(100, 100, image=logo)
canvas.grid(row=0, column=1)

website_label = Label(text="Website:")
website_label.grid(row=1, column=0)

website_input = Entry(width=33)
website_input.grid(row=1, column=1)
website_input.focus()

search_button = Button(text="Search", width=14, command=find_password)
search_button.grid(row=1, column=2)

username_label = Label(text="Email/Username:")
username_label.grid(row=2, column=0)

username_input = Entry(width=52)
username_input.grid(row=2, column=1, columnspan=2)
username_input.insert(0, "fake@gmail.com")

password_label = Label(text="Password:")
password_label.grid(row=3, column=0)

password_input = Entry(width=33)
password_input.grid(row=3, column=1)

password_button = Button(text="Generate Password", command=generate_password)
password_button.grid(row=3, column=2)

add_button = Button(text="Add", width=44, command=save_password)
add_button.grid(row=4, column=1, columnspan=2)

window.mainloop()
