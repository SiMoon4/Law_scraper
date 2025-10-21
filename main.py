import smtplib
from bs4 import BeautifulSoup
import requests
import tkinter
from tkinter import ttk

#WINDOW SETUP

window = tkinter.Tk()
window.title("Law scraper")
window.minsize(width= 700, height= 500)
window.config(padx=30, pady=50, bg="grey90")

#STYLES

style = ttk.Style()
style.configure("TLabel", font = ("Calibri", 12), bg = "grey90")
style.configure("TButton", font = ("Calibri", 12))

#WELCOME

welcome_frame = ttk.Frame(window, padding=10)
welcome_frame.pack(fill="x", pady=10)


central_label = ttk.Label(welcome_frame, text="Law scraper", font=("Calibri", 30)).grid(column=1, row=0)

ttk.Label(welcome_frame, text="Search for law by law number, year and paragraph", font=("Calibri", 20)).grid(column=1, row=1)

# central_label = tkinter.Label(text="Law Scraper", font=("Calibri", 30))
# central_label.grid(column=1, row=0)

# explain_label = tkinter.Label(text="Type what law, year and paragraph you want to know", font=("Calibri", 20))
# explain_label.grid(column=1, row=1)

#LAW INPUT

input_frame = ttk.Frame(window, padding=10)
input_frame.pack(fill="x", pady=10)

ttk.Label(input_frame, text="Law number").grid(column=0, row=2, pady=5)
# law_label = tkinter.Label(text="Law", font=("Calibri", 12))
# law_label.grid(column=0, row=2)
law_number = ttk.Entry(input_frame, width=20)
law_number.grid(column=0, row=3, padx=5, sticky="ew", pady=5)

# law = tkinter.Entry(width=20)
# law.focus
# law.insert(index=0, string=0)
# law.grid(column=0, row=3)

ttk.Label(input_frame, text="Year").grid(column=1, row=2, pady=5)
year = ttk.Entry(input_frame, width=20)
year.grid(column=1, row=3, padx=5, pady=5)

# year_label = tkinter.Label(text="Year", font=("Calibri", 12))
# year_label.grid(column=1, row=2)

# year = tkinter.Entry(width=20)
# year.focus()
# year.insert(index=0, string=0)
# year.grid(column=1, row=3)

ttk.Label(input_frame, text="Paragraph").grid(column=2, row=2, pady=5)
paragraph = ttk.Entry(input_frame, width=20)
paragraph.grid(column=2, row=3, padx=5, pady=5)

# paragraph_label = tkinter.Label(text="Paragraph", font=("Calibri", 12))
# paragraph_label.grid(column=2, row=2)

# paragraph = tkinter.Entry(width=20)
# paragraph.focus
# law.insert(index=0, string=0)
# paragraph.grid(column=2, row=3)

search_button = ttk.Button(input_frame, text="Search", command=None)
search_button.grid(column=1, row=4)

#LAW SEARCH

search_frame = ttk.Frame(window, padding=10)
search_frame.pack(fill="x", pady=10)

# search_button = tkinter.Button(text="Search", command=None)
# search_button.grid(column=1, row=4)

search_result = ttk.Label(search_frame, text="-", font=("Calibri", 15))
# search_result = tkinter.Label(text="-", font=("Calibri", 15))
search_result.grid(column=1, row=5)


#SENDING A MAIL

email_frame = ttk.Frame(window, padding=10)
email_frame.pack(fill="x", pady=10)

ttk.Label(email_frame, text="Send it to your email").grid(column=1, row=6, pady=5)
email_input = ttk.Entry(email_frame, width=40)
email_input.grid(column=1, row=7, pady=5)

# email_input = tkinter.Entry(width=40)
# email_input.focus
# email_input.grid(column=1, row=6)

email_button = ttk.Button(email_frame, text="Send", command=None)
email_button.grid(column=1, row=8)

# email_button = tkinter.Button(text="Send", command=None)
# email_button.grid(column=1, row=8)



window.mainloop()





