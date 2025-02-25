from djangoapp.utilities.view_file_import import *

@csrf_exempt
@api_view(['POST'])
@login_required
def add_exercise_details(request):
    """Adding exercise details"""
    try:
        data = request.data
        user_id = request.user.pk
        start_time = data["start_time"]
        end_time = data["end_time"]
        sets_of_parts = data["sets_of_parts"]
        efforts = data["efforts"]

        exercise_details_obj = bm_exercise(
            user_id = user_id,
            start_time = start_time,
            end_time = end_time,
            sets_of_parts = sets_of_parts,
            efforts = efforts
        )
        exercise_details_obj.save()
        msg = "Exercise details added successfully"
        logger.info(msg)
        return HttpResponse(
            json.dumps({"status":"success","message":msg}),status=200,content_type="application/json")
    except Exception as msg:
        logger.error(msg)
        traceback.print_exc()
        return HttpResponse(
            json.dumps({"status":"failed","message": backend_issue}),status=200,content_type="application/json")
    
@csrf_exempt
@api_view(['GET'])
@login_required
def get_exercise_details(request):
    """Getting exercise details"""
    try:
        response_data = []
        data = request.GET
        user = request.user
        if user.is_authenticated:
            filter_data = {key: data[key] for key in data.keys()}
            filter_data['user'] = user
            person_date_exercise_obj = bm_exercise.objects.filter(**filter_data).order_by('id')
            for i in person_date_exercise_obj:
                response_data.append({
                    "exercise_id":i.pk,
                    "full_name":f'{i.user.first_name} {i.user.last_name}',
                    "date":str(i.date),
                    "start_time":str(i.start_time),
                    "end_time":str(i.end_time),
                    "sets_of_parts":i.sets_of_parts,
                    "efforts":f"{i.efforts} %"
                })
            msg = "Exercise details retrieved successfully"
            logger.info(msg)
            return HttpResponse(
                json.dumps({"status":"success","message": msg,"data":response_data}),status=200,content_type="application/json")
    except Exception as msg:
        logger.error(msg)
        traceback.print_exc()
        return HttpResponse(
            json.dumps({"status":"failed","message": backend_issue}),status=200,content_type="application/json")