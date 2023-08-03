import sys
import traceback
from django.core.mail import EmailMultiAlternatives
import ssl

# def send_mail(from_email,to_email,subject,html_content):
#     try:
#         ssl._create_default_https_context = ssl._create_unverified_context
#         msg = EmailMultiAlternatives(subject, html_content, from_email, [to_email])
#         msg.attach_alternative(html_content, "text/html")
#         msg.send()
#         print('mail send successfully to ',to_email)
#         return True
#     except Exception as e:
#         exc_type, exc_value, exc_traceback = sys.exc_info()
#         err = "\n".join(traceback.format_exception(*sys.exc_info()))
#         print(err)
#         print(e)
#         return e


import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart

def send_mail(to_email,subject,html_content):
    try:
        # Create the email message
        msg = MIMEMultipart()
        msg["From"] = 'send2greeshma@gmail.com'
        msg["To"] = to_email
        msg["Subject"] = subject
        msg.attach(MIMEText(html_content, "html"))

        # Establish a secure connection with the SMTP server
        smtp_server = "smtp.gmail.com"
        smtp_port = 587
        with smtplib.SMTP(smtp_server, smtp_port) as server:
            server.starttls()
            server.login('send2greeshma@gmail.com', 'qhxzbpriiykjgfit')
            server.send_message(msg)
        return True
    except Exception as e:
        exc_type, exc_value, exc_traceback = sys.exc_info()
        err = "\n".join(traceback.format_exception(*sys.exc_info()))
        print(err)
        print(e)
        return e



def send_password_reset_email(token,email):
    try:
        html_content = render_to_string('mail_template.html', {'token':token})
        subject = 'Password Reset Email'
        result = send_mail(email,subject,html_content)
        if result == True:
            return success_response(status=status.HTTP_200_OK,message='Password reset link has been sent.',data='')
        else:
            return failure_response(status=status.HTTP_400_BAD_REQUEST,message='Error in mail send',data=e)
    except Exception as e:
        print(e)
        return failure_response(status=status.HTTP_400_BAD_REQUEST,message='Error in mail send',data=e)


# from_email = 'send2greeshma@gmail.com'
# to_email = 'userone@getnada.com'
# subject = 'test'
# html_content = '<p>hiiii</p>'
# send_mail(from_email,to_email,subject,html_content)