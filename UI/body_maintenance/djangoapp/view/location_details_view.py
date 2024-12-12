"""
Location Details
"""
import logging
import traceback
import json
from django.http import HttpResponse
from rest_framework.decorators import api_view
from djangoapp.models import trac_location_details
from djangoapp.utilities.user_auth import Auth

# logging configuration
logger = logging.getLogger(__name__)
logger = logging.getLogger('django')

@api_view(['GET'])
def get_location_details(request):
    """Get location details"""
    try:
        # authenticate
        response = Auth.anonymous(request)
        if response == 'authorized':
            pass
        else:
            return response

        response_data = []
        # getting location details
        location_data = trac_location_details.objects.all()

        for i in location_data:
            response_data.append({
                "id":i.pk,
                "location_name":i.location_name
            })
        logger.info("Location data retrieved successfully")
        return HttpResponse(
            json.dumps({"status":"success",
                        "message": "Location data retrieved successfully","data":response_data}),
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


@api_view(['POST'])
def add_location_details(request):
    """Add new location"""
    try:
        # authenticate
        response = Auth.anonymous(request)
        if response == 'authorized':
            pass
        else:
            return response

        # getting data from request
        location_name = request.data["location_name"]

        # Check if any location with the given location exists
        location_exist = trac_location_details.objects.filter(location_name=location_name).exists()
        if location_exist:
            logger.info("Location already exists")
            return HttpResponse(
                json.dumps({"status": "failed",
                            "message": "Location already exists"}),
                            status=200,
                            content_type="application/json",
                            )

        location_obj = trac_location_details(
            location_name = location_name
        )

        location_obj.save()

        logger.info("Location added successfully")
        return HttpResponse(
            json.dumps({"status":"success",
                        "message": "Location added successfully"}),
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
