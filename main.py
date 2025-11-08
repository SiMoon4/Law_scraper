import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from bs4 import BeautifulSoup
import requests
import tkinter
from tkinter import ttk
import os
from dotenv import load_dotenv
import datetime
import lxml
#twilio sms poslani

load_dotenv()

my_email = os.getenv("MY_EMAIL")
password = os.getenv("PASSWORD")
smtp_server = "smtp.gmail.com"
smtp_port = 587
if not my_email or not password:
    print("Chyba: E-mailové údaje nebyly nalezeny v .env souboru.")
    print("Ujistěte se, že máte soubor .env a obsahuje EMAIL_USER a EMAIL_PASS.")

#future - object orianted 
law_response = []

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

#LAW INPUT

input_frame = ttk.Frame(window, padding=10)
input_frame.pack(fill="x", pady=10)

ttk.Label(input_frame, text="Law number").grid(column=0, row=2, pady=5)
law_number = ttk.Entry(input_frame, width=20)
law_number.grid(column=0, row=3, padx=5, sticky="ew", pady=5)

ttk.Label(input_frame, text="Year").grid(column=1, row=2, pady=5)
year = ttk.Entry(input_frame, width=20)
year.grid(column=1, row=3, padx=5, pady=5)

ttk.Label(input_frame, text="Paragraph").grid(column=2, row=2, pady=5)
paragraph = ttk.Entry(input_frame, width=20)
paragraph.grid(column=2, row=3, padx=5, pady=5)

# SEARCH FUNCTION/class

headers = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/114.0.0.0 Safari/537.36",
    "Accept-Language": "cs-CZ,cs;q=0.9"
}

def get_law():
    global law_response
    p = paragraph.get()
    y = year.get()
    n = law_number.get()

    if not p or not y or not n:
        search_result.config(text="Vyplňte všechna pole!", foreground="red")
        return

    response = requests.get(url=f"https://krajta.slv.cz/{y}/{n}/par_{p}", headers=headers)
    response.raise_for_status()
    data = response.text

    soup = BeautifulSoup(data, "lxml")
    selector = f"[id*='par_{p}']"
    law = soup.select(selector=selector)
    for i in law:
        law_response.append(i.get_text())
    
    if law_response == []:
        search_result.config(text="Zákon NEBYL nalezen", foreground="red")
    else:
        search_result.config(text="Zákon BYL nalezen", foreground="green")

search_button = ttk.Button(input_frame, text="Search", command=get_law)
search_button.grid(column=1, row=4)

#LAW SEARCH

search_frame = ttk.Frame(window, padding=10)
search_frame.pack(fill="x", pady=10)

search_result = ttk.Label(search_frame, font=("Calibri", 15))
search_result.grid(column=0, row=5)

#EMAIL FUNCTION

def sending_email():
    try:
        if law_response == []:
            email_sent_result.config(text="Nejprve vyhledej zákon", foreground="red")
        email_to = email_input.get()
        msg = MIMEMultipart()
        msg["FROM"] = my_email
        msg["TO"] = email_to
        msg["SUBJECT"] = "Zákon, který jsi hledal!"
        for i in law_response:
            msg.attach(MIMEText(f"{i}\n", "plain"))

        with smtplib.SMTP(smtp_server, smtp_port) as server:
            server.starttls()
            server.login(my_email, password)
            server.sendmail(from_addr=my_email, to_addrs=email_to, msg=msg.as_string())
        
        email_sent_result.config(text="Email BYL poslán!", foreground="green")
        print("Email nebyl poslán!")
    except Exception as e:
        email_sent_result.config(text="Email NEBYL poslán!", foreground="red")
        print(f"Email nebyl poslán! Error: {e}")


#SENDING A MAIL

email_frame = ttk.Frame(window, padding=10)
email_frame.pack(fill="x", pady=10)

ttk.Label(email_frame, text="Send it to your email").grid(column=1, row=6, pady=5)
email_input = ttk.Entry(email_frame, width=40)
email_input.grid(column=1, row=7, pady=5)

email_button = ttk.Button(email_frame, text="Send", command=sending_email)
email_button.grid(column=1, row=8)

#EMAIL CONFIRMATION

email_sent_frame = ttk.Frame(window, padding=10)
email_sent_frame.pack(fill="x", pady=10)

email_sent_result = ttk.Label(email_sent_frame, font=("Calibri", 15))
email_sent_result.grid(column=1, row=5)

#SENDING SMS

window.mainloop()