from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
import smtplib, socket
import tkinter, random, time, functools, threading, screens

def login():
        global USERNAME
        global PASSWORD
        global SECURITY
        global HOST

        #Get all the details
        USERNAME = username.get()
        PASSWORD = password.get()
        HOSTS = {"Outlook" : ['smtp-mail.outlook.com', 587], "Yahoo" : ["stmp.mail.yahoo.com", 465], "Google" : ["smtp.gmail.com", 587],
                 "Hotmail" : ["imap-mail.outlook.com", 993]}
        
        HOST = HOSTS[selected.get()]
        SECURITY = str(random.randint(100_000, 999_999))

        
        s = smtplib.SMTP(host=HOST[0], port=HOST[1])
        s.starttls()
        s.login(USERNAME, PASSWORD)

        message = " Here is your verification code: {0}.\nMake sure to enter it into the box to ensure that you have entered the right email".format(SECURITY)
        msg = MIMEMultipart()

        msg['From'] = USERNAME
        msg['To'] = USERNAME
        msg['Subject'] = 'SpamBot Verification Code'

        msg.attach(MIMEText(message, 'plain'))

        s.send_message(msg)
        del msg


        home.hide()
        confirm.show()

def verify():
        user_input = code_box.get()
        if user_input != SECURITY:
            flash_red(5)
        else:
            confirm.hide()
            last_step.show()
        
def flash_red(i):
    if i >= 0:
        temp = i - 1
        code_box.configure({"background" : "red"})
        window.after(500, flash_white, temp)

def flash_white(i):
    if i >= 0:
        temp = i - 1
        code_box.configure({"background" : "white"})
        window.after(500, flash_red, temp)

def begin():
        global count, bots
        #The fun
        bots = list()
        f, t, su, m = USERNAME, target.get(), title.get(), body.get(tkinter.END)
        b = nobots.get()

        try:
            int(b)
        except TypeError:
            b = 100

        for i in range(int(b)):
            bot = threading.Thread(target=send, name="bot{0}".format(i),
            args=(f, t, su, m))              
            bot.start(); bot.join()

        temp_win = tkinter.Tk()
        temp_win.withdraw()
        temp_win.after(100, begin)

def send(f, t, su, m):

    s = smtplib.SMTP(host=HOST[0], port=HOST[1])
    s.starttls()
    s.login(USERNAME, PASSWORD)
    message = m
    msg = MIMEMultipart()

    msg['From'] = f
    msg['To'] = t
    msg['Subject'] = su

    msg.attach(MIMEText(message, 'plain'))
    s.send_message(msg)
    del msg
    update_score()


def back():
        confirm.hide()
        home.show()
        

def update_score():
    global count
    count += 1

print(__name__)
if __name__ == "__main__":           
        #Setup GUI
        bots = list()
        window = tkinter.Tk()
        home = screens.Screen("Home", window)
        
        window.minsize(width=800, height=600)

        heading = tkinter.Label(window, text="Welcome to The SpamBot")
        home.add_item(heading, 0, 1)


        username_label = tkinter.Label(window, text="Username: ")
        username = tkinter.Entry(window, width=50)

        password_label = tkinter.Label(window, text="Password: ")
        password = tkinter.Entry(window, width=50, show="*")


        host_label = tkinter.Label(window, text="Email Host: ")

        HOSTS = ["Outlook", "Yahoo", "Google", "Hotmail"]
        selected = tkinter.StringVar(window)
        selected.set(HOSTS[0])

        host = tkinter.OptionMenu(window, selected, *HOSTS)

        home.add_item(username_label, 2, 0)
        home.add_item(username, 2, 1)
        home.add_item(password_label, 3, 0)
        home.add_item(password, 3, 1)
        home.add_item(host_label, 4, 0)
        home.add_item(host, 4, 1)

           
            
        submit = tkinter.Button(window, text="LETS GO!", command=login)
        home.add_item(submit, 5, 1)


        USERNAME = ""
        PASSWORD = ""
        SECURITY = ""
        HOST = ""

        #Confirmation Screen
        confirm = screens.Screen("Enter your confirmation code", window)
        
        #Setup GUI
        code_box = tkinter.Entry(window, width=12)
        code_label = tkinter.Label(window, text="Enter your six digit confirmation code, sent to you in an email")


        resend = tkinter.Button(window, text="Resend", command=login)
        go_back = tkinter.Button(window, text="Change Details", command=back)

        code_submit = tkinter.Button(window, text="Submit", command=verify)
        count = 0
        temp = count
        first = 10
        confirm.add_item(code_label, 0, 0)
        confirm.add_item(code_box, 1, 0)
        confirm.add_item(code_submit, 2, 0)
        confirm.add_item(resend, 3, 0)
        confirm.add_item(go_back, 4, 0)

        last_step = screens.Screen("Setup", window)
        heading_1 = tkinter.Label(window, text="Fill in the following fields")
        target_label = tkinter.Label(window, text="To: ")
        target = tkinter.Entry(window, width=50)

        title_label = tkinter.Label(window, text="Subject: ")
        title = tkinter.Entry(window, width=50)

        body_label = tkinter.Label(window, text="Message: ")
        body = tkinter.Text(window, width=50, height=10)

        nobots_label = tkinter.Label(window, text="How many email bots do you want (min 0, max 1000)? ")
        nobots = tkinter.Entry(window, width=4)

            

        send_button = tkinter.Button(window, text="Start", command=begin)
        email_count = tkinter.Label(window, text=str("Emails sent: {0}".format(count)))

        last_step.add_item(heading_1, 0, 1)
        last_step.add_item(target_label, 1, 0)
        last_step.add_item(target, 1, 1)
        last_step.add_item(title_label, 2, 0)
        last_step.add_item(title, 2, 1)
        last_step.add_item(body_label, 3, 0)
        last_step.add_item(body, 3, 1)
        last_step.add_item(nobots_label, 4, 0)
        last_step.add_item(nobots, 4, 1)
        last_step.add_item(send_button, 5, 1)
        last_step.add_item(email_count, 6, 1)

        def update():
                global temp, first
                if count != temp:
                        email_count.config({"text":"Emails sent: {0}".format(count)})
                        temp = count

                window.after(1, update)

        home.show()
        window.after(1, update)
        tkinter.mainloop()    



