from djangoapp.utilities.view_file_import import *

class InjestModuleData(generics.ListAPIView):
    permission_classes = (IsAuthenticated,)

    def post(self, request):
        """injest data into access_module names"""

        try:
            module_name = request.data["module_name"]
            obj_access_module = access_module(module_name=module_name)
            obj_access_module.save()
            return HttpResponse(
                json.dumps(
                    {
                        "status": "success",
                        "message": "module added successfully",
                        "module_id": obj_access_module.pk,
                    }
                )
            )
        except:
            traceback.print_exc()

    def get(self, request):
        """get list of modules available for access management"""
        try:
            modules_list = []

            total_modules = access_module.objects.all()
            for module in total_modules:
                modules_list.append(
                    {"module_id": module.pk, "module_name": module.module_name}
                )
            return HttpResponse(
                json.dumps(
                    {
                        "status": "success",
                        "message": "module access data fetched successfully",
                        "data": modules_list,
                    }
                )
            )
        except Exception as msg:
            traceback.print_exc()
            logger.error(msg)
            return HttpResponse(
                json.dumps(
                    {"status": "failed", "message": "Please contact administrator"}
                )
            )


class UserAccessManagement(generics.ListAPIView):
    permission_classes = (IsAuthenticated,)

    def post(self, request):
        try:
            logger.info(request)
            print(request.data)
            data_list = request.data["data"]
            for data in data_list:
                # print(data)

                module_name_id = int(data["module_id"])
                role_id = int(data["role_id"])
                create_access = data["create_access"]
                read_access = data["read_access"]
                update_access = data["update_access"]
                delete_access = data["delete_access"]
                logger.info("checking if access is exists")
                module_exists = access_module_config.objects.filter(
                    module_name_id=module_name_id, role_id=role_id
                ).exists()

                if module_exists:
                    logger.info("updating existing access")
                    obj = access_module_config.objects.filter(
                        module_name_id=module_name_id, role_id=role_id
                    )
                    if bool(create_access) == False and bool(read_access) == False:
                        obj.delete()
                    else:
                        obj.update(
                            role_id=role_id,
                            module_name_id=module_name_id,
                            create_access=bool(create_access),
                            read_access=bool(read_access),
                            update_access=bool(update_access),
                            delete_access=bool(delete_access),
                        )
                else:
                    logger.info("adding new access")
                    obj_access_module_config = access_module_config(
                        role_id=role_id,
                        module_name_id=module_name_id,
                        create_access=bool(create_access),
                        read_access=bool(read_access),
                        update_access=bool(update_access),
                        delete_access=bool(delete_access),
                    )
                    obj_access_module_config.save()
            return HttpResponse(
                json.dumps(
                    {"status": "success", "message": "access added successfully"}
                )
            )
        except Exception as msg:
            traceback.print_exc()
            logger.error(msg)
            return HttpResponse(
                json.dumps(
                    {"status": "failed", "message": "Please contact administrator"}
                )
            )

    # class UserAccessManagement(generics.ListAPIView):
    #     permission_classes=(IsAuthenticated,)
    #     def post(self,request):
    #         try:
    #             logger.info(request)
    #             print(request.data)
    #             data_list = request.data["data"]
    #             for data in data_list:
    #                 # print(data)

    #                 module_name_id = int(data["module_id"])
    #                 role_id = int(data["role_id"])
    #                 create_access = data["create_access"]
    #                 read_access = data["read_access"]
    #                 update_access = data["update_access"]
    #                 delete_access = data["delete_access"]

    #                 # module_name=access_module.objects.get(id=module_name_id).module_name
    #                 if module_name_id==0:
    #                     print("&&&&&&&&&")
    #                     logger.info("if access for ticket")
    #                     sub_ticket_module_list=["Created_by_me","All_Tickets","My_Tickets","Assigned_To_Me","To_be_Approved","To_be_Assigned","My_Department_Tickets"]
    #                     module_id_list=[]
    #                     module_obj=access_module.objects.filter(module_name__in=sub_ticket_module_list)
    #                     logger.info("iterating module_obj over j")
    #                     for j in module_obj:
    #                         module_id_list.append(j.pk)
    #                     for data in module_id_list:
    #                         module_name_id=data
    #                         module_exists = access_module_config.objects.filter(module_name_id=module_name_id,role_id=role_id).exists()
    #                         if module_exists:
    #                             print("********")
    #                             logger.info("updating existing access")
    #                             obj = access_module_config.objects.filter(module_name_id=module_name_id,role_id=role_id)
    #                             if bool(create_access) == False and bool(read_access) == False:
    #                                 obj.delete()
    #                             else:
    #                                 obj.update(
    #                                     role_id = role_id,
    #                                     module_name_id = module_name_id,
    #                                     create_access= bool(create_access),
    #                                     read_access = bool(read_access),
    #                                     update_access = bool(update_access),
    #                                     delete_access = bool(delete_access)
    #                                     )
    #                         else:
    #                             logger.info("adding new access")
    #                             obj_access_module_config = access_module_config(
    #                             role_id = role_id,
    #                             module_name_id = module_name_id,
    #                             create_access= bool(create_access),
    #                             read_access = bool(read_access),
    #                             update_access = bool(update_access),
    #                             delete_access = bool(delete_access)
    #                             )
    #                             obj_access_module_config.save()

    #                 logger.info("checking if access is exists")
    #                 module_exists = access_module_config.objects.filter(module_name_id=module_name_id,role_id=role_id).exists()

    #                 if module_exists:
    #                     print("$$$$$$$$")
    #                     logger.info("updating existing access")
    #                     obj = access_module_config.objects.filter(module_name_id=module_name_id,role_id=role_id)
    #                     if bool(create_access) == False and bool(read_access) == False:
    #                         obj.delete()
    #                     else:
    #                         obj.update(
    #                             role_id = role_id,
    #                             module_name_id = module_name_id,
    #                             create_access= bool(create_access),
    #                             read_access = bool(read_access),
    #                             update_access = bool(update_access),
    #                             delete_access = bool(delete_access)
    #                             )
    #                 else:
    #                     logger.info("adding new access")
    #                     obj_access_module_config = access_module_config(
    #                     role_id = role_id,
    #                     module_name_id = module_name_id,
    #                     create_access= bool(create_access),
    #                     read_access = bool(read_access),
    #                     update_access = bool(update_access),
    #                     delete_access = bool(delete_access)
    #                     )
    #                     obj_access_module_config.save()
    #             return HttpResponse(json.dumps({
    #                 "status":"success",
    #                 "message":"access added successfully"
    #             }))
    #         except Exception as msg:
    #             traceback.print_exc()
    #             logger.error(msg)
    #             return HttpResponse(json.dumps({
    #                 "status":"failed",
    #                 "message":"Please contact administrator"
    #             }))

    def get(self, request):
        """get list of access modules along with role"""
        try:
            access_data = []
            if "role_id" in request.GET:
                role_id = request.GET["role_id"]
                data = role.objects.filter(id=role_id)
            else:
                data = role.objects.all()
            data_access = access_module.objects.all()
            for i in data:
                # print(i.module_name)

                accessed_designations = []
                for j in data_access:
                    access_data_list = access_module_config.objects.filter(
                        role_id=i.pk, module_name_id=j.pk
                    )

                    if len(access_data_list) >= 1:
                        accessed_designations.append(
                            {
                                "module_id": access_data_list[0].module_name.pk,
                                "module_name": access_data_list[
                                    0
                                ].module_name.module_name,
                                "create_access": access_data_list[0].create_access,
                                "read_access": access_data_list[0].read_access,
                                "update_access": access_data_list[0].update_access,
                                "delete_access": access_data_list[0].delete_access,
                            }
                        )
                        # print(access_data_list[0].create_access,"@@")
                    else:
                        accessed_designations.append(
                            {
                                "module_name": j.module_name,
                                "module_id": j.pk,
                                "create_access": False,
                                "read_access": False,
                                "update_access": False,
                                "delete_access": False,
                            }
                        )

                access_data.append({i.pk: accessed_designations})
                # access_data.append({i.module_name:accessed_designations})
            return HttpResponse(
                json.dumps(
                    {
                        "status": "success",
                        "message": "access data fetched successfuly",
                        "data": access_data,
                    }
                )
            )
        except Exception as msg:
            traceback.print_exc()
            logger.error(msg)
            return HttpResponse(
                json.dumps(
                    {"status": "failed", "message": "Please contact administrator"}
                )
            )


