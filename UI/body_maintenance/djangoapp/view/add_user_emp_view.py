from djangoapp.utilities.view_file_import import *
from djangoapp.utilities.validation import *
import threading
from django.db.models import Q
from djangoapp.utilities.send_acknowledge_email_view import *

logger = logging.getLogger(__name__)
logger = logging.getLogger("django")


class add_employee_user(generics.ListCreateAPIView):
    """For adding employee & getting employee details"""

    permission_classes = (IsAuthenticated,)

    def post(self, request):
        try:
            data = request.data
            if "action" in data:
                action = data["action"]
            else:
                logger.error("Transaction Action Not Provided")
                return HttpResponse(
                    json.dumps(
                        {
                            "status": "failed",
                            "message": "Please Provide Action to Perform",
                        }
                    )
                )

            if action == "Insert":
                first_name = data["first_name"]
                check = validate_string_only(first_name)
                if not check:
                    logger.error("Please Provide Valid First Name")
                    return HttpResponse(
                        json.dumps(
                            {
                                "status": "failed",
                                "message": "Please Provide Valid First Name",
                            }
                        )
                    )

                last_name = data["last_name"]
                if last_name is not None:
                    check = validate_string_only(last_name)
                    if not check:
                        logger.error("Please Provide Valid Last Name")
                        return HttpResponse(
                            json.dumps(
                                {
                                    "status": "failed",
                                    "message": "Please Provide Valid Last Name",
                                }
                            )
                        )

                email_address = data["email"]
                check = validate_email(email_address)
                if not check:
                    logger.error("Please Provide Valid email")
                    return HttpResponse(
                        json.dumps(
                            {
                                "status": "failed",
                                "message": "Please Provide Valid Email",
                            }
                        )
                    )
                email = str(email_address).strip()
                check_email = User.objects.filter(username=email).exists()
                if check_email:
                    logger.info("employee with same email already exists")
                    return HttpResponse(
                        json.dumps(
                            {
                                "status": "failed",
                                "message": "Employee with same email already exists",
                            }
                        )
                    )
                username = email
                password = "Welcome@123"

                phone = data["contact"]
                if phone is not None:
                    check_contact = validate_id(phone)
                    if not check_contact:
                        logger.info("please provide valid contact")
                        return HttpResponse(
                            json.dumps(
                                {
                                    "status": "failed",
                                    "message": "Please Provide Valid Contact",
                                }
                            )
                        )
                
                if not request.data.get('isLoginAllowed'):
                    isloginallowed = False
                else:
                    isloginallowed = request.data.get('isLoginAllowed')

                required_fields = ["department_id", "designation_id", "role_id"]
                missing_fields = [
                    field for field in required_fields if field not in data
                ]

                if missing_fields:
                    logger.error("if missing fields")
                    return HttpResponse(
                        json.dumps(
                            {
                                "status": "failed",
                                "message": f"Please Provide {', '.join(missing_fields).replace('_id','')}",
                            }
                        )
                    )
                if 'location' in data and data['location'] not in [None,""]:
                    location = data['location']
                else:
                    location=None
                department_id = depart_config.objects.get(id=data["department_id"]).pk
                designation_id = desig_config.objects.get(id=data["designation_id"]).pk
                user_obj = User.objects.create_user(
                    first_name=first_name,
                    # last_name=last_name,
                    username=username,
                    email=email,
                    password=password,
                    is_active = isloginallowed
                )
                logger.info("employee in Auth_User created Successfully")
                user_obj.save()
                auth_user_id = user_obj.pk
                emp_obj = employee_config(
                    auth_user_id_id=auth_user_id,
                    first_name=first_name,
                    last_name=last_name,
                    location_id=location,
                    phone=phone,
                    emailaddress=email,
                    department_id=department_id,
                    designation_id=designation_id,
                )
                emp_obj.save()
                logger.info("employee in employee table created Successfully")
                subject = "Your Default Password"
                recipient_list = [email]
                # creating massage template
                html_temp = """<html>
                <head></head>
                <body>
                    <h2>Octillion Power Application Credentials</h2>
                    <h3>Hi {first_name},</h3>
                    <hr width="480px;" color="Gray" size="2" align="left">
                    <p>User {first_name} Created successfully and Your default password is <strong font-size="30px">Welcome@123</strong></p>
                    <p>If you want to change your password then go to forgot password option.</a></p><br><br>
                    <p>Thank You!<br>Team Nexgensis<br>info@nexgensis.com</p>

                </body>
                </html>""".format(
                    first_name=first_name
                )
                # sending mail by using send_acknowledge_email method by passing subject,html_temp,recipient_list
                thread = threading.Thread(
                    target=send_acknowledge_email,
                    args=(subject, html_temp, recipient_list),
                )
                thread.start()
                logger.info("email send Successfully")

                role_id1 = str(data["role_id"]).split(",")
                for i in role_id1:
                    role_id = role.objects.get(id=int(i)).pk
                    emp_role_obj = employee_role(
                        employee_id=emp_obj.pk, roles_id=role_id
                    )
                    emp_role_obj.save()
                # NEW
                # default_module_list=['My_Tickets','Created_by_me','Pending_Tickets']
                # module_name_id=access_module.objects.filter(module_name__in=default_module_list)
                # for i in module_name_id:
                #     acc_obj=access_module_config(
                #         create_access=False,
                #         read_access=True,
                #         update_access=False,
                #         delete_access=False,
                #         module_name_id=i.pk,
                #         role_id=role_id
                #     )
                #     acc_obj.save()

                logger.info("employee role added Successfully")
                return HttpResponse(
                    json.dumps(
                        {
                            "status": "success",
                            "message": "Employee created successfully",
                        }
                    )
                )
            elif action == "Update":
                if "employee_id" not in data or data['employee_id'] in [None,""]:
                    return HttpResponse(
                    json.dumps(
                        {
                            "status": "failed",
                            "message": "Please Provided Employee ID",
                        }
                    )
                )
                employee_id = data['employee_id']
                if not employee_config.objects.filter(id = employee_id,is_active = True).exists():
                    return HttpResponse(
                        json.dumps({
                                "status": "failed",
                                "message": "Employee ID Does Not Exists",
                            }))
                data_obj = employee_config.objects.get(id=employee_id)
                user_profile_dict = {}
                auth_id=data_obj.auth_user_id.pk
                user_profile_dict['auth_user_id_id'] = auth_id
                if "first_name" in data and data['first_name'] not in [None,""]:
                    user_profile_dict["first_name"] = data["first_name"]
                    User.objects.filter(id=auth_id).update(first_name=data["first_name"])
                else:
                    user_profile_dict["first_name"] = data_obj.first_name
                if "last_name" in data:
                    user_profile_dict["last_name"] = data['last_name']
                    User.objects.filter(id=auth_id).update(last_name=data["last_name"])
                else:
                    user_profile_dict["first_name"] = data_obj.last_name
                if "contact" in data:
                    user_profile_dict["phone"] = data["contact"]
                else:
                    user_profile_dict["phone"] = data_obj.phone
                if "department_id" in data:
                    department_id = depart_config.objects.get(
                        id=data["department_id"]
                    ).pk
                    user_profile_dict["department_id"] = department_id
                else:
                    user_profile_dict["department_id"] = data_obj.department_id
                if "designation_id" in data:
                    designation_id = desig_config.objects.get(
                        id=data["designation_id"]
                    ).pk
                    user_profile_dict["designation_id"] = designation_id
                else:
                    user_profile_dict["designation_id"] = data_obj.designation_id
                if "email" in data:
                    email = str(data["email"]).strip()
                    if data_obj.emailaddress == email:
                        pass
                    else:
                        if_exists = employee_config.objects.filter(
                            emailaddress=email
                        ).exists()
                        if if_exists:
                            logger.info("Email already exists")
                            return HttpResponse(
                                json.dumps(
                                    {
                                        "status": "failed",
                                        "message": "Email already exists",
                                    }
                                )
                            )
                    user_profile_dict["emailaddress"] = email
                    User.objects.filter(pk=auth_id).update(username=email)
                    User.objects.filter(pk=auth_id).update(email=email)
                else:
                    user_profile_dict["emailaddress"] = data_obj.emailaddress
                if request.data.get('isLoginAllowed'):
                    isloginallowed = request.data.get('isLoginAllowed')
                    User.objects.filter(pk=auth_id).update(is_active = isloginallowed)
                else:
                    pass
                if 'location' in data and data['location'] not in [None,'']:
                    location = data['location']
                    user_profile_dict["location_id"] = location
                else:
                    user_profile_dict["locations"] = data_obj.locations
                if employee_config.objects.filter(**user_profile_dict).filter(pk = employee_id).exists():
                    return HttpResponse(
                    json.dumps(
                        {
                            "status": "success",
                            "message": "No changes made",
                        }
                    )
                )
                user_profile_dict["action"] = "Update"
                # print("***********",user_profile_dict)
                new_obj = employee_config.objects.create(**user_profile_dict)
                employee_config.objects.filter(pk = data_obj.pk).update(
                    is_active = False,
                    is_deleted = True,
                    auth_user_id = None
                )
                if "role_id" in data:
                    # employee_role.objects.filter(employee_id=id).delete()
                    role_id1 = str(data["role_id"]).split(",")
                    for i in role_id1:
                        role_id = role.objects.get(pk=int(i)).pk
                        role_obj = employee_role(employee_id=new_obj.pk, roles_id=role_id)
                        role_obj.save()
                logger.info("employee updated Successfully")
                return HttpResponse(
                    json.dumps(
                        {
                            "status": "success",
                            "message": "Employee updated successfully",
                        }
                    )
                )
            elif action == "Delete":
                if "employee_id" not in data or data['employee_id'] in [None,""]:
                    return HttpResponse(
                    json.dumps(
                        {
                            "status": "failed",
                            "message": "Please Provided Employee ID",
                        }
                    )
                )
                employee_id = data['employee_id']
                if employee_config.objects.filter(id = employee_id,is_active = True).exists():
                    data_obj = employee_config.objects.get(id=employee_id)
                    data_obj.is_active = False
                    data_obj.is_deleted = True
                    auth_obj = data_obj.auth_user_id
                    data_obj.auth_user_id = None
                    data_obj.save()
                    auth_obj.delete()
                    return HttpResponse(
                        json.dumps({
                                "status": "success",
                                "message": "Employee ID Deleted Successfully",
                        }))
                else:
                    return HttpResponse(
                        json.dumps({
                                "status": "failed",
                                "message": "Employee ID Does Not Exists",
                        }))
            else:
                return HttpResponse(
                        json.dumps({
                                "status": "failed",
                                "message": "Valid actions are : Insert, Update, Delete",
                        }))
        except Exception as msg:
            logger.error(msg)
            traceback.print_exc()
            return HttpResponse(
                json.dumps(
                    {"status": "failed", "message": "please contact administrator"}
                )
            )

    def get(self, request):
        try:
            data_list = []
            data = request.GET
            if "page_number" in request.GET:
                page_number = int(request.GET["page_number"])
            else:
                page_number = 1

            start = int((int(page_number) * 15) - 15)
            end = page_number * 15
            if "search_item" in data:
                search_item = data["search_item"]
                if "designation_id" in data and "department_id" in data:
                    department_id = str(request.GET["department_id"]).split(",")
                    dept_list = []
                    desi_list = []
                    for i in department_id:
                        dep_id = depart_config.objects.get(pk=int(i)).pk
                        dept_list.append(dep_id)
                    designation_id = str(data["designation_id"]).split(",")
                    for j in designation_id:
                        desig_id = desig_config.objects.get(pk=int(j)).pk
                        desi_list.append(desig_id)
                    q_object = Q(department_id__in=dept_list) & Q(
                        designation_id__in=desi_list
                    )
                    data_obj = (
                        employee_config.objects.filter(q_object, is_deleted=False)
                        .filter(
                            Q(first_name__icontains=search_item)
                            | Q(last_name__icontains=search_item)
                        )[start:end]
                    )
                    data_obj1 = (
                        employee_config.objects.filter(q_object, is_deleted=False)
                        .filter(
                            Q(first_name__icontains=search_item)
                            | Q(last_name__icontains=search_item)
                        )
                    )
                    data_obj_count = (
                        employee_config.objects.filter(q_object, is_deleted=False)
                        .filter(
                            Q(first_name__icontains=search_item)
                            | Q(last_name__icontains=search_item)
                        )
                        .count()
                    )
                elif "department_id" in data:
                    logger.info("if department in data")
                    department_id = str(request.GET["department_id"]).split(",")
                    dept_list = []
                    for i in department_id:
                        dep_id = depart_config.objects.get(pk=int(i)).pk
                        dept_list.append(dep_id)
                    data_obj = (
                        employee_config.objects.filter(
                            department_id__in=dept_list, is_deleted=False
                        )
                        .filter(
                            Q(first_name__icontains=search_item)
                            | Q(last_name__icontains=search_item)
                        )[start:end]
                    )
                    data_obj1 = (
                        employee_config.objects.filter(
                            department_id__in=dept_list, is_deleted=False
                        )
                        .filter(
                            Q(first_name__icontains=search_item)
                            | Q(last_name__icontains=search_item)
                        )
                    )
                    data_obj_count = (
                        employee_config.objects.filter(
                            department_id__in=dept_list, is_deleted=False
                        )
                        .filter(
                            Q(first_name__icontains=search_item)
                            | Q(last_name__icontains=search_item)
                        )
                        .count()
                    )
                elif "designation_id" in data:
                    desi_list = []
                    designation_id = str(data["designation_id"]).split(",")
                    for j in designation_id:
                        desig_id = desig_config.objects.get(pk=int(j)).pk
                        desi_list.append(desig_id)
                    data_obj = (
                        employee_config.objects.filter(
                            designation_id__in=desi_list, is_deleted=False
                        )
                        .filter(
                            Q(first_name__icontains=search_item)
                            | Q(last_name__icontains=search_item)
                        )[start:end]
                    )
                    data_obj1 = (
                        employee_config.objects.filter(
                            designation_id__in=desi_list, is_deleted=False
                        )
                        .filter(
                            Q(first_name__icontains=search_item)
                            | Q(last_name__icontains=search_item)
                        )
                    )
                    data_obj_count = (
                        employee_config.objects.filter(
                            designation_id__in=desi_list, is_deleted=False
                        )
                        .filter(
                            Q(first_name__icontains=search_item)
                            | Q(last_name__icontains=search_item)
                        )
                        .count()
                    )
                else:

                    data_obj = (
                        employee_config.objects.filter(is_deleted=False)
                        .order_by("-id")
                        .filter(
                            Q(first_name__icontains=search_item)
                            | Q(last_name__icontains=search_item)
                        )[start:end]
                    )
                    data_obj1 = (
                        employee_config.objects.filter(is_deleted=False)
                        .order_by("-id")
                        .filter(
                            Q(first_name__icontains=search_item)
                            | Q(last_name__icontains=search_item)
                        )
                    )
                    data_obj_count = (
                        employee_config.objects.filter(is_deleted=False)
                        .order_by("-id")
                        .filter(
                            Q(first_name__icontains=search_item)
                            | Q(last_name__icontains=search_item)
                        )
                        .count()
                    )

            else:
                if "designation_id" in data and "department_id" in data:
                    department_id = str(request.GET["department_id"]).split(",")
                    dept_list = []
                    desi_list = []
                    for i in department_id:
                        dep_id = depart_config.objects.get(pk=int(i)).pk
                        dept_list.append(dep_id)
                    designation_id = str(data["designation_id"]).split(",")
                    for j in designation_id:
                        desig_id = desig_config.objects.get(pk=int(j)).pk
                        desi_list.append(desig_id)
                    q_object = Q(department_id__in=dept_list) & Q(
                        designation_id__in=desi_list
                    )
                    data_obj = employee_config.objects.filter(
                        q_object, is_deleted=False
                    )[start:end]
                    data_obj1 = employee_config.objects.filter(
                        q_object, is_deleted=False
                    )
                    data_obj_count = (
                        employee_config.objects.filter(q_object, is_deleted=False)
                        .count()
                    )
                elif "department_id" in data:
                    logger.info("if department in data")
                    department_id = str(request.GET["department_id"]).split(",")
                    dept_list = []
                    for i in department_id:
                        dep_id = depart_config.objects.get(pk=int(i)).pk
                        dept_list.append(dep_id)
                    data_obj = employee_config.objects.filter(
                        department_id__in=dept_list, is_deleted=False
                    )[start:end]
                    data_obj1 = employee_config.objects.filter(
                        department_id__in=dept_list, is_deleted=False
                    )
                    data_obj_count = (
                        employee_config.objects.filter(
                            department_id__in=dept_list, is_deleted=False
                        )
                        .count()
                    )
                elif "designation_id" in data:
                    desi_list = []
                    designation_id = str(data["designation_id"]).split(",")
                    for j in designation_id:
                        desig_id = desig_config.objects.get(pk=int(j)).pk
                        desi_list.append(desig_id)
                    data_obj = employee_config.objects.filter(
                        designation_id__in=desi_list, is_deleted=False
                    )[start:end]
                    data_obj1 = employee_config.objects.filter(
                        designation_id__in=desi_list, is_deleted=False
                    )
                    data_obj_count = (
                        employee_config.objects.filter(
                            designation_id__in=desi_list, is_deleted=False
                        )
                        .count()
                    )
                else:

                    data_obj = (
                        employee_config.objects.filter(is_deleted=False)
                        .order_by("-id")[start:end]
                    )
                    data_obj1 = employee_config.objects.filter(
                        is_deleted=False
                    )
                    data_obj_count = (
                        employee_config.objects.filter(is_deleted=False)
                        .count()
                    )
            max_page_number = int(math.ceil(len(data_obj1) / 15))
            for data in data_obj:
                data_list2 = []
                data_list3 = []
                data_list4 = []
                data_list5 = []
                try:
                    employee_unique_id = str(
                        str(data.first_name[0]).capitalize()
                        + str(data.last_name[0]).capitalize()
                        + "-"
                        + "00"
                        + str(data.pk)
                    )
                except:
                    employee_unique_id = ""
                    
                try:
                    location = data.location.location_name
                    location_id = data.location.pk
                except Exception as e:
                    location=''
                    location_id = ''
                # print(employee_unique_id, "employee_unique_id")
                employee_id = data.pk
                role_obj = employee_role.objects.filter(employee_id=employee_id)
                for k in role_obj:
                    role_id = k.roles.pk
                    data_list2.append(k.roles.pk)
                    data_list3.append(k.roles.role_name)
                    group_obj = role_group_config.objects.filter(
                        role_id=role_id
                    ).distinct("group_id")
                    for n in group_obj:
                        data_list4.append(
                            n.group.pk,
                        )
                        data_list5.append(n.group.group_name)

                logger.info("data appended")
                data_list.append(
                    {
                        "employee_unique_id": employee_unique_id,
                        "employee_id": data.pk,
                        "employee_name": (data.first_name + " " + data.last_name) if data.last_name else data.first_name,
                        "email": data.emailaddress,
                        "contact": data.phone,
                        "department": data.department.department_name,
                        "department_id": data.department.pk,
                        "designation": data.designation.designation,
                        "designation_id": data.designation.pk,
                        # "employee_role_details":data_list1,
                        "location":location,
                        'location_id':location_id,
                        "role_id": str(data_list2),
                        "role_name": str(data_list3),
                    }
                )
            logger.info("employee details retrived Successfully")
            return HttpResponse(
                json.dumps(
                    {
                        "status": "success",
                        "message": "Employee details retrived successfully",
                        "data": data_list,
                        "max_pages": max_page_number,
                        "obj_count": data_obj_count,
                    }
                )
            )

        except Exception as msg:
            logger.error(msg)
            traceback.print_exc()
            return HttpResponse(
                json.dumps(
                    {"status": "failed", "message": "please contact administrator"}
                )
            )


