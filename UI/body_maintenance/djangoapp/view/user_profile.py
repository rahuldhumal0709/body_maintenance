import datetime
import json
from djangoapp.utilities.validation import *
import traceback
from django.db import connection
from django.http import HttpResponse, JsonResponse
from rest_framework.permissions import IsAuthenticated
from rest_framework import generics
from rest_framework.views import APIView
from djangoapp.utilities.validation import *
from djangoapp.models import *
from django.db.models import Q
import logging
from django.conf import settings
import base64
from rest_framework.decorators import api_view
from django.views.decorators.csrf import csrf_exempt
from djangoapp.utilities.send_acknowledge_email_view import *
from djangoapp.utilities.generate_otp_view import *
import random
from django.utils import timezone

logger = logging.getLogger(__name__)
logger = logging.getLogger("django")



@csrf_exempt
@api_view(['GET'])
def get_user_profile(request):
    try:
        data_list = []
        user_id = request.user.pk
        employee_obj = employee_config.objects.get(auth_user_id=user_id)
        first_name = employee_obj.first_name
        last_name = employee_obj.last_name
        email = employee_obj.emailaddress
        phone = employee_obj.phone
        date_of_join = employee_obj.dateof_joining
        department = employee_obj.department.department_name
        emp_id = employee_obj.pk
        designation = employee_obj.designation.designation
        role_obj = employee_role.objects.filter(employee_id=emp_id)
        data_list1 = []
        for i in role_obj:
            data_list1.append({"employee_role": i.roles.role_name})

        data_list.append(
            {
                "full_name": first_name + " " + last_name,
                "first_name": first_name,
                "last_name": last_name,
                "email": email,
                "contact": phone,
                "date_of_joining": str(date_of_join),
                "department": department,
                "designation": designation,
                "employee_role": data_list1,
            }
        )

        logger.info("data retrieved successfully")
        return HttpResponse(
            json.dumps(
                {
                    "status": "success",
                    "message": f"Tickets User Profile retrieved successfully",
                    "data": data_list,
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