class GetAccessList(generics.ListCreateAPIView):
    permission_classes = (IsAuthenticated,)

    def get(self, request):
        """get user's access list by employee_id"""
        try:
            access_data_list = []
            # print(request.user.pk)
            role_id = int(request.GET["role_id"])
            role_name = role.objects.filter(id=role_id)
            role_name = role_name[0].role_name
            # employee_id = employee_config.objects.get(id=int(employee_id))
            # print(employee_id.pk)
            modules = access_module.objects.all()
            for i in modules:
                access_name = access_module_config.objects.filter(
                    role_id=int(role_id), module_name_id=i.pk
                )
                # print(type(access_name))
                if len(access_name) >= 1:
                    access_data_list.append(
                        {
                            "module_name": i.module_name,
                            "module_id": i.pk,
                            "role_id": role_id,
                            "is_enabled": True,
                            "create_access": access_name[0].create_access,
                            "read_access": access_name[0].read_access,
                            "update_access": access_name[0].update_access,
                            "delete_access": access_name[0].delete_access,
                        }
                    )
                else:
                    access_data_list.append(
                        {
                            "module_name": i.module_name,
                            "module_id": i.pk,
                            "role_id": role_id,
                            "is_enabled": False,
                            "create_access": False,
                            "read_access": False,
                            "update_access": False,
                            "delete_access": False,
                        }
                    )
            print(access_data_list)
            return HttpResponse(
                json.dumps(
                    {
                        "status": "success",
                        "message": "data retrieved successfully",
                        "role": role_name,
                        "data": access_data_list,
                    }
                )
            )

        except Exception as msg:
            traceback.print_exc()
            logger.error(msg)
            return HttpResponse(
                json.dumps(
                    {"status": "failed", "message": "Please contact administrator"}
                )
            )


