import datetime
import json
import os
from django.conf import settings
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

#=================================== job_profile details =============================================================

class Job_profile_details(generics.ListCreateAPIView):
    """Adding and retrive job_profile details of person"""

    # permission_classes = (IsAuthenticated,)

    def post(self,request):
        """Adding job_profile details"""
        try:
            data = request.data

            person_name_id = bm_person_info.objects.get(pk=data["person_name_id"]).pk
            date = data["date"]
            company_name = data["company_name"]
            is_referral = data["is_referral"]

            if 'referral_person_name' in data:
                referral_person_name = data["referral_person_name"]
            else:
                referral_person_name = ''

            if 'platform' in data:
                platform = data["platform"]
            else:platform = ''
            
            for_which_role = data["for_which_role"]
            if 'resume' in data:
                resume = data["resume"]
            else:
                resume = ''
            # path = os.path.join(settings.MEDIA_ROOT)
            job_profile_details_obj = bm_job_profile(
                person_name_id = person_name_id,
                date = date,
                company_name = company_name,
                is_referral = is_referral,
                referral_person_name = referral_person_name,
                platform_name = platform,
                for_which_role = for_which_role,
                resume = resume
            )
            job_profile_details_obj.save()
            logger.info("Job profile details added successfully")
            return HttpResponse(
                json.dumps({"status":"success",
                            "message":"Job profile details added successfully"}),
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
        """Getting job_profile details"""
        try:
            response_data = []
            data = request.GET
            isinstance_obj = isinstance(data, dict)
            if isinstance_obj and data:
                filter_data = {key: data[key] for key in data.keys()}
                person_date_job_profile_obj = bm_job_profile.objects.filter(**filter_data).order_by('id')
                # filter details using person_name_id or date or combination of both.
                for i in person_date_job_profile_obj:
                    response_data.append({
                        "job_profile_id":i.pk,
                        "person_name":i.person_name.person_name,
                        "date":str(i.date),
                        "company_name":i.company_name,
                        "is_referral":i.is_referral,
                        "referral_person_name":i.referral_person_name,
                        "platform_name":i.platform_name,
                        "for_which_role":i.for_which_role,
                        "resume":str(i.resume)
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
            job_profile_data = bm_job_profile.objects.all()
            for i in job_profile_data:
                response_data.append({
                    "job_profile_id":i.pk,
                    "person_name":i.person_name.person_name,
                    "date":str(i.date),
                    "company_name":i.company_name,
                    "is_referral":i.is_referral,
                    "referral_person_name":i.referral_person_name,
                    "platform_name":i.platform_name,
                    "for_which_role":i.for_which_role,
                    "resume":str(i.resume)
                    })
            logger.info(f"Job profile details retrieved successfully")
            return HttpResponse(
                json.dumps({"status":"success",
                            "message": f"Job profile details retrieved successfully",
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
