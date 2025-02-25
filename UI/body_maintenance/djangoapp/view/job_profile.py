from djangoapp.utilities.view_file_import import *

@csrf_exempt
@api_view(['POST'])
@login_required
def add_job_profile(request):
    """Adding job profile details"""
    try:
        data = request.data
        user_id = User.objects.get(id=data['user_id']).pk
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
        job_profile_details_obj = bm_job_profile(
            user_id = user_id,
            date = date,
            company_name = company_name,
            is_referral = is_referral,
            referral_person_name = referral_person_name,
            platform_name = platform,
            for_which_role = for_which_role,
            resume = resume
        )
        job_profile_details_obj.save()
        msg = "Job profile details added successfully"
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
def get_job_profile_details(request):
    """Getting job profile details"""
    try:
        response_data = []
        data = request.GET
        user = request.user
        if user.is_authenticated:
            filter_data = {key: data[key] for key in data.keys()}
            filter_data['user'] = user
            person_date_job_profile_obj = bm_job_profile.objects.filter(**filter_data).order_by('id')
            for i in person_date_job_profile_obj:
                response_data.append({
                    "job_profile_id":i.pk,
                    "full_name":f'{i.user.first_name} {i.user.last_name}',
                    "date":str(i.date),
                    "company_name":i.company_name,
                    "is_referral":i.is_referral,
                    "referral_person_name":i.referral_person_name,
                    "platform_name":i.platform_name,
                    "for_which_role":i.for_which_role,
                    "resume":str(i.resume)
                })
            msg = "Job profile details retrieved successfully"
            logger.info(f"Details of given input ")
            return HttpResponse(
                json.dumps({"status":"success","message": msg,"data":response_data}),status=200,content_type="application/json")
    except Exception as msg:
        logger.error(msg)
        traceback.print_exc()
        return HttpResponse(
            json.dumps({"status":"failed","message": backend_issue}),status=200,content_type="application/json")