class get_employee_by_role(generics.ListCreateAPIView):
    """getting employees for request role_ids"""

    permission_classes = (IsAuthenticated,)

    def get(self, request):
        try:
            data_list = []
            role_id = str(request.GET["role_id"]).split(",")
            logger.info("getting multiple role by spliting")
            for i in role_id:
                role_id1 = role.objects.get(pk=int(i)).pk
                emp_obj = employee_role.objects.filter(roles_id=role_id1)
                logger.info("filter employee by roles")
                for j in emp_obj:
                    data_list.append(
                        {
                            # "role_id":j.roles.pk,
                            "employee_id": j.employee.pk,
                            "employee_name": j.employee.first_name
                            + " "
                            + j.employee.last_name,
                        }
                    )

            distinct_dicts = []
            for d in data_list:
                if d not in distinct_dicts:
                    distinct_dicts.append(d)

            data_list = distinct_dicts

            logger.info("employee  retrived Successfully")
            return HttpResponse(
                json.dumps(
                    {
                        "status": "success",
                        "message": "Employee retrived successfully",
                        "data": data_list,
                    }
                )
            )

        except Exception as msg:
            logger.error(msg)
            traceback.print_exc()
            return HttpResponse(
                json.dumps(
                    {"status": "failed", "message": "please contact administrator"}
                )
            )

