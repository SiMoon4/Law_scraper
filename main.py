import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from bs4 import BeautifulSoup
import requests
import tkinter
from tkinter import ttk
import os
from dotenv import load_dotenv
import webbrowser
from twilio.rest import Client
import datetime
import lxml
#twilio sms poslani

load_dotenv()

my_email = os.getenv("MY_EMAIL")
password = os.getenv("PASSWORD")
twilio_username = os.getenv("TWILIO_USERNAME")
twilio_password = os.getenv("TWILIO_PASSWORD")
phone_number_from = os.getenv("PHONE_NUMBER")
smtp_server = "smtp.gmail.com"
smtp_port = 587
if not my_email or not password:
    print("Error: Email information were not found in the .env file.")
    print("Ensure you have an .env file and that it contains EMAIL_USER and EMAIL_PASS.")

#future - object orianted 
law_response = []

#WINDOW SETUP

window = tkinter.Tk()
window.title("Law scraper")
window.minsize(width= 800, height= 500)
window.config(padx=30, pady=50, bg="grey90")

#STYLES

style = ttk.Style()
style.configure("TLabel", font = ("Calibri", 12), bg = "grey90")
style.configure("TButton", font = ("Calibri", 12))

#WELCOME

welcome_frame = ttk.Frame(window, padding=10)
welcome_frame.pack(fill="x", pady=10)
welcome_frame.columnconfigure(0, weight=1)

central_label = ttk.Label(welcome_frame, text="Law scraper", font=("Calibri", 30)).grid(column=0, row=0)
ttk.Label(welcome_frame, text="Search for law by law number, year and paragraph", font=("Calibri", 20)).grid(column=0, row=1)

#LAW INPUT

input_frame = ttk.Frame(window, padding=10)
input_frame.pack(fill="x", pady=10)

input_frame.columnconfigure(0, weight=1)
input_frame.columnconfigure(1, weight=1)
input_frame.columnconfigure(2, weight=1)

ttk.Label(input_frame, text="Law number").grid(column=0, row=0, pady=5)
law_number = ttk.Entry(input_frame, width=30, justify="center")
law_number.grid(column=0, row=1, padx=5, pady=5)

ttk.Label(input_frame, text="Year").grid(column=1, row=0, pady=5)
year = ttk.Entry(input_frame, width=30, justify="center")
year.grid(column=1, row=1, padx=5, pady=5)

ttk.Label(input_frame, text="Paragraph").grid(column=2, row=0, pady=5)
paragraph = ttk.Entry(input_frame, width=30, justify="center")
paragraph.grid(column=2, row=1, padx=5, pady=5)

# SEARCH FUNCTION

headers = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/144.0.0.0 Safari/537.36",
    "Accept-Language": "cs-CZ,cs;q=0.9"
}

def get_law():
    global law_response
    global url
    p = paragraph.get()
    y = year.get()
    n = law_number.get()

    if not p or not y or not n:
        search_result.config(text="Fill in all fields!", foreground="red")
        return

    url = f"https://krajta.slv.cz/{y}/{n}/par_{p}"
    response = requests.get(url=url, headers=headers)
    response.raise_for_status()
    data = response.text

    soup = BeautifulSoup(data, "lxml")
    selector = f"[id*='par_{p}']"
    law = soup.select(selector=selector)
    for i in law:
        law_response.append(i.get_text())
    
    if law_response == []:
        search_result.config(text="The law HAS NOT BEEN found", foreground="red")
        link_result.config(text="Link is NOT ready!", foreground="red")
    else:
        search_result.config(text="The law HAS BEEN found", foreground="green")
        link_result.config(text="Link is ready!", foreground="green")

search_button = ttk.Button(input_frame, text="Search", command=get_law, width=25)
search_button.grid(column=0, row=2, columnspan=3, pady=10)

#LAW SEARCH

search_frame = ttk.Frame(window, padding=10)
search_frame.pack(fill="x", pady=10)
search_frame.columnconfigure(0, weight=1)

search_result = ttk.Label(search_frame, font=("Calibri", 15))
search_result.grid(column=0, row=0)

#EMAIL FUNCTION

def sending_email():
    try:
        if law_response == []:
            sent_result.config(text="First, find the law", foreground="red")
        email_to = email_input.get()
        msg = MIMEMultipart()
        msg["FROM"] = my_email
        msg["TO"] = email_to
        msg["SUBJECT"] = "The law you have been searching for!"
        for i in law_response:
            msg.attach(MIMEText(f"{i}\n", "plain"))
        msg.attach(MIMEText(f"{url}", "plain"))

        with smtplib.SMTP(smtp_server, smtp_port) as server:
            server.starttls()
            server.login(my_email, password)
            server.sendmail(from_addr=my_email, to_addrs=email_to, msg=msg.as_string())
        
        sent_result.config(text="Email HAS BEEN sent!", foreground="green")
        print("Email HAS BEEN sent!")
    except Exception as e:
        sent_result.config(text="Email HAS NOT BEEN sent!", foreground="red")
        print(f"Email HAS NOT BEEN sent! Error: {e}")

#LINK FUNCTION

def webside_link():
    webbrowser.open_new(url=url)
    print(law_response)

#SMS_FUNCTION

def sending_text():

    phone_number_to = sms_input.get()
    client = Client(username=twilio_username, password=twilio_password)
    message = client.messages.create(body=f"Here is the link to the law\n{url}", from_=phone_number_from, to=phone_number_to)
    print(message.body)

#SENDING A MAIL + LINK + SENDING SMS

action_frame = ttk.Frame(window, padding=10)
action_frame.pack(fill="x", pady=10)
action_frame.columnconfigure(0, weight=1)
action_frame.columnconfigure(1, weight=1)
action_frame.columnconfigure(2, weight=1)

ttk.Label(action_frame, text="Send it to your email").grid(column=0, row=0, pady=5)
email_input = ttk.Entry(action_frame, width=35, justify="center")
email_input.grid(column=0, row=1)

email_button = ttk.Button(action_frame, text="Send", command=sending_email)
email_button.grid(column=0, row=2, pady=5)

link = ttk.Label(action_frame, text="Go to the webside").grid(column=1, row=0, pady=5)
link_result = ttk.Label(action_frame, font=("Calibri", 15))
link_result.grid(column=1, row=1, pady=5)

link_button = ttk.Button(action_frame, text="Link", command=webside_link)
link_button.grid(column=1, row=2, pady=5)

sms = ttk.Label(action_frame, text = "Save a link through message").grid(column=2, row=0, pady=5)
sms_input = ttk.Entry(action_frame, width=35, justify = "center")
sms_input.grid(column=2, row=1)
sms_input.insert(0, "+420")

sms_button = ttk.Button(action_frame, text="Send", command=sending_text)
sms_button.grid(column=2, row=2, pady=5)

#EMAIL + SMS CONFIRMATION

sent_frame = ttk.Frame(window, padding=10)
sent_frame.pack(fill="x", pady=10)
sent_frame.columnconfigure(0, weight=1)

sent_result = ttk.Label(sent_frame, font=("Calibri", 15))
sent_result.grid(column=0, row=0)


window.mainloop()