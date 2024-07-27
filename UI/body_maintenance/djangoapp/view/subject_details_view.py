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

#=================================== Subject name =============================================================

class Subject_name(generics.ListCreateAPIView):
    """Adding/Fetching subject name"""

    # permission_classes = (IsAuthenticated,)

    def post(self, request):
        """Adding subject name"""
        try:
            data = request.data

            subject_name = data["subject_name"]

            subject_obj = bm_subject_names(
                subject_name = subject_name,
            )
            subject_obj.save()
            logger.info(f"Subject {subject_name} added successfully")
            return HttpResponse(
                json.dumps({"status":"success",
                            "message": f"Subject {subject_name} added successfully"}),
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
        """Getting subject names"""
        try:
            response_data = []
            subject_obj = bm_subject_names.objects.all()
            for i in subject_obj:
                response_data.append({
                    "subject_id":i.pk,
                    "subject_name":i.subject_name,
                })
            logger.info(f"Subjects retrieved successfully")
            return HttpResponse(
                json.dumps({"status":"success",
                            "message": f"Subjects retrieved successfully",
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

#=================================== Subject all details =============================================================

class Subject_all_details(generics.ListCreateAPIView):
    """Adding and retrive subject all details"""

    # permission_classes = (IsAuthenticated,)

    def post(self,request):
        """Adding subject all details"""
        try:
            data = request.data

            person_name_id = bm_person_info.objects.get(pk=data["person_name_id"]).pk
            date = data["date"]
            start_time = data["start_time"]
            end_time = data["end_time"]
            subject_name_id = data["subject_name_id"]
            topic = data["topic"]
            description = data["description"]
            efforts = data["efforts"]
            is_any_que_solved = data["is_any_que_solved"]
            if is_any_que_solved == True :
                how_many_que = data["how_many_que"]
            else:
                how_many_que = 0

            subject_all_details_obj = bm_subject_details(
                person_name_id = person_name_id,
                date = date,
                start_time = start_time,
                end_time = end_time,
                subject_name_id = subject_name_id,
                topic = topic,
                description = description,
                efforts = efforts,
                is_any_que_solved = is_any_que_solved,
                how_many_que = how_many_que
            )
            subject_all_details_obj.save()
            logger.info("Subject details added successfully")
            return HttpResponse(
                json.dumps({"status":"success",
                            "message":"Subject details added successfully"}),
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
        """Getting subject all details"""
        try:
            response_data = []
            data = request.GET
            isinstance_obj = isinstance(data, dict)
            if isinstance_obj and data:
                filter_data = {key: data[key] for key in data.keys()}
                person_date_subject_obj = bm_subject_details.objects.filter(**filter_data).order_by('id')
                # filter details using person_name_id or date or combination of both.
                for i in person_date_subject_obj:
                    start_time = datetime.datetime.combine(i.date, i.start_time)
                    end_time = datetime.datetime.combine(i.date, i.end_time)
                    total_study_time_of_subject = end_time - start_time
                    response_data.append({
                        "subject_all_id":i.pk,
                        "person_name":i.person_name.person_name,
                        "date":str(i.date),
                        "start_time":str(i.start_time),
                        "end_time":str(i.end_time),
                        "total_study_time_of_subject":str(total_study_time_of_subject),
                        "subject_name":i.subject_name.subject_name,
                        "topic":i.topic,
                        "description":i.description,
                        "efforts":f"{i.efforts} %",
                        "is_any_que_solved":i.is_any_que_solved,
                        "how_many_que":i.how_many_que
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
            subject_all_data = bm_subject_details.objects.all()
            for i in subject_all_data:
                start_time = datetime.datetime.combine(i.date, i.start_time)
                end_time = datetime.datetime.combine(i.date, i.end_time)
                total_study_time_of_subject = end_time - start_time
                response_data.append({
                    "subject_all_id":i.pk,
                    "person_name":i.person_name.person_name,
                    "date":str(i.date),
                    "start_time":str(i.start_time),
                    "end_time":str(i.end_time),
                    "total_study_time_of_subject":str(total_study_time_of_subject),
                    "subject_name":i.subject_name.subject_name,
                    "topic":i.topic,
                    "description":i.description,
                    "efforts":f"{i.efforts} %",
                    "is_any_que_solved":i.is_any_que_solved,
                    "how_many_que":i.how_many_que
                })
            logger.info(f"Subject details retrieved successfully")
            return HttpResponse(
                json.dumps({"status":"success",
                            "message": f"Subject details retrieved successfully",
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