class get_roles(generics.ListCreateAPIView):
    """getting roles"""

    permission_classes = (IsAuthenticated,)

    def get(self, request):
        try:
            data_list = []
            # data_obj1 = role.objects.filter(role_name__in=["My Manager"])
            # for data in data_obj1:
            #     data_list.append({
            #         "role_id":data.pk,
            #         "role":data.role_name
            #     })
            data_obj2 = role.objects.exclude(
                role_name__in=["All", "Self", "Default", "My Manager"]
            ).filter(is_deleted=False)
            for i in data_obj2:
                # role_check=employee_role.objects.filter(roles_id=i.pk)
                # if role_check.count()>0:
                data_list.append(
                    {
                        "role_id": i.pk,
                        "role": i.role_name,
                        # "priority":i.   #NEW
                    }
                )
            logger.info("role details retrieved successfully")
            return HttpResponse(
                json.dumps(
                    {
                        "status": "success",
                        "message": "roles retrieved successfully",
                        "data": data_list,
                    }
                )
            )

        except Exception as msg:
            logger.error(msg)
            traceback.print_exc()
            return HttpResponse(
                json.dumps(
                    {"status": "failed", "message": "please contact administrator"}
                )
            )


@csrf_exempt
@api_view(["GET"])
def get_all_employee(request):
    try:
        data_list = []
        data_obj = (
            employee_config.objects.filter(is_deleted=False)
            .order_by("id")
        )
        for i in data_obj:
            data_list.append(
                {
                    "employee_id": i.pk,
                    "first_name": i.first_name,
                    "last_name": i.last_name,
                    "full_name": i.first_name + " " + i.last_name,
                }
            )
        logger.info("employee retrieved successfully")
        return HttpResponse(
            json.dumps(
                {
                    "status": "success",
                    "message": "Employee data retrieved successfully",
                    "data": data_list,
                }
            )
        )

    except Exception as msg:
        logger.error(f"technician data retrieval failed: {msg}")
        traceback.print_exc()
        return HttpResponse(
            json.dumps({"status": "failed", "message": "please contact administrator"})
        )

