from djangoapp.utilities.url_file_import import *
app_name = 'djangoapp'

urlpatterns = [
    # --------------------------- User View -------------------------------------
    path('bm/get_user_profile',get_user_profile,name='bm/get_user_profile'),
    path('bm/get_all_employee',get_all_employee),
    path('bm/add_employee_user',add_employee_user.as_view()),
    path('bm/forgot_password',forgot_password.as_view()),
    path('bm/set_password',set_password.as_view()),
    path('bm/get_designation',get_designation.as_view()),
    path('bm/get_departments',get_departments.as_view()), 
    path('bm/add_designation',add_designation.as_view()),
    path('bm/department_config',department_config.as_view()),
    path('bm/get_user_role',get_user_role.as_view()),
    # --------------------------------Access Managment-----------------------
    path('bm/add_module',InjestModuleData.as_view()),
    path('bm/add_access',UserAccessManagement.as_view()),
    path('bm/get_access_list',GetAccessList.as_view()),
    path('bm/get_employee_access_list',GetEmployeeAcessList.as_view()),
    path('bm/save_dup_access_module',save_dup_access_module,name='bm/save_dup_access_module'),
    path('bm/get_roles',get_roles.as_view()),
    path('bm/get_location_details',get_location_details,name = 'add_location_details'),
    path('bm/add_location_details',add_location_details,name = 'add_location_details'),
    path('bm/update_email_configs',update_email_configs,name='bm/update_email_configs'),
    path('bm/add_role',add_role,name='bm/add_role'),
    path('bm/user_login_status',user_login_status,name='bm/user_login_status'),
    #-------------------------------BM---------------------------------------
    path('bm/add_user_info',add_user_info,name = 'add_user_info'),
    path('bm/get_user_info',get_user_info,name = 'get_user_info'),
    path('bm/update_user_info',update_user_info,name = 'update_user_info'),
    path('bm/add_meal_type',add_meal_type,name = 'add_meal_type'),
    path('bm/get_meal_types',get_meal_types,name = 'get_meal_types'),
    path('bm/add_meal_details',add_meal_details,name = 'add_meal_details'),
    path('bm/get_meal_details',get_meal_details,name = 'get_meal_details'),
    path('bm/add_user_weight',add_user_weight,name = 'add_user_weight'),
    path('bm/get_user_weight',get_user_weight,name = 'get_user_weight'),
    path('bm/add_exercise_details',add_exercise_details,name = 'add_exercise_details'),
    path('bm/get_exercise_details',get_exercise_details,name = 'get_exercise_details'),
    path('bm/add_bmi_details',add_bmi_details,name = 'add_bmi_details'),
    path('bm/get_bmi_details',get_bmi_details,name = 'get_bmi_details'),
    path('bm/add_subject',add_subject,name = 'add_subject'),
    path('bm/get_subject_names',get_subject_names,name = 'get_subject_names'),
    path('bm/add_subject_details',add_subject_details,name = 'add_subject_details'),
    path('bm/get_subject_details',get_subject_details,name = 'get_subject_details'),
    path('bm/add_office_work',add_office_work,name = 'add_office_work'),
    path('bm/get_office_work_details',get_office_work_details,name = 'get_office_work_details'),
    path('bm/add_job_profile',add_job_profile,name = 'add_job_profile'),
    path('bm/get_job_profile_details',get_job_profile_details,name = 'get_job_profile_details'),
]
