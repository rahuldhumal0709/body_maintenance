import json
from djangoapp.utilities.validation import *
import traceback
from django.http import HttpResponse
from rest_framework import generics
from djangoapp.utilities.validation import *
from djangoapp.models import *
import logging
from djangoapp.utilities.send_acknowledge_email_view import *
from djangoapp.utilities.generate_otp_view import *
from djangoapp.utilities.notification_view import *
from django.utils import timezone

logger = logging.getLogger(__name__)
logger = logging.getLogger("django")


class forgot_password(generics.ListCreateAPIView):
    """for forgot password"""

    # permission_classes=(IsAuthenticated,)
    def post(self, request):
        try:
            data = request.data
            email_add = data["email"]
            email = str(email_add).strip()
            is_exists = User.objects.filter(email=email).exists()
            logger.info("check email is exists or not")
            if is_exists:
                logger.info("if exists")
                fname = User.objects.get(email=email).first_name
                contact = employee_config.objects.get(emailaddress=email).phone
                otp = generateOTP()
                logger.info("generate otp successfully")
                logger.info(f"otp: {otp}")
                # print("otp", otp)
                subject = "Reset your password"
                recipient_list = [email]
                html_temp = """<html>
                <head></head>
                <body>
                    <h3>Reset your Octillion Power Password</h3>
                    <h4>Hi {fname},</h4>
                    <hr width="480px;" color="Gray" size="2" align="left">
                    <p>We are sending you this email because you requested a password reset.</p>
                    <p>Your OTP (one time password) is: <strong>{otp}</strong> Don't share your OTP with anyone.</p>
                    <p>If you didn't request a password reset, you can ignore this email. Your password will not changed.</a></p>
                    <p>Thank You!<br>Team Nexgensis<br>info@nexgensis.com</p>

                </body>
                </html>""".format(
                    fname=fname, otp=otp
                )

                send_acknowledge_email(subject, html_temp, recipient_list)
                logger.info("acknowledgement mail sent.")
                sms_status_code, message = send_sms_using_fast2sms(otp, contact)

                if sms_status_code == 200:
                    otp_obj = otp_records(
                        email=email,
                        contact=contact,
                        generated_at=timezone.now()
                        + timezone.timedelta(hours=5, minutes=30),
                        otp=otp,
                    )
                    otp_obj.save()
                    logger.info("otp saved")
            logger.info("no account found with giveb credentials")
            return HttpResponse(
                json.dumps(
                    {
                        "status": "success",
                        "message": "OTP sent successfully! Please check your registered email or phone number",
                    }
                )
            )

        except Exception as msg:
            logger.error(msg)
            traceback.print_exc()
            return HttpResponse(
                json.dumps(
                    {"status": "failed", "message": "please contact administrator"}
                )
            )


class set_password(generics.ListCreateAPIView):
    """set password with opt verification"""

    # permission_classes=(IsAuthenticated,)
    def post(self, request):
        try:
            data = request.data

            email = data["email"]
            otp = otp_records.objects.filter(email=email).last().otp
            logger.info("getting save otp")
            gen_otp = str(data["otp"]).strip()
            if otp == int(gen_otp):
                logger.info("checking OTP")
                us = User.objects.get(email=email)
                new_password = data["new_password"]
                confirm_password = data["confirm_password"]
                if new_password == confirm_password:
                    logger.info("if both password match")
                    us.set_password(new_password)
                    us.save()
                    logger.info("password updated")
                    forgot_password_log_obj = forgot_password_log(
                        email=email,
                        otp=otp,
                        first_name=us.first_name,
                        last_name=us.last_name,
                    )
                    forgot_password_log_obj.save()
                    return HttpResponse(
                        json.dumps(
                            {
                                "status": "success",
                                "message": "Your password has been changed successfully! You can now log in using your new password.",
                            }
                        )
                    )

                else:
                    logger.info("New password and confirm password not matched")
                    return HttpResponse(
                        json.dumps(
                            {
                                "status": "failed",
                                "message": "New password and confirm password not matched",
                            }
                        )
                    )
            else:
                logger.info("Invalid OTP, please enter a valid one-time password")
                return HttpResponse(
                    json.dumps(
                        {
                            "status": "failed",
                            "message": "Invalid OTP, please enter a valid one-time password.",
                        }
                    )
                )
        except Exception as msg:
            logger.error(msg)
            traceback.print_exc()
            return HttpResponse(
                json.dumps(
                    {"status": "failed", "message": "please contact administrator"}
                )
            )
