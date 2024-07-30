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

#=================================== office =============================================================

class Office_working_details(generics.ListCreateAPIView):
    """Adding and retrive office details of person"""

    # permission_classes = (IsAuthenticated,)

    def post(self,request):
        """Adding office details"""
        try:
            data = request.data

            user_id = User.objects.get(id=data['user_id']).pk
            date = data["date"]
            start_time = data["start_time"]
            end_time = data["end_time"]
            work = data["work"]
            description = data["description"]
            efforts = data["efforts"]

            office_details_obj = bm_office(
                user_id = user_id,
                date = date,
                start_time = start_time,
                end_time = end_time,
                work = work,
                description = description,
                efforts = efforts
            )
            office_details_obj.save()
            logger.info("Working in office details added successfully")
            return HttpResponse(
                json.dumps({"status":"success",
                            "message":"Working in office details added successfully"}),
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
        """Getting office details"""
        try:
            response_data = []
            data = request.GET
            isinstance_obj = isinstance(data, dict)
            if isinstance_obj and data:
                filter_data = {key: data[key] for key in data.keys()}
                person_date_office_obj = bm_office.objects.filter(**filter_data).order_by('id')
                # filter details using person_name_id or date or combination of both.
                for i in person_date_office_obj:
                    start_time = datetime.datetime.combine(i.date, i.start_time)
                    end_time = datetime.datetime.combine(i.date, i.end_time)
                    total_working_time = end_time - start_time
                    response_data.append({
                        "office_id":i.pk,
                        "user_id":f'{i.user.first_name} {i.user.last_name}',
                        "date":str(i.date),
                        "start_time":str(i.start_time),
                        "end_time":str(i.end_time),
                        "total_working_time":str(total_working_time),
                        "work":i.work,
                        "description":i.description,
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
                                    "message": f"Details of given input retrieved successfully",
                                    "data":response_data}),
                        status=200,
                        content_type="application/json",
                    )
            office_data = bm_office.objects.all()
            for i in office_data:
                start_time = datetime.datetime.combine(i.date, i.start_time)
                end_time = datetime.datetime.combine(i.date, i.end_time)
                total_working_time = end_time - start_time
                response_data.append({
                    "office_id":i.pk,
                    "user_id":f'{i.user.first_name} {i.user.last_name}',
                    "date":str(i.date),
                    "start_time":str(start_time),
                    "end_time":str(end_time),
                    "total_working_time":str(total_working_time),
                    "work":i.work,
                    "description":i.description,
                    "efforts":f"{i.efforts} %"
                    })
            logger.info(f"Working in office details retrieved successfully")
            return HttpResponse(
                json.dumps({"status":"success",
                            "message": f"Working in office details retrieved successfully",
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
