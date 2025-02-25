from djangoapp.utilities.view_file_import import *

@csrf_exempt
@api_view(['POST'])
@login_required
def add_user_info(request):
    """Adding User Details"""
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
        same_address = data['same_address']
        if same_address:
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
        User.objects.filter(pk=user_id).update(first_name=first_name,last_name=last_name)
        msg = "User details added successfully"
        logger.info(msg)
        return HttpResponse(
            json.dumps({"status":"success","message": msg}),status=200,content_type="application/json")
    except Exception as msg:
        logger.error(msg)
        traceback.print_exc()
        return HttpResponse(
            json.dumps({"status":"failed","message": backend_issue}),status=200,content_type="application/json")

@csrf_exempt
@api_view(['POST'])
@login_required
def update_user_info(request):
    """Update User Details"""
    try:
        data = request.data
        user_id = User.objects.get(id=data['user_id']).pk
        update_filter = {}
        if 'first_name' in data:
            update_filter['first_name'] = data['first_name']
            User.objects.filter(pk=user_id).update(first_name=data['first_name'])
        if 'last_name' in data:
            update_filter['last_name'] = data['last_name']
            User.objects.filter(pk=user_id).update(last_name=data['last_name'])
        if 'dob' in data:
            update_filter['dob'] = data['dob']
        if 'gender' in data:
            update_filter['gender'] = data['gender']
        if 'height' in data:
            update_filter['height'] = data['height']
        if 'education' in data:
            update_filter['education'] = data['education']
        if 'permanent_address' in data:
            update_filter['permanent_address'] = data['permanent_address']
        if 'current_address' in data:
            update_filter['current_address'] = data['current_address']
        if 'marital_status' in data:
            update_filter['marital_status'] = data['marital_status']
        bm_person_info.objects.filter(
            user_id =user_id
        ).update(**update_filter)
        msg = "User Details Updated Successfully"
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
def get_user_info(request):
    """Getting User Details"""
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
            msg = "User details retrieved successfully"
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
def add_user_weight(request):
    """Adding user weight"""
    try:
        data = request.data

        user_id = request.user.pk
        date = data["date"]
        weight_of_person = data["weight"]
        weight_details_obj = bm_weight(
            user_id = user_id,
            date = date,
            weight = weight_of_person
        )
        weight_details_obj.save()
        msg = "Weight added successfully"
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
def get_user_weight(request):
    """Getting weight Details"""
    try:
        response_data = []
        data = request.GET
        user = request.user
        if user.is_authenticated:
            filter_data = {key: data[key] for key in data.keys()}
            filter_data['user'] = user
            person_weight_obj = bm_weight.objects.filter(**filter_data).order_by('id')
            for i in person_weight_obj:
                response_data.append({
                    "weight_id":i.pk,
                    "full_name":f'{i.user.first_name} {i.user.last_name}',
                    "date":str(i.date),
                    "weight":i.weight
                })
            msg = "User weight retrieved successfully"
            logger.info(f"Details of given input ")
            return HttpResponse(
                json.dumps({"status":"success","message": msg,"data":response_data}),status=200,content_type="application/json")
    except Exception as msg:
        logger.error(msg)
        traceback.print_exc()
        return HttpResponse(
            json.dumps({"status":"failed","message": backend_issue}),status=200,content_type="application/json")