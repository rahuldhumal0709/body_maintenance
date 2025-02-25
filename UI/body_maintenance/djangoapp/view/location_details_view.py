from djangoapp.utilities.view_file_import import *

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
        location_data = trac_location_details.objects.all()
        for i in location_data:
            response_data.append({
                "id":i.pk,
                "location_name":i.location_name
            })
        msg = "Location retrieved successfully"
        logger.info(msg)
        return HttpResponse(
            json.dumps({"status":"success","message": msg,"data":response_data}),status=200,content_type="application/json")
    except Exception as msg:
        logger.error(msg)
        traceback.print_exc()
        return HttpResponse(
            json.dumps({"status":"failed","message": backend_issue}),status=200,content_type="application/json")

@api_view(['POST'])
def add_location_details(request):
    """Add new location"""
    try:
        response = Auth.anonymous(request)
        if response == 'authorized':
            pass
        else:
            return response
        location_name = request.data["location_name"]
        location_exist = trac_location_details.objects.filter(location_name=location_name).exists()
        if location_exist:
            logger.info("Location already exists")
            return HttpResponse(
                json.dumps({"status": "failed","message": "Location already exists"}),status=200,content_type="application/json")
        location_obj = trac_location_details(
            location_name = location_name
        )
        location_obj.save()
        msg = "Location added successfully"
        logger.info(msg)
        return HttpResponse(
            json.dumps({"status":"success","message": msg}),status=200,content_type="application/json")

    except Exception as msg:
        logger.error(msg)
        traceback.print_exc()
        return HttpResponse(
            json.dumps({"status":"failed","message": backend_issue}),status=200,content_type="application/json")