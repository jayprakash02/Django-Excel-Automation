from django.core.mail import  send_mail
from django.template.loader import render_to_string
import threading


class EmailThread(threading.Thread):

    def __init__(self, data):
        threading.Thread.__init__(self)
        self.data = data

    def run(self):
        html_message = render_to_string(
            'html_message.html', {'data' : self.data}
        )
        send_mail(
            subject=self.data['email_subject'], message =self.data['email_body'],from_email=None, recipient_list=[self.data['to_email']], html_message=html_message)


class Util:
    @staticmethod
    def send_email(data):
        
        EmailThread(data).start()
