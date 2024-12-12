# user_auth.py

import json
from rest_framework import status
from django.http import HttpResponse,JsonResponse
from djangoapp.models import employee_config,apiresource_config,apiresource_grouppermission_config,dashboard_menu_grouppermission_config,dashboard_menu_config
from django.contrib.auth.models import User
import traceback

class Auth:
    """ check authorized user"""
    def anonymous(request):
        """ check authorized user"""
        # if superuser
        if request.user.is_superuser:
            #print("superuser")
            is_authorized = 'authorized'
            return is_authorized
        
        # if not authorized user
        elif request.user.is_anonymous:
            #print('not authorized')
            return HttpResponse(json.dumps({"Authorization": "Not authorized"}), status=status.HTTP_401_UNAUTHORIZED)
        # if authorized user
        else:
            is_authorized = 'authorized'
            #print('authorized')
            return is_authorized


    ###############################################
        # try:
        #     if request.user.is_superuser:
        #         print("$$$$superuser")
        #         is_authorized = 'authorized'
        #         return is_authorized
            
        #     if request.user.is_anonymous:
        #         print('@@@@@@@@@@@',request.user)
        #         return HttpResponse(json.dumps({"Authorization": "Not authorized"}), status=status.HTTP_401_UNAUTHORIZED)

        #     auth_user_id = request.user.id
        #     # print('######### auth_user_id',auth_user_id)

        #     employee = employee_config.objects.select_related().get(id=auth_user_id)
        #     # print("employee",employee)
        #     designation=employee.designation
        #     # print("designation",designation)

        #     url_path= request.path
        #     # print('######### url_path',url_path)
        #     url = url_path.split("/")[-1]
        #     # print('url',url)

        #     api_resource = apiresource_config.objects.select_related().get(api_url=url)
        #     # api=api_resource.api_url
        #     api_id=api_resource.id
        #     # print('api',api,"api_id",api_id)

        #     permission = apiresource_grouppermission_config.objects.select_related().get(api_url=api_id)
        #     # print('permission',permission)
        #     desig = permission.designation
        #     # print('permissionDesignation',desig)

            
        #     if designation==desig:
        #         print("authorized")
        #         is_authorized = 'authorized'
        #         return is_authorized
                
        #     else:
        #         print("not authorized")
        #         is_authorized = False
        #         return HttpResponse(json.dumps({"Authorization": "Not authorized"}), status=status.HTTP_401_UNAUTHORIZED)
        # except:
        #    traceback.print_exc()
        #     return HttpResponse(
        #         json.dumps({"status":"failed","message": "There is backend issue, please contact administrator"}),
        #         status=200,
        #         content_type="application/json",
        #     )
        
            
    ###########################################

    def menu_permission(request):
        """returns accessible menu list to user """
        try:
            if request.user.is_superuser:
                menu_list=[]
                menu_list.append('access to all menu')
                return menu_list 
            else:
                # get user id
                auth_user_id = request.user.id
                # employee details
                employee = employee_config.objects.select_related().get(id=auth_user_id)
                # designation data
                designation=employee.designation
                # menu_permission data
                menu_permission_object = dashboard_menu_grouppermission_config.objects.filter(designation=designation)
                # print(menu_permission_object, len(menu_permission_object))
                menu_list=[]
                for i in range (len(menu_permission_object)):
                    menuobj = menu_permission_object[i]
                    menu_list.append(str(menuobj.menu_grouppermission))
                    
                return menu_list  
          
        except:
            traceback.print_exc()
            return HttpResponse(
                json.dumps({"status":"failed","message": "There is backend issue, please contact administrator"}),
                status=200,
                content_type="application/json",
            )
        