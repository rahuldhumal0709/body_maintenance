import datetime
import json
import traceback
from django.db import connection
from django.http import HttpResponse, JsonResponse
from rest_framework.permissions import IsAuthenticated
from rest_framework import generics
from rest_framework.views import APIView
from djangoapp.models import *
from rest_framework import status
import datetime
from rest_framework.response import Response
import logging

logger = logging.getLogger(__name__)
logger = logging.getLogger("django")

#=================================== BMI =============================================================

class BMI_details(generics.ListCreateAPIView):
    """Adding and retrive bmi details of person"""

    # permission_classes = (IsAuthenticated,)

    def post(self,request):
        """Adding bmi details"""
        try:
            data = request.data

            user_id = User.objects.get(id=data['user_id']).pk
            date = data["date_id"]
            my_height = bm_person_info.objects.get(user_id=user_id).height
            my_weight = bm_weight.objects.filter(user_id=user_id,date=date).first().weight
            my_bmi = round(my_weight / ((my_height/100) ** 2), 2)

            if 19 <= my_bmi <= 24:
                result = 'Good'
            elif my_bmi < 19:
                result = 'Underweight'
            else:
                result = 'Overweight'

            bmi_details_obj = bm_bmi(
                user_id = user_id,
                date = date,
                height = my_height,
                weight = my_weight,
                bmi = my_bmi,
                result = result,
            )
            bmi_details_obj.save()
            logger.info("BMI details added successfully")
            return HttpResponse(
                json.dumps({"status":"success",
                            "message":"BMI details added successfully"}),
                    status=200,
                    content_type="application/json",
                )
        except Exception as msg:
            logger.error(msg)
            traceback.print_exc()
            return HttpResponse(
                json.dumps({"status":"failed",
                            "message": "There is backend issue, please contact administrator"}),
                status=200,
                content_type="application/json",
            )
        
    def get(self,request):
        """Getting bmi details"""
        try:
            response_data = []
            data = request.GET
            user = request.user
            if user.is_authenticated:
                filter_data = {key: data[key] for key in data.keys()}
                filter_data['user'] = user
                person_date_bmi_obj = bm_bmi.objects.filter(**filter_data).order_by('id')
                # filter details using person_name_id or date or combination of both.
                for i in person_date_bmi_obj:
                    response_data.append({
                        "bmi_id":i.pk,
                        "full_name":f'{i.user.first_name} {i.user.last_name}',
                        "date":str(i.date),
                        "height":i.height,
                        "weight":i.weight,
                        "BMI":f"{i.bmi} kg/m2",
                        "result":i.result
                    })
                if len(response_data)==0:
                    logger.info(f"Details of given input not found")
                    return HttpResponse(
                    json.dumps({"status":"failed",
                                "message": "Details of given input not found",
                                "data":response_data}),
                    status=200,
                    content_type="application/json",
                    )
                
                else:
                    logger.info(f"Details of given input retrieved successfully")
                    return HttpResponse(
                        json.dumps({"status":"success",
                                    "message": "Details of given input retrieved successfully",
                                    "total":len(response_data),
                                    "data":response_data}),
                        status=200,
                        content_type="application/json",
                    )
        except Exception as msg:
            logger.error(msg)
            traceback.print_exc()
            return HttpResponse(
                json.dumps({"status":"failed",
                            "message": "There is backend issue, please contact administrator"}),
                status=200,
                content_type="application/json",
            )

