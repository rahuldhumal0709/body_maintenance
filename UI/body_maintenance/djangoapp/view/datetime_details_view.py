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

#=================================== Date info =============================================================

class Date_details(generics.ListCreateAPIView):
    """Adding/Fetching Date"""

    # permission_classes = (IsAuthenticated,)

    def post(self, request):
        """Adding date"""
        try:
            data = request.data

            date = data["date"]

            date_obj = bm_date(
                date = date,
            )
            date_obj.save()
            logger.info(f"Details of date {str(date)} added successfully")
            return HttpResponse(
                json.dumps({"status":"success",
                            "message": f"Details of date {str(date)} added successfully"}),
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
        
    def get(self, request):
        """Get dates"""
        try:
            response_data = []
            date_obj = bm_date.objects.all()
            for i in date_obj:
                date = i.date
                response_data.append({
                    "date_id":i.pk,
                    "date":str(date),
                })
            logger.info(f"All dates retrieved successfully")
            return HttpResponse(
                json.dumps({"status":"success",
                            "message": f"All dates retrieved successfully",
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

#=================================== Wakeup sleep time =============================================================

class Wakeup_sleep_time_details(generics.ListCreateAPIView):
    """Adding/Fetching Wakeup sleep time details"""

    # permission_classes = (IsAuthenticated,)

    def post(self, request):
        """Adding Wakeup_sleep_details"""
        try:
            data = request.data

            person_name_id = data["person_name_id"]
            date_id = data["date_id"]
            wakeup_time = data["wakeup_time"]

            if 'sleep_time' in data:
                sleep_time = data["sleep_time"]
            else:
                sleep_time = None

            time_details_obj = bm_daily_wakeup_sleep_time(
                person_name_id = bm_person_info.objects.get(pk=person_name_id).pk,
                date_id = bm_date.objects.get(pk=date_id).pk,
                wakeup_time = wakeup_time,
                sleep_time = sleep_time,
            )

            time_details_obj.save()
            logger.info(f"Details added successfully")
            return HttpResponse(
                json.dumps({"status":"success",
                            "message": f"Details added successfully"}),
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
        
    def get(self, request):
        """Get time information"""
        try:
            response_data = []
            data = request.GET
            isinstance_obj = isinstance(data, dict)
            if isinstance_obj and data:
                filter_data = {key: data[key] for key in data.keys()}
                person_datetime_obj = bm_daily_wakeup_sleep_time.objects.filter(**filter_data).order_by('id')
                # filter details using person_name_id or date or combination of both.
                for i in person_datetime_obj:
                    date = i.date.date
                    person_name = i.person_name.person_name
                    response_data.append({
                        "date_id":i.pk,
                        "person_name":person_name,
                        "date":str(date),
                        "wakeup_time":str(i.wakeup_time),
                        "sleep_time":str(i.sleep_time),
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
            time_obj = bm_daily_wakeup_sleep_time.objects.all()
            for i in time_obj:
                date = i.date.date
                response_data.append({
                    "date_id":i.pk,
                    "person_name":i.person_name.person_name,
                    "date":str(date),
                    "wakeup_time":str(i.wakeup_time),
                    "sleep_time":str(i.sleep_time),
                })
            logger.info(f"All details retrieved successfully")
            return HttpResponse(
                json.dumps({"status":"success",
                            "message": f"All details retrieved successfully",
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