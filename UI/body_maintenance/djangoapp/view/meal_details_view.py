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

#=================================== Breakfast =============================================================

class Breakfast_details(generics.ListCreateAPIView):
    """Adding/Fetching Breakfast details"""

    # permission_classes = (IsAuthenticated,)

    def post(self, request):
        """Adding Breakfast details"""
        try:
            data = request.data

            user_id = User.objects.get(id=data['user_id']).pk
            date = data["date"]
            breakfast_meal = data["breakfast_meal"]
            description = data["description"]

            breakfast_details_obj = bm_breakfast(
                user_id = user_id,
                date = date,
                breakfast_meal = breakfast_meal,
                description = description
            )
            breakfast_details_obj.save()
            logger.info(f"Breakfast added successfully")
            return HttpResponse(
                json.dumps({"status":"success",
                            "message": f"Breakfast added successfully"}),
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
        """Get Breakfast details"""
        try:
            response_data = []
            data = request.GET
            isinstance_obj = isinstance(data, dict)
            if isinstance_obj and data:
                filter_data = {key: data[key] for key in data.keys()}
                person_date_breakfast_obj = bm_breakfast.objects.filter(**filter_data).order_by('id')
                # filter details using person_name_id or date or combination of both.
                for i in person_date_breakfast_obj:
                    response_data.append({
                        "breakfast_id":i.pk,
                        "user_id":f'{i.user.first_name} {i.user.last_name}',
                        "date":str(i.date),
                        "breakfast_meal":i.breakfast_meal,
                        "description":i.description
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
            breakfast_data = bm_breakfast.objects.all()
            for i in breakfast_data:
                response_data.append({
                    "breakfast_id":i.pk,
                    "user_id":f'{i.user.first_name} {i.user.last_name}',
                    "date":str(i.date),
                    "breakfast_meal":i.breakfast_meal,
                    "description":i.description
                })
            logger.info(f"Breakfast details retrieved successfully")
            return HttpResponse(
                json.dumps({"status":"success",
                            "message": f"Breakfast details retrieved successfully",
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
        
#=================================== Lunch =============================================================

class Lunch_details(generics.ListCreateAPIView):
    """Adding/Fetching Lunch details"""

    # permission_classes = (IsAuthenticated,)

    def post(self, request):
        """Adding Lunch details"""
        try:
            data = request.data

            user_id = User.objects.get(id=data['user_id']).pk
            date = data["date"]
            lunch_menu = data["lunch_menu"]
            description = data["description"]

            lunch_details_obj = bm_lunch(
                user_id = user_id,
                date = date,
                lunch_menu = lunch_menu,
                description = description
            )
            lunch_details_obj.save()
            logger.info(f"Lunch added successfully")
            return HttpResponse(
                json.dumps({"status":"success",
                            "message": f"Lunch added successfully"}),
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
        """Get Lunch details"""
        try:
            response_data = []
            data = request.GET
            isinstance_obj = isinstance(data, dict)
            if isinstance_obj and data:
                filter_data = {key: data[key] for key in data.keys()}
                person_date_lunch_obj = bm_lunch.objects.filter(**filter_data).order_by('id')
                # filter details using person_name_id or date or combination of both.
                for i in person_date_lunch_obj:
                    response_data.append({
                        "lunch_id":i.pk,
                        "user_id":f'{i.user.first_name} {i.user.last_name}',
                        "date":str(i.date),
                        "lunch_menu":i.lunch_menu,
                        "description":i.description
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
            lunch_data = bm_lunch.objects.all()
            for i in lunch_data:
                response_data.append({
                    "lunch_id":i.pk,
                    "user_id":f'{i.user.first_name} {i.user.last_name}',
                    "date":str(i.date),
                    "lunch_menu":i.lunch_menu,
                    "description":i.description
                })
            logger.info(f"Lunch details retrieved successfully")
            return HttpResponse(
                json.dumps({"status":"success",
                            "message": f"Lunch details retrieved successfully",
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
        
#=================================== Dinner =============================================================

class Dinner_details(generics.ListCreateAPIView):
    """Adding/Fetching Dinner details"""

    # permission_classes = (IsAuthenticated,)

    def post(self, request):
        """Adding dinner details"""
        try:
            data = request.data

            user_id = User.objects.get(id=data['user_id']).pk
            date = data["date"]
            dinner_menu = data["dinner_menu"]
            description = data["description"]

            dinner_details_obj = bm_dinner(
                user_id = user_id,
                date = date,
                dinner_menu = dinner_menu,
                description = description
            )
            dinner_details_obj.save()
            logger.info(f"Dinner added successfully")
            return HttpResponse(
                json.dumps({"status":"success",
                            "message": f"Dinner added successfully"}),
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
        """Get Dinner details"""
        try:
            response_data = []
            data = request.GET
            isinstance_obj = isinstance(data, dict)
            if isinstance_obj and data:
                filter_data = {key: data[key] for key in data.keys()}
                person_date_dinner_obj = bm_dinner.objects.filter(**filter_data).order_by('id')
                # filter details using person_name_id or date or combination of both.
                for i in person_date_dinner_obj:
                    response_data.append({
                        "dinner_id":i.pk,
                        "user_id":f'{i.user.first_name} {i.user.last_name}',
                        "date":str(i.date),
                        "dinner_menu":i.dinner_menu,
                        "description":i.description
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
            dinner_data = bm_dinner.objects.all()
            for i in dinner_data:
                response_data.append({
                    "dinner_id":i.pk,
                    "user_id":f'{i.user.first_name} {i.user.last_name}',
                    "date":str(i.date),
                    "dinner_menu":i.dinner_menu,
                    "description":i.description
                })
            logger.info(f"Dinner details retrieved successfully")
            return HttpResponse(
                json.dumps({"status":"success",
                            "message": f"Dinner details retrieved successfully",
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
        
#=================================== Total cal =============================================================

# class Calculate_total_calories(generics.ListCreateAPIView):
#     """Calculate/Fetching total calories"""

#     # permission_classes = (IsAuthenticated,)

#     def post(self, request):
#         """Calculate total calories"""
#         try:
#             data = request.data

#             person_name_id = data["person_name_id"]
#             date = data["date"]
#             is_data_exist = bm_total_calories.objects.filter(person_name_id=person_name_id,date=date)
#             if not is_data_exist:
#                 breakfast_calories = 0
#                 breakfast_calories_obj = bm_breakfast.objects.filter(person_name_id=person_name_id,date=date)
#                 for i in breakfast_calories_obj:
#                     breakfast_calories += i.dish_calories

#                 lunch_calories = 0
#                 lunch_calories_obj = bm_lunch.objects.filter(person_name_id=person_name_id,date=date)
#                 for i in lunch_calories_obj:
#                     lunch_calories += i.dish_calories

#                 dinner_calories = 0
#                 dinner_calories_obj = bm_dinner.objects.filter(person_name_id=person_name_id,date=date)
#                 for i in dinner_calories_obj:
#                     dinner_calories += i.dish_calories

#                 total_cal = breakfast_calories + lunch_calories + dinner_calories
#                 # print("total_cal : ",total_cal)
#                 total_calories_obj = bm_total_calories(
#                     person_name_id = bm_person_info.objects.get(pk=person_name_id).pk,
#                     date = date,
#                     total_calories = total_cal,
#                 )
#                 total_calories_obj.save()
#                 logger.info("Total calories added successfully")
#                 return HttpResponse(
#                     json.dumps({"status":"success",
#                                 "message": "Total calories added successfully"}),
#                     status=200,
#                     content_type="application/json",
#                 )
#             logger.info("Data already exist")
#             return HttpResponse(
#                 json.dumps({"status":"failed",
#                             "message": "Data already exist"}),
#                 status=200,
#                 content_type="application/json",
#             )
#         except Exception as msg:
#             logger.error(msg)
#             traceback.print_exc()
#             return HttpResponse(
#                 json.dumps({"status":"failed",
#                             "message": "There is backend issue, please contact administrator"}),
#                 status=200,
#                 content_type="application/json",
#             )
        
#     def get(self, request):
#         """Get total calories details"""
#         try:
#             response_data = []
#             data = request.GET
#             isinstance_obj = isinstance(data, dict)
#             if isinstance_obj and data:
#                 filter_data = {key: data[key] for key in data.keys()}
#                 person_total_cal_obj = bm_total_calories.objects.filter(**filter_data).order_by('id')
#                 # filter details using person_name_id or date or combination of both.
#                 for i in person_total_cal_obj:
#                     date = i.date
#                     response_data.append({
#                         "total_calories_id":i.pk,
#                         "person_name":i.person_name.person_name,
#                         "date":str(date),
#                         "total_calories":f"{i.total_calories} cal",
#                     })
#                 if len(response_data)==0:
#                     logger.info(f"Details of given input not found")
#                     return HttpResponse(
#                     json.dumps({"status":"failed",
#                                 "message": "Details of given input not found",
#                                 "data":response_data}),
#                     status=200,
#                     content_type="application/json",
#                     )
                
#                 else:
#                     logger.info(f"Details of given input retrieved successfully")
#                     return HttpResponse(
#                         json.dumps({"status":"success",
#                                     "message": f"Details of given input retrieved successfully",
#                                     "data":response_data}),
#                         status=200,
#                         content_type="application/json",
#                     )
#             total_calories_data = bm_total_calories.objects.all()
#             for i in total_calories_data:
#                 date = i.date
#                 response_data.append({
#                     "total_calories_id":i.pk,
#                     "person_name":i.person_name.person_name,
#                     "date":str(date),
#                     "total_calories":f"{i.total_calories} cal",
#                 })
#             logger.info("Total calories retrieved successfully")
#             return HttpResponse(
#                 json.dumps({"status":"success",
#                             "message": "Total calories retrieved successfully",
#                             "data":response_data}),
#                 status=200,
#                 content_type="application/json",
#             )
#         except Exception as msg:
#             logger.error(msg)
#             traceback.print_exc()
#             return HttpResponse(
#                 json.dumps({"status":"failed",
#                             "message": "There is backend issue, please contact administrator"}),
#                 status=200,
#                 content_type="application/json",
#             )