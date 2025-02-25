from djangoapp.utilities.view_file_import import *

@csrf_exempt
@api_view(['POST'])
@login_required
def add_bmi_details(request):
    """Adding bmi details"""
    try:
        data = request.data
        user_id = User.objects.get(id=data['user_id']).pk
        date = data["date_id"]
        my_height = bm_person_info.objects.get(user_id=user_id).height
        my_weight = bm_weight.objects.filter(user_id=user_id,date=date).first().weight
        my_bmi = round(my_weight / ((my_height/100) ** 2), 2)

        if 19 <= my_bmi <= 24:
            result = 'Good'
        elif my_bmi < 19:
            result = 'Underweight'
        else:
            result = 'Overweight'

        bmi_details_obj = bm_bmi(
            user_id = user_id,
            date = date,
            height = my_height,
            weight = my_weight,
            bmi = my_bmi,
            result = result,
        )
        bmi_details_obj.save()
        msg = "BMI added successfully"
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
def get_bmi_details(request):
    """Getting bmi details"""
    try:
        response_data = []
        data = request.GET
        user = request.user
        if user.is_authenticated:
            filter_data = {key: data[key] for key in data.keys()}
            filter_data['user'] = user
            person_date_bmi_obj = bm_bmi.objects.filter(**filter_data).order_by('id')
            for i in person_date_bmi_obj:
                response_data.append({
                    "bmi_id":i.pk,
                    "full_name":f'{i.user.first_name} {i.user.last_name}',
                    "date":str(i.date),
                    "height":i.height,
                    "weight":i.weight,
                    "BMI":f"{i.bmi} kg/m2",
                    "result":i.result
                })
            msg = "BMI details retrieved successfully"
            logger.info(msg)
            return HttpResponse(
                json.dumps({"status":"success","message": msg,"data":response_data}),status=200,content_type="application/json")
    except Exception as msg:
        logger.error(msg)
        traceback.print_exc()
        return HttpResponse(
            json.dumps({"status":"failed","message": backend_issue}),status=200,content_type="application/json")