from tkinter import * #* incl only class & constants
from tkinter import messagebox #for modules
import random
import pyperclip
import json

# CONSTANTS
BG_COLOR = "#e3e3e3"
BTN_COLOR = "gray"

window = Tk()
window.title("Password Manager")
window.config(padx=20, pady=20, bg=BG_COLOR)

canvas = Canvas(width=200, height=200, bg=BG_COLOR, highlightthickness=0)
pw_img = PhotoImage(file="logo.png")
canvas.create_image(130, 100, image=pw_img)
canvas.grid(column=1, row=0)


# ---------------------------- PASSWORD GENERATOR ------------------------------- #
def generate_pw_handler():
	letters = ['a', 'b', 'c', 'd', 'e', 'f', 'g', 'h', 'i', 'j', 'k', 'l', 'm', 'n', 'o', 'p', 'q', 'r', 's', 't', 'u', 'v',
						 'w', 'x', 'y', 'z', 'A', 'B', 'C', 'D', 'E', 'F', 'G', 'H', 'I', 'J', 'K', 'L', 'M', 'N', 'O', 'P', 'Q', 'R',
						 'S', 'T', 'U', 'V', 'W', 'X', 'Y', 'Z']
	numbers = ['0', '1', '2', '3', '4', '5', '6', '7', '8', '9']
	symbols = ['!', '#', '$', '%', '&', '(', ')', '*', '+']

	pw_char_list = []

	for n in range(random.randint(8, 10)):
		pw_char_list += random.choice(letters)

	for n in range(random.randint(2, 4)):
		pw_char_list += random.choice(numbers)

	for n in range(random.randint(2, 4)):
		pw_char_list += random.choice(symbols)

	# print(pw_char_list)
	random.shuffle(pw_char_list)  # shuffle in place
	generated_text = ''.join(pw_char_list)
	# print(final_from_list)

	# clear prev generated pw
	password_input.delete(0, END)

	# insert new generated pw
	password_input.insert(0, generated_text)


def copy_pw_handler():
	pw_input = password_input.get()
	pyperclip.copy(pw_input)

# ---------------------------- SAVE PASSWORD ------------------------------- #
def save_pw_handler():
	eu_input = email_user_input.get()
	w_input = web_input.get().lower()
	pw_input = password_input.get()

	new_entry = {
		w_input: {
			"user": eu_input,
			"pw":pw_input
		}
	}

	if not (eu_input.strip() and w_input.strip() and pw_input.strip()):
		messagebox.showinfo(title="Oops!", message="All fields are required!")
	else:
		is_ok = messagebox.askokcancel(title=w_input, message=f"These are the details entered: \nEmail: {eu_input} \nPassword: {pw_input} \nIs it ok to save?")

		if is_ok:
			# with open("wp.txt", "a") as file:
				# file.write(f"{eu_input} | {w_input} | {pw_input}\n")
			try:
				with open("wp.json", "r") as file:
					# reading old data
					data = json.load(file)
			except FileNotFoundError:
				with open("wp.json", "w") as file:
					# save updated data
					json.dump(new_entry, file, indent=4)
			else:
				# update old data with new data
				data.update(new_entry)
				with open("wp.json", "w") as file:
					# save updated data
					json.dump(data, file, indent=4)
			finally:
				web_input.delete(0, END)
				password_input.delete(0, END)

# ---------------------------- SEARCH CREDENTIAL ------------------------------- #
def search_cred_handler():
	w_input = web_input.get().lower()
	try:
		with open("wp.json", "r") as file:
			data = json.load(file)
			# found_cred = data[w_input]
	except FileNotFoundError:
		messagebox.showinfo(title="Error", message=f"There is no entry to lookup on.")
	# except KeyError: # would work
		# messagebox.showinfo(title="Error", message=f"No credentials found for {w_input}.")
	else:
		# handle neg scenario with if else as much as possible instead of exception.
		if w_input in data:
			found_cred = data[w_input]
			messagebox.showinfo(title=f"{w_input}", message=f"\nEmail: {found_cred['user']} \nPassword: {found_cred['pw']} \n** Password has been auto-copied to clipboard **")
			pyperclip.copy(found_cred['pw'])
		else:
			messagebox.showinfo(title="Error", message=f"No credentials found for {w_input}.")


# ---------------------------- UI SETUP ------------------------------- #

# LABEL
web_label = Label(text="Website: ", bg=BG_COLOR)
web_label.grid(column=0, row=1)

email_user_label = Label(text="Email/Username: ", bg=BG_COLOR)
email_user_label.grid(column=0, row=2)

password_label = Label(text="Password: ", bg=BG_COLOR)
password_label.grid(column=0, row=3)

# ENTRY
web_input = Entry(width=38, highlightthickness=0)
web_input.grid(column=1, row=1, columnspan=2)

email_user_input = Entry(width=44, highlightthickness=0)
email_user_input.grid(column=1, row=2, columnspan=3)
# prepopulate with insert. use 0 for start/first word. END for last word.
email_user_input.insert(0, 'abc@gmail.com')

password_input = Entry(width=25, highlightthickness=0)
password_input.grid(column=1, row=3)

# BUTTONS
search_btn = Button(text="Search", highlightthickness=0, highlightbackground=BTN_COLOR, command=search_cred_handler)
search_btn.grid(column=3, row=1)

gen_pw_btn = Button(text="Generate Random", highlightthickness=0, highlightbackground=BTN_COLOR, command=generate_pw_handler)
gen_pw_btn.grid(column=2, row=3)

copy_pw_btn = Button(text="Copy", highlightthickness=0, highlightbackground=BTN_COLOR, command=copy_pw_handler)
copy_pw_btn.grid(column=3, row=3)

add_btn = Button(text="Add", width=44, highlightthickness=0, highlightbackground=BTN_COLOR, command=save_pw_handler)
add_btn.grid(column=1, row=4, columnspan=3)

window.mainloop()