from djangoapp.utilities.view_file_import import *

@csrf_exempt
@api_view(['GET'])
def get_user_profile(request):
    try:
        data_list = []
        user_id = request.user.pk
        employee_obj = employee_config.objects.get(auth_user_id=user_id)
        first_name = employee_obj.first_name
        last_name = employee_obj.last_name
        email = employee_obj.emailaddress
        phone = employee_obj.phone
        date_of_join = employee_obj.dateof_joining
        department = employee_obj.department.department_name
        emp_id = employee_obj.pk
        designation = employee_obj.designation.designation
        role_obj = employee_role.objects.filter(employee_id=emp_id)
        data_list1 = []
        for i in role_obj:
            data_list1.append({"employee_role": i.roles.role_name})

        data_list.append(
            {
                "full_name": first_name + " " + last_name,
                "first_name": first_name,
                "last_name": last_name,
                "email": email,
                "contact": phone,
                "date_of_joining": str(date_of_join),
                "department": department,
                "designation": designation,
                "employee_role": data_list1,
            }
        )
        msg = "User profile retrieved successfully"
        logger.info(msg)
        return HttpResponse(
            json.dumps(
                {"status": "success","message": msg,"data": data_list}))
    except Exception as msg:
        logger.error(msg)
        traceback.print_exc()
        return HttpResponse(
            json.dumps(
                {"status": "Failed", "message": backend_issue}))