from django.core.mail import send_mail
from django.template.loader import render_to_string
import threading
from django.shortcuts import get_object_or_404
from app.models import Sheet

class SetPermission(threading.Thread):

    def __init__(self, service_drive):
        self.service_drive = service_drive
        threading.Thread.__init__(self)

    def setPermisionApprover(self, email):
        self.insert_permission(file_id=get_object_or_404(
            Sheet, question_type='Intelligent Dummy').sheetID, value=email, perm_type='user', role='writer')
        self.insert_permission(file_id=get_object_or_404(
            Sheet, question_type='Life Vector').sheetID, value=email, perm_type='user', role='writer')
        self.insert_permission(file_id=get_object_or_404(
            Sheet, question_type='Dummy Question').sheetID, value=email, perm_type='user', role='writer')
        self.insert_permission(file_id=get_object_or_404(
            Sheet, question_type='Learning Method').sheetID, value=email, perm_type='user', role='writer')

    def insert_permission(self, file_id, value, perm_type, role):
        service = self.service_drive
        new_permission = {
            'value': value,
            'type': perm_type,
            'role': role
        }
        try:
            return service.permissions().insert(
                fileId=file_id, body=new_permission).execute()
        except errors.HttpError as error:
            print('An error occurred: %s' % error)
        return None


class EmailThread(threading.Thread):

    def __init__(self, data):
        threading.Thread.__init__(self)
        self.data = data

    def run(self):
        html_message = render_to_string(
            'html_message.html', {'data': self.data}
        )
        send_mail(
            subject=self.data['email_subject'], message=self.data['email_body'], from_email=None, recipient_list=[self.data['to_email']], html_message=html_message)


class Util:
    @staticmethod
    def send_email(data):

        EmailThread(data).start()

    @staticmethod
    def excel_sheet(service_drive, approver_email):
        SetPermission(service_drive=service_drive).setPermisionApprover(
            email=approver_email)
