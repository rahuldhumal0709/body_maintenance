import logging
import traceback
import json
from django.http import HttpResponse
from rest_framework.decorators import api_view
from django.views.decorators.csrf import csrf_exempt
from djangoapp.models import EmailConfiguration
from djangoapp.utilities.email_config import load_email_configuration
from djangoapp.utilities.user_auth import Auth
from djangoapp.utilities.access_manager import email_authenticate_access
from djangoapp.models import EmailAccessPassword,InterlockAccessPassword

# logging configuration
logger = logging.getLogger(__name__)
logger = logging.getLogger('django')

@csrf_exempt
@api_view(['POST'])
def update_email_configs(request):
    try:
        # authenticate
        response = Auth.anonymous(request)
        if response == 'authorized':
            pass
        else:
            return response
        required_fields = ['smtp_user', 'smtp_password','access_password']   
        if not all(field in request.data for field in required_fields):
            return HttpResponse(
                json.dumps({"status": "failed", 
                "message": "Please provide mandatory fields"}),
                status=200
            )
        access = email_authenticate_access(request.data['access_password'])
        if access:
            fields_to_update = {}
            for field in ['smtp_host', 'smtp_port', 'smtp_user', 'smtp_password', 'use_tls', 'use_ssl']:
                if field in request.data:
                    fields_to_update[field] = request.data[field]

            # Update or create the email configuration
            config, created = EmailConfiguration.objects.update_or_create(
                id=1,  # Assuming a single configuration record
                defaults={**fields_to_update}
            )

            # Reload the email configuration into settings
            load_email_configuration()
        
            logger.info("Email Configs Updated Successfully")
            return HttpResponse(json.dumps({
                "status":"success",
                "message": "Email Configs Updated Successfully"}),
                status=200,
                content_type="application/json",
            )
        else:
            return HttpResponse(json.dumps({
                "status":"failed",
                "message": "Password Authentication Failed"}),
                status=200,
                content_type="application/json",) 
    except Exception as msg:
        logger.error(msg)
        traceback.print_exc()
        return HttpResponse(
            json.dumps({"status":"failed",
                        "message": "There is backend issue, please contact administrator"}),
                        status=200,
                        content_type="application/json",
                        )
@api_view(['GET'])        
def get_email_configs(request):
    try:
        request.GET
        email_obj = EmailConfiguration.objects.all().last()
        if email_obj:
            data = {
                'smtp_host':email_obj.smtp_host,
                'smtp_port':email_obj.smtp_port,
                'smtp_user':email_obj.smtp_user,
                'use_tls':email_obj.use_tls,
                'use_ssl':email_obj.use_ssl
            }
        else:
            data = {}
        return HttpResponse(json.dumps({
            "status":"success",
            "message": "Email Configs Retirved Successfully",
            "data":data}),
            status=200,
            content_type="application/json",
        )
    except Exception as msg:
        logger.error(msg)
        traceback.print_exc()
        return HttpResponse(json.dumps({
            "status":"failed",
            "message": "There is backend issue, please contact administrator"}),
            status=200,
            content_type="application/json",
        )   
@csrf_exempt
@api_view(['POST'])
def set_email_access_password(request):
    try:
        if 'password' not in request.data:
           return HttpResponse(
            json.dumps({"status": "failed", "message": "Please Provide Password"}),
            status=200,
            content_type="application/json",
        )
        if EmailAccessPassword.objects.exists():
            EmailAccessPassword.objects.update(password = request.data['password'])
            msg = "Password Updated Successfully"
        else:
            EmailAccessPassword.objects.create(password = request.data['password'])
            msg = "Password Created Successfully"
        return HttpResponse(
            json.dumps({"status": "success", "message":msg}),
            status=200,
            content_type="application/json",
        )
    except Exception as e:
        logger.error(e)
        traceback.print_exc()
        return HttpResponse(
            json.dumps({"status": "failed", "message": "Please contact administrator"}),
            status=200,
            content_type="application/json",
        )
        
@csrf_exempt
@api_view(['POST'])
def set_interlock_password(request):
    try:
        if 'password' not in request.data:
           return HttpResponse(
            json.dumps({"status": "failed", "message": "Please Provide Password"}),
            status=200,
            content_type="application/json",
        )
        if InterlockAccessPassword.objects.exists():
            InterlockAccessPassword.objects.update(password = request.data['password'])
            msg = "Password Updated Successfully"
        else:
            InterlockAccessPassword.objects.create(password = request.data['password'])
            msg = "Password Created Successfully"
        return HttpResponse(
            json.dumps({"status": "success", "message":msg}),
            status=200,
            content_type="application/json",
        )
    except Exception as e:
        logger.error(e)
        traceback.print_exc()
        return HttpResponse(
            json.dumps({"status": "failed", "message": "Please contact administrator"}),
            status=200,
            content_type="application/json",
        )