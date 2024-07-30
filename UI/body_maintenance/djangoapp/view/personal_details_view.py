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
            user_id = User.objects.get(id=data['user_id']).pk
            first_name = data["first_name"]
            last_name = data["last_name"]
            dob = data["dob"]
            gender = data["gender"]
            height = data["height"]
            education = data["education"]
            permanent_address = data["permanent_address"]
            is_current_address_permanent_address = data['is_current_address_permanent_address']
            if is_current_address_permanent_address:
                current_address = permanent_address
            else:
                current_address = data["current_address"]
            marital_status = data["marital_status"]
            person_details_obj = bm_person_info(
                user_id = user_id,
                first_name = first_name,
                last_name = last_name,
                dob = dob,
                gender = gender,
                height = height,
                education = education,
                permanent_address = permanent_address,
                current_address = current_address,
                marital_status = marital_status
            )
            person_details_obj.save()
            User.objects.filter(id=user_id).update(first_name=first_name,last_name=last_name)
            logger.info("Personal details added successfully")
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
            data = request.GET
            user = request.user
            if user.is_authenticated:
                filter_data = {key: data[key] for key in data.keys()}
                filter_data['user'] = user
                person_data_obj = bm_person_info.objects.filter(**filter_data).order_by('id')
                for i in person_data_obj:
                    gender_choices = dict(i._meta.get_field('gender').choices)
                    gender = gender_choices.get(i.gender)
                    response_data.append({
                        "person_id":i.pk,
                        "user_name":i.user.username,
                        "full_name":f'{i.first_name} {i.last_name}',
                        "date_of_birth":str(i.dob),
                        "gender":gender,
                        "height":f"{i.height} cm",
                        "education":i.education,
                        "permanent_address":i.permanent_address,
                        "current_address":i.current_address,
                        "marital_status":i.marital_status
                })
                if not response_data:
                    logger.info("Details of given input not found")
                    return HttpResponse(
                    json.dumps({"status":"failed",
                                "message": "Details of given input not found",
                                "data":response_data}),
                    status=200,
                    content_type="application/json",
                    )
                
                else:
                    logger.info("Details of given input retrieved successfully")
                    return HttpResponse(
                        json.dumps({"status":"success",
                                    "message": f"Details of given input retrieved successfully",
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

#=================================== Weight info =============================================================

class Weight_details(generics.ListCreateAPIView):
    """Adding/Fetching weight Details"""

    # permission_classes = (IsAuthenticated,)

    def post(self, request):
        """Adding weight Details"""
        try:
            data = request.data

            user_id = User.objects.get(id=data['user_id']).pk
            date = data["date"]
            weight_of_person = data["weight"]
            weight_details_obj = bm_weight(
                user_id = user_id,
                date = date,
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
            user = request.user
            if user.is_authenticated:
                filter_data = {key: data[key] for key in data.keys()}
                filter_data['user'] = user
                person_weight_obj = bm_weight.objects.filter(**filter_data).order_by('id')
                # filter details using person_name_id or date or combination of both.
                for i in person_weight_obj:
                    response_data.append({
                        "weight_id":i.pk,
                        "full_name":f'{i.user.first_name} {i.user.last_name}',
                        "date":str(i.date),
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
