from django.conf import settings
from django.core.mail import EmailMultiAlternatives,EmailMessage
import logging

logger = logging.getLogger(__name__)
logger = logging.getLogger("django")



def send_acknowledge_email(subject,message,recipient_list):
    try:
        email_from = settings.EMAIL_HOST_USER
        print(subject)
        html_content = message
        print(recipient_list)
        text_content = "text"
        print(email_from)
        #subject = subject
        msg = EmailMultiAlternatives(subject, text_content, email_from,recipient_list)
        msg.attach_alternative(html_content, "text/html")
        msg.send()
        logger.info("email sent successfully")
    except ConnectionError as conn_err:
        logger.error("Failed to connect to the email server: %s", conn_err)
    except TimeoutError as timeout_err:
        logger.error("Email sending timed out: %s", timeout_err)
    except Exception as err:
        logger.error("An unexpected error occurred while sending email: %s", err)
    