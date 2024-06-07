import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from typing import Sequence
from jinja2 import Template

class EmailSender:
    """Eine Simple E-Mail Klasse
    """
    def __init__(self):
        self.host = "mx2eb7.netcup.net"
        self.username = "noreply@appilcan.de"
        self.password = "Mnibjb007"
    
    def render_html(self, template_path:str, **kwargs):
        with open(f"app/mails/{template_path}.html", 'r') as file:
            template = Template(file.read())
        self.html = template.render(**kwargs)

    def send_email(self, recipient: str|Sequence[str], subject:str):
        try:
            msg = MIMEMultipart('alternative')
            msg['Subject'] = subject
            msg['From'] = self.username

            part = MIMEText(self.html, 'html')
            msg.attach(part)

            with smtplib.SMTP(self.host, 587) as server:
                server.starttls()
                server.login(self.username, self.password)
                server.sendmail(self.username, recipient, msg.as_string())
        except smtplib.SMTPException as e:
            print("Fehler beim Senden der E-Mail:", str(e))

def send_register(recipient, url, firstname):
    client = EmailSender()
    client.render_html("register", name=firstname, url=url)
    client.send_email(recipient, "Registration")

def send_forget_password_mail(recipient, url, firstname):
    client = EmailSender()
    client.render_html("password", name=firstname, url=url)
    client.send_email(recipient, "Reset Password")
    
def send_welcome(recipient, firstname):
    client = EmailSender()
    client.render_html("welcome", name=firstname)
    client.send_email(recipient, "Welcome to the URL")
