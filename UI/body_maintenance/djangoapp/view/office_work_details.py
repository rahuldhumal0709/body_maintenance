from djangoapp.utilities.view_file_import import *

@csrf_exempt
@api_view(['POST'])
@login_required
def add_office_work(request):
    """Adding office work details"""
    try:
        data = request.data

        user_id = User.objects.get(id=data['user_id']).pk
        date = data["date"]
        start_time = data["start_time"]
        end_time = data["end_time"]
        work = data["work"]
        description = data["description"]
        efforts = data["efforts"]

        office_details_obj = bm_office(
            user_id = user_id,
            date = date,
            start_time = start_time,
            end_time = end_time,
            work = work,
            description = description,
            efforts = efforts
        )
        office_details_obj.save()
        msg = "Office work details added successfully"
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
def get_office_work_details(request):
    """Getting office work details"""
    try:
        response_data = []
        data = request.GET
        user = request.user
        if user.is_authenticated:
            filter_data = {key: data[key] for key in data.keys()}
            filter_data['user'] = user
            person_date_office_obj = bm_office.objects.filter(**filter_data).order_by('id')
            for i in person_date_office_obj:
                start_time = datetime.datetime.combine(i.date, i.start_time)
                end_time = datetime.datetime.combine(i.date, i.end_time)
                total_working_time = end_time - start_time
                response_data.append({
                    "office_id":i.pk,
                    "full_name":f'{i.user.first_name} {i.user.last_name}',
                    "date":str(i.date),
                    "start_time":str(i.start_time),
                    "end_time":str(i.end_time),
                    "total_working_time":str(total_working_time),
                    "work":i.work,
                    "description":i.description,
                    "efforts":f"{i.efforts} %"
                })
            msg = "Office work details retrieved successfully"
            logger.info(msg)
            return HttpResponse(
                json.dumps({"status":"success","message": msg,"data":response_data}),status=200,content_type="application/json")
    except Exception as msg:
        logger.error(msg)
        traceback.print_exc()
        return HttpResponse(
            json.dumps({"status":"failed","message": backend_issue}),status=200,content_type="application/json")
