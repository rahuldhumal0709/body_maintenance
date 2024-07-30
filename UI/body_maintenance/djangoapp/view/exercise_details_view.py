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

#=================================== Exercise =============================================================

class Exercise_details(generics.ListCreateAPIView):
    """Adding and retrive exrecise details"""

    # permission_classes = (IsAuthenticated,)

    def post(self,request):
        """Adding exercise details"""
        try:
            data = request.data

            user_id = User.objects.get(id=data['user_id']).pk
            date = data["date"]
            start_time = data["start_time"]
            end_time = data["end_time"]
            sets_of_parts = data["sets_of_parts"]
            efforts = data["efforts"]

            exercise_details_obj = bm_exercise(
                user_id = user_id,
                date = date,
                start_time = start_time,
                end_time = end_time,
                sets_of_parts = sets_of_parts,
                efforts = efforts
            )
            exercise_details_obj.save()
            logger.info("Exercise details added successfully")
            return HttpResponse(
                json.dumps({"status":"success",
                            "message":"Exercise details added successfully"}),
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
        """Getting exercise details"""
        try:
            response_data = []
            data = request.GET
            user = request.user
            if user.is_authenticated:
                filter_data = {key: data[key] for key in data.keys()}
                filter_data['user'] = user
                person_date_exercise_obj = bm_exercise.objects.filter(**filter_data).order_by('id')
                # filter details using person_name_id or date or combination of both.
                for i in person_date_exercise_obj:
                    response_data.append({
                        "exercise_id":i.pk,
                        "full_name":f'{i.user.first_name} {i.user.last_name}',
                        "date":str(i.date),
                        "start_time":str(i.start_time),
                        "end_time":str(i.end_time),
                        "sets_of_parts":i.sets_of_parts,
                        "efforts":f"{i.efforts} %"
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