@csrf_exempt
@api_view(['POST'])
def add_role(request):
    try:
        data = request.data

        role_name = data.get('role_name')
        role_type= data.get('role_type',0)
        is_deleted=data.get('is_deleted',False)

        if not role_name:
            return HttpResponse(
                json.dumps({"status": "failed", "message": "Role name is required."}),
                status=200,
                content_type="application/json"
            )

        role_details= role.objects.create(
            role_name=role_name,
            role_type =role_type,
            is_deleted=is_deleted
        )
        return HttpResponse(
            json.dumps({"status": "success", "message": "Role details added successfully"}),
            status=200,
            content_type="application/json",
        )

    except Exception as e:
        print(e)
        logger.error(e)
        traceback.print_exc()
        return HttpResponse(
            json.dumps({"status": "failed", "message": "Please contact administrator"}),
            status=500,  
            content_type="application/json",
        ) 
        
@csrf_exempt
@api_view(['POST'])
@login_required
def user_login_status(request):
    try:
        data = request.data
        log_type = data.get('type')
        employee_obj = employee_config.objects.filter(auth_user_id_id = request.user.pk).last()
        if log_type == 'login':
            EventLog.objects.create(
                event_type = 'User logs',
                event = 'Login',
                event_description = f'User Logged in',
                user = f'{employee_obj.first_name} {employee_obj.last_name}',
                metadata = json.dumps({
                    "Employee Name":f"{employee_obj.first_name} {employee_obj.last_name}",
                    "Employee Email":employee_obj.emailaddress,
                    "Location":employee_obj.location.location_name if employee_obj.location else None,
                    "Department":employee_obj.department.department_name}
            ))
        elif log_type == 'logout':
            EventLog.objects.create(
                event_type = 'User logs',
                event = 'Logout',
                event_description = f'User Logged Out',
                user = f'{employee_obj.first_name} {employee_obj.last_name}',
                metadata = json.dumps({
                    "Employee Name":f"{employee_obj.first_name} {employee_obj.last_name}",
                    "Employee Email":employee_obj.emailaddress,
                    "Location":employee_obj.location.location_name if employee_obj.location else None,
                    "Department":employee_obj.department.department_name}
            ))
        return HttpResponse(
            json.dumps({"status": "success", 
                        "message": "Log Added"}),
            status=200,
            content_type="application/json",
        )
    except Exception as e:
        logger.error(e)
        traceback.print_exc()
        return HttpResponse(
            json.dumps({"status": "failed", "message": "Please contact administrator"}),
            status=200,
            content_type="application/json",
        )