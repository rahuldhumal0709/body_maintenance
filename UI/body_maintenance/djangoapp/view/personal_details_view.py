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

#=================================== Person info =============================================================

class Person_details(generics.ListCreateAPIView):
    """Adding/Fetching Person Details"""

    # permission_classes = (IsAuthenticated,)

    def post(self, request):
        """Adding Person Details"""
        try:
            data = request.data

            person_name = data["person_name"]
            dob = data["dob"]
            gender = data["gender"]
            height = data["height"]
            education = data["education"]
            permanent_address = data["permanent_address"]
            current_address = data["current_address"]
            marital_status = data["marital_status"]
            person_details_obj = bm_person_info(
                person_name = person_name,
                dob = dob,
                gender = gender,
                height = height,
                education = education,
                permanent_address = permanent_address,
                current_address = current_address,
                marital_status = marital_status
            )
            person_details_obj.save()
            logger.info("Person details added successfully")
            return HttpResponse(
                json.dumps({"status":"success",
                            "message": "Person details added successfully"}),
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
        """Getting Person Details"""
        try:
            response_data = []
            person_data = bm_person_info.objects.all()
            for i in person_data:
                gender_choices = dict(i._meta.get_field('gender').choices)
                gender = gender_choices.get(i.gender)
                response_data.append({
                    "person_id":i.pk,
                    "person_name":i.person_name,
                    "date_of_birth":str(i.dob),
                    "gender":gender,
                    "height":f"{i.height} cm",
                    "education":i.education,
                    "permanent_address":i.permanent_address,
                    "current_address":i.current_address,
                    "marital_status":i.marital_status
                })
            logger.info(f"Details retrieved successfully")
            return HttpResponse(
                json.dumps({"status":"success",
                            "message": f"Details retrieved successfully",
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

#=================================== Weight info =============================================================

class Weight_details(generics.ListCreateAPIView):
    """Adding/Fetching weight Details"""

    # permission_classes = (IsAuthenticated,)

    def post(self, request):
        """Adding weight Details"""
        try:
            data = request.data

            person_name_id = data["person_name_id"]
            date_id = data["date_id"]
            weight_of_person = data["weight"]
            weight_details_obj = bm_weight(
                person_name_id = bm_person_info.objects.get(pk=person_name_id).pk,
                date_id = bm_date.objects.get(pk=date_id).pk,
                weight = weight_of_person
            )
            weight_details_obj.save()
            logger.info("Weight added successfully")
            return HttpResponse(
                json.dumps({"status":"success",
                            "message": "weight added successfully"}),
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
        """Getting weight Details"""
        try:
            response_data = []
            data = request.GET
            isinstance_obj = isinstance(data, dict)
            if isinstance_obj and data:
                filter_data = {key: data[key] for key in data.keys()}
                person_weight_obj = bm_weight.objects.filter(**filter_data).order_by('id')
                # filter details using person_name_id or date or combination of both.
                for i in person_weight_obj:
                    response_data.append({
                        "weight_id":i.pk,
                        "person_name":i.person_name.person_name,
                        "date":str(i.date.date),
                        "weight":i.weight
                        
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
            weight_data = bm_weight.objects.all()
            for i in weight_data:
                response_data.append({
                    "weight_id":i.pk,
                    "person_name":i.person_name.person_name,
                    "date":str(i.date.date),
                    "weight":i.weight
                    
                })
            logger.info(f"Weight retrieved successfully")
            return HttpResponse(
                json.dumps({"status":"success",
                            "message": f"Weight retrieved successfully",
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
