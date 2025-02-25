from djangoapp.utilities.view_file_import import *

@csrf_exempt
@api_view(['POST'])
@login_required
def add_meal_type(request):
    """Adding Meal type"""
    try:
        data = request.data
        meal_type = data["meal_type"]
        meal_type_obj = bm_meal_type(
            meal_type = meal_type
        )
        meal_type_obj.save()
        msg = "Meal type added successfully"
        logger.info(msg)
        return HttpResponse(
            json.dumps({"status":"success","message": msg}),status=200,content_type="application/json")
    except Exception as msg:
        logger.error(msg)
        traceback.print_exc()
        return HttpResponse(
            json.dumps({"status":"failed","message": backend_issue}),status=200,content_type="application/json")
    
@csrf_exempt
@api_view(['GET'])
@login_required
def get_meal_types(request):
    """Getting Meal types"""
    try:
        response_data = []
        meal_type_obj = bm_meal_type.objects.all()
        for i in meal_type_obj:
            response_data.append({
                "meal_type_id":i.pk,
                "name":i.name
            })
        msg = "Meal types retrieved successfully"
        logger.info(msg)
        return HttpResponse(
            json.dumps({"status":"success","message": msg,"data":response_data}),status=200,content_type="application/json")
    except Exception as msg:
        logger.error(msg)
        traceback.print_exc()
        return HttpResponse(
            json.dumps({"status":"failed","message": backend_issue}),status=200,content_type="application/json")

@csrf_exempt
@api_view(['POST'])
@login_required
def add_meal_details(request):
    """Adding Meal details"""
    try:
        data = request.data

        user_id = User.objects.get(id=data['user_id']).pk
        date = data["date"]
        meal_type_id = data["meal_type_id"]
        meal = data["meal"]
        description = data["description"]

        meal_details_obj = bm_meal(
            user_id = user_id,
            date = date,
            meal_type_id = meal_type_id,
            meal = meal,
            description = description
        )
        meal_details_obj.save()
        msg = "Meal added successfully"
        logger.info(msg)
        return HttpResponse(
            json.dumps({"status":"success","message": msg}),status=200,content_type="application/json")
    except Exception as msg:
        logger.error(msg)
        traceback.print_exc()
        return HttpResponse(
            json.dumps({"status":"failed","message": backend_issue}),status=200,content_type="application/json")
    
@csrf_exempt
@api_view(['GET'])
@login_required
def get_meal_details(request):
    """Getting Meal Details"""
    try:
        response_data = []
        data = request.GET
        user = request.user
        if user.is_authenticated:
            filter_data = {key: data[key] for key in data.keys()}
            filter_data['user'] = user
            person_date_breakfast_obj = bm_meal.objects.filter(**filter_data).order_by('id')
            for i in person_date_breakfast_obj:
                response_data.append({
                    "meal_id":i.pk,
                    "full_name":f'{i.user.first_name} {i.user.last_name}',
                    "date":str(i.date),
                    "meal_type":i.meal_type.name,
                    "meal":i.meal,
                    "description":i.description
                })
            msg = "Meal Details retrieved successfully"
            logger.info(msg)
            return HttpResponse(
                json.dumps({"status":"success","message": msg,"data":response_data}),status=200,content_type="application/json")
    except Exception as msg:
        logger.error(msg)
        traceback.print_exc()
        return HttpResponse(
            json.dumps({"status":"failed","message": backend_issue}),status=200,content_type="application/json")