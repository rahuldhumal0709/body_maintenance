from djangoapp.utilities.view_file_import import *
from rest_framework.permissions import IsAuthenticated
            
class department_config(generics.ListCreateAPIView):
    """for adding & deleting department"""

    permission_classes = (IsAuthenticated,)

    def post(self, request):
        try:
            data = request.data
            if "id" in data:
                id = data["id"]
                delete_depart = True
            else:
                delete_depart = False

            if not delete_depart:
                logger.info("adding data")
                department_name = str(data["department_name"]).strip()
                is_exists = depart_config.objects.filter(
                    department_name__iexact=department_name
                ).exists()
                if is_exists:
                    logger.info("data already exists")
                    return HttpResponse(
                        json.dumps(
                            {
                                "status": "failed",
                                "message": "Department already exists",
                            }
                        )
                    )
                if "description" in data:
                    description = data["description"]
                else:
                    description = ""

                data_obj = depart_config(
                    department_name=department_name, description=description
                )
                data_obj.save()
                logger.info("data save successfully")
            else:
                # logger.info("updating data")
                # if issue_depart.objects.filter(department_id_id=int(id)).exists():
                #     logger.info("department already exists in issue dept")
                #     return HttpResponse(
                #         json.dumps(
                #             {
                #                 "status": "failed",
                #                 "message": "Department cannot be deleted as it is associated with an issue type ",
                #             }
                #         )
                #     )

                if employee_config.objects.filter(department_id=int(id)).exists():
                    logger.info("department already exists in employee config")
                    return HttpResponse(
                        json.dumps(
                            {
                                "status": "failed",
                                "message": "Department cannot be deleted as it is associated with an employee ",
                            }
                        )
                    )
                else:
                    data_obj = depart_config.objects.filter(id=id).delete()
                    logger.info("data deleted successfully")
            logger.info("Department updated successfully")
            return HttpResponse(
                json.dumps(
                    {
                        "status": "success",
                        "message": "Department updated successfully",
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
class get_departments(generics.ListCreateAPIView):
    """getting department details"""

    permission_classes = (IsAuthenticated,)

    def get(self, request):
        try:
            data_list = []
            data_obj = depart_config.objects.all()
            logger.info("getting all data")
            for data in data_obj:
                logger.info("appending data")
                data_list.append(
                    {
                        "department_id": data.pk,
                        "department_name": data.department_name,
                        "description": data.description,
                    }
                )
            logger.info("department details retrieved successfully")
            return HttpResponse(
                json.dumps(
                    {
                        "status": "success",
                        "message": "department details retrieved successfully",
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

class get_designation(generics.ListCreateAPIView):
    """getting all designation details"""

    permission_classes = (IsAuthenticated,)

    def get(self, request):
        try:
            data_list = []
            data_obj = desig_config.objects.filter(is_deleted=False)
            logger.info("getting all data successfully")
            for data in data_obj:
                logger.info("appending")
                data_list.append(
                    {"designation_id": data.pk, "designation": data.designation}
                )

            logger.info("designation details retrived Successfully")
            return HttpResponse(
                json.dumps(
                    {
                        "status": "success",
                        "message": "Designation details retrived successfully",
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
            
class get_user_role(generics.ListCreateAPIView):
    """getting requested user role"""

    permission_classes = (IsAuthenticated,)

    def get(self, request):
        try:
            user_id = request.user.pk
            employee_id = employee_config.objects.get(auth_user_id=user_id).pk
            username = User.objects.get(id=user_id).username
            logger.info("")
            manager = "Managers"
            nonmanager = "NonManagers"
            admin = "Admin"
            manager_role_id = role.objects.get(role_name=manager).pk
            nonmanager_role_id = role.objects.get(role_name=nonmanager).pk
            admin_role_id = role.objects.get(role_name=admin).pk
            emp_list_1 = []
            emp_role_obj_1 = employee_role.objects.filter(roles_id=manager_role_id)
            for data in emp_role_obj_1:
                logger.info("appending")
                emp_list_1.append(data.employee.pk)

            emp_list_2 = []
            emp_role_obj_2 = employee_role.objects.filter(roles_id=nonmanager_role_id)
            for data in emp_role_obj_2:
                logger.info("appending")
                emp_list_2.append(data.employee.pk)

            emp_list_3 = []
            emp_role_obj_3 = employee_role.objects.filter(roles_id=admin_role_id)
            for data in emp_role_obj_3:
                logger.info("appending")
                emp_list_3.append(data.employee.pk)

            if employee_id in emp_list_1:
                logger.info("Managers")
                role_name = "Managers"
            elif employee_id in emp_list_3:
                role_name = "Admin"
                logger.info("Admin")
            else:
                role_name = "NonManagers"
                logger.info("NonManagers")

            logger.info("role retrived Successfully")

            if "fcm_token" in request.GET:
                logger.info("get fcm token from request")
                fcm_token = request.GET["fcm_token"]
            else:
                logger.info("fcm token not in request data")
                fcm_token = ""

            user_obj = User.objects.filter(username=username)
            is_exist = user_fcm_token.objects.filter(us=user_obj[0]).exists()
            logger.info("checking user in fcm token model")
            if is_exist:
                user_fcm_token.objects.filter(us=user_obj[0]).update(
                    fcm_token=fcm_token
                )
                logger.info(f"FCM token updated for user {username}")
            else:

                fcm_token_obj = user_fcm_token(us=user_obj[0], fcm_token=fcm_token)
                fcm_token_obj.save()
                logger.info("fcm token saved successfully")
            return HttpResponse(
                json.dumps(
                    {
                        "status": "success",
                        "message": "Role retrived successfully",
                        "Role": role_name,
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

class add_designation(generics.ListCreateAPIView):
    permission_classes = (IsAuthenticated,)

    def post(self, request):
        try:
            data = request.data
            if "id" in data:
                id = data["id"]
                deleted = True
            else:
                deleted = False
            if not deleted:
                logger.info("adding designation")
                designation = str(data["designation"]).strip()
                if desig_config.objects.filter(
                    designation__iexact=designation
                ).exists():
                    logger.info("designation already exists")
                    return HttpResponse(
                        json.dumps(
                            {
                                "status": "failed",
                                "message": "Designation already exists",
                            }
                        )
                    )

                description = ""
                data_obj = desig_config(
                    designation=designation, description=description
                )
                data_obj.save()
            else:
                logger.info("deleting designation")
                desig_id = desig_config.objects.get(pk=id).pk
                if employee_config.objects.filter(designation_id=desig_id).exists():
                    return HttpResponse(
                        json.dumps(
                            {
                                "status": "failed",
                                "message": "Designation cannot be deleted as it is associated with an employee",
                            }
                        )
                    )
                else:
                    desig_config.objects.filter(pk=id).delete()

            return HttpResponse(
                json.dumps(
                    {
                        "status": "success",
                        "message": "Designation Deleted successfully",
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