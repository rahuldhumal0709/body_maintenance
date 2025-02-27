from djangoapp.utilities.view_file_import import *

@csrf_exempt
@api_view(['POST'])
@login_required
def add_subject(request):
    """Adding subject"""
    try:
        data = request.data
        subject_name = data["subject_name"]
        subject_obj = bm_subject_names(
            subject_name = subject_name,
        )
        subject_obj.save()
        msg = "Subject added successfully"
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
def get_subject_names(request):
    """Getting subjects"""
    try:
        response_data = []
        subject_obj = bm_subject_names.objects.all()
        for i in subject_obj:
            response_data.append({
                "subject_id":i.pk,
                "subject_name":i.subject_name,
            })
        msg = "Subject names retrieved successfully"
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
def add_subject_details(request):
    """Adding subject details"""
    try:
        data = request.data
        user_id = User.objects.get(id=data['user_id']).pk
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
            user_id = user_id,
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
        msg = "Subject details added successfully"
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
def get_subject_details(request):
    """Getting subject all details"""
    try:
        response_data = []
        data = request.GET
        user = request.user
        if user.is_authenticated:
            filter_data = {key: data[key] for key in data.keys()}
            filter_data['user'] = user
            person_date_subject_obj = bm_subject_details.objects.filter(**filter_data).order_by('id')
            for i in person_date_subject_obj:
                start_time = datetime.datetime.combine(i.date, i.start_time)
                end_time = datetime.datetime.combine(i.date, i.end_time)
                total_study_time_of_subject = end_time - start_time
                response_data.append({
                    "subject_all_id":i.pk,
                    "full_name":f'{i.user.first_name} {i.user.last_name}',
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
            msg = "Subject details retrieved successfully"
            logger.info(msg)
            return HttpResponse(
                json.dumps({"status":"success","message": msg,"data":response_data}),status=200,content_type="application/json")
    except Exception as msg:
        logger.error(msg)
        traceback.print_exc()
        return HttpResponse(
            json.dumps({"status":"failed","message": backend_issue}),status=200,content_type="application/json")