class GetEmployeeAcessList(generics.ListAPIView):
    permission_classes = (IsAuthenticated,)

    def get(self, request):
        """get user's access list by employee_id"""
        try:
            access_data_list = []
            # print(request.user.pk)
            # employee_id = request.GET["employee_id"]
            user_id = request.user.pk
            employee_id = employee_config.objects.get(auth_user_id=user_id).pk
            print("employee_id", employee_id)
            role_id = employee_role.objects.filter(
                employee_id=employee_id, is_deleted=False
            )
            # print("role_id",role_id.count())
            role_list = []
            for i in role_id:
                role_list.append(i.roles.pk)

            # for j in role_id:
            # print("*******",role_list)
            create_access = False
            read_access = False
            update_access = False
            delete_access = False
            modules = access_module.objects.all()
            for i in modules:
                access_name = access_module_config.objects.filter(
                    role_id__in=role_list, module_name_id=i.pk
                )
                create_access = False
                read_access = False
                update_access = False
                delete_access = False
                count = 0
                count1 = 0
                count2 = 0
                count3 = 0
                for j in access_name:
                    if j.create_access == True:
                        count += 1
                    if j.read_access == True:
                        # print("(((((", j.read_access)
                        count1 += 1
                    if j.update_access == True:
                        count2 += 1
                    if j.delete_access == True:
                        count3 += 1
                if count > 0:
                    create_access = True
                if count1 > 0:
                    read_access = True
                if count2 > 0:
                    update_access = True
                if count3 > 0:
                    delete_access = True
                # print("count",count)
                # print("count1",count1)
                # print("count2",count2)
                # print("count3",count3)
                if access_name.count() == 0:
                    continue

                # print("access_name",access_name)
                if len(access_name) >= 1:
                    access_data_list.append(
                        {
                            "module_name": i.module_name,
                            "module_id": i.pk,
                            "is_enabled": True,
                            "create_access": create_access,
                            "read_access": read_access,
                            "update_access": update_access,
                            "delete_access": delete_access,
                        }
                    )

                else:
                    pass
                # print("access_data_list",access_data_list)
                if len(access_data_list) == 0:
                    return HttpResponse(
                        json.dumps(
                            {"status": "success", "message": "No Access Given Yet"}
                        )
                    )
            # distinct_dicts = []
            # for d in access_data_list:
            #     if d not in distinct_dicts:
            #         distinct_dicts.append(d)
            #     access_data_list=distinct_dicts

            # print("access_data_list",access_data_list)

            return HttpResponse(
                json.dumps(
                    {
                        "status": "success",
                        "message": "data retrieved successfully",
                        # "role": role_id.role_name,
                        "data": access_data_list,
                    }
                )
            )

        except Exception as msg:
            traceback.print_exc()
            logger.error(msg)
            return HttpResponse(
                json.dumps(
                    {"status": "failed", "message": "Please contact administrator"}
                )
            )


