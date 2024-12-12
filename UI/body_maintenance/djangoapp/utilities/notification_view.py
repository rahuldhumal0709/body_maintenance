import json
# from config_app.utilities.validation import *
# import traceback
# from config_app.utilities.validation import *
# from config_app.models import *
import logging
# from config_app.utilities.send_acknowledge_email_view import *
# from config_app.utilities.generate_otp_view import *
from django.db.models import Count
import requests
import traceback

logger = logging.getLogger(__name__)
logger = logging.getLogger("django")

FAST2SMS_API_KEY = (
    "PCSV5Tojw62DiebI0fG9cJHWgd4mEzR1hBqApYtNyaxsr3vFOUzjoabg6pnWEtBxdf1UJc7erIVNFh95"
)
FAST2SMS_URL = "https://www.fast2sms.com/dev/bulkV2"


def send_sms_using_fast2sms(message_body, reciever_phone_number):
    """Send text message notification by fast2sms"""
    try:

        url = FAST2SMS_URL
        headers = {
            "authorization": FAST2SMS_API_KEY,
            "Content-Type": "application/x-www-form-urlencoded",
            "Cache-Control": "no-cache",
        }
        payload = (
            f"variables_values={message_body}&route=otp&numbers={reciever_phone_number}"
        )
        send_text = requests.post(url=url, data=payload, headers=headers)
        json_data = json.loads(send_text.content)
        if send_text.status_code == 200:
            logger.info(f"message sent successfully to {reciever_phone_number}")
        else:

            logger.info(f"message sending failed due to {json_data['message']}")
        return send_text.status_code, json_data["message"]
    except Exception as exc:
        print(traceback.print_exc())
        logger.error(f"messaage sending failed: {exc}")
        return send_text.status_code, json_data["message"]


def send_notification(fcm_token_list):
    """Sending notifiction"""
    try:
        url = "https://fcm.googleapis.com/fcm/send"
        Header = {
            "Content-Type": "application/json",
            "Authorization": "key=AAAAcO_eSYw:APA91bE8XhLf12vBvi8XTHtsbc1cm5ohvVNuLpFHKnpCuOfWUWiSezxBlSa7rbNydry5jTWBo_xuCbRA6IcggnrRKiUugizklaCNvkObO88hT0Fl-4y7ca9bQ89J9D9ho4T-PXA3n8J0",
        }
        body = {
            "registration_ids": fcm_token_list,  # "dJbgCPqCRDu1C-J9F5s6uS:APA91bFRrTADvD9NET6PpZO7Ede30VwD5yxRCkxmqrVV5IQRNqMNyGsiMQ0EFN2i0ikepmaqtGtnXedXB1zl9UKXuiQMNP9afEQ0CqLPkRowRXtQY8cJJC7QNMBOG8UyDC-RbzMtjS2l",
            "notification": {
                "title": "Ticket status testing notification",
                "body": "Phase 1",
                "mutable_content": True,
            },
            "data": {
                "page": "dashboard",
            },
        }
        notification = requests.post(url=url, headers=Header, json=body)
        print(notification.content)
        logger.info("notification senf successfully")
        if notification.status_code == 200:
            return True
        else:
            return False

    except:
        traceback.print_exc()
        return None