@csrf_exempt
@api_view(["GET"])
def get_specific_access_module(request):
    """getting access list for some specific module"""
    try:
        response = Auth.anonymous(request)
        if response == "authorized":
            pass
        else:
            return response
        data_list = []
        specific_module_list = [
            "Dashboard",
            "Ticket_work_flow",
            "User_Configuration",
            "Access_Control",
        ]
        logger.info(f"add specific module name: {specific_module_list}")
        data_obj = access_module.objects.filter(module_name__in=specific_module_list)
        logger.info("filtering data_obj over i")
        for i in data_obj:
            data_list.append(
                {
                    "module_id": i.pk,
                    "module_name": i.module_name,
                }
            )
        logger.info("Module retrieved successfully")
        return HttpResponse(
            json.dumps(
                {
                    "status": "success",
                    "message": "Module retrieved successfully",
                    # "role": role_id.role_name,
                    "data": data_list,
                    "module_id": 0,
                    "module_name": "Tickets",
                }
            )
        )

    except Exception as msg:
        traceback.print_exc()
        logger.error(msg)
        return HttpResponse(
            json.dumps({"status": "failed", "message": "Please contact administrator"})
        )


@csrf_exempt
@api_view(["POST"])
def save_dup_access_module(request):  # NEW
    try:
        data = request.data
        role_id = role.objects.get(id=data["role_id"])
        access_obj = duplicate_access_module_config.objects.filter(role_id=role_id.pk)
        for data in access_obj:
            module_name = data.module_name_id
            create_acc = data.create_access
            read_acc = data.read_access
            update_acc = data.update_access
            delete_acc = data.delete_access

            module_name_id = access_module.objects.get(module_name=module_name)

            acc_con_obj = access_module_config(
                module_name_id=module_name_id.pk,
                role_id=role_id.pk,
                create_access=create_acc,
                read_access=read_acc,
                update_access=update_acc,
                delete_access=delete_acc,
            )
            acc_con_obj.save()

        logger.info("Access module saved")
        return HttpResponse(
            json.dumps(
                {
                    "status": "success",
                    "message": "Access module saved successfully",
                }
            )
        )

    except Exception as msg:
        traceback.print_exc()
        logger.error(msg)
        return HttpResponse(
            json.dumps({"status": "failed", "message": "Please contact administrator"})
        )
