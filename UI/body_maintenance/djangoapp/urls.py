from django.urls import path
from .views import *  # Corrected import path
from .view.personal_details_view import *
from .view.meal_details_view import *
from .view.datetime_details_view import *
from .view.exercise_details_view import *
from .view.bmi_details_view import *
from .view.subject_details_view import *
from .view.office_work_details import *
from .view.job_profile import *
from .view.generate_otp import *
from djangoapp.view.add_user_emp_view import *
from djangoapp.view.forgot_password_view import *
from djangoapp.view.email_config_views import update_email_configs
from djangoapp.view.all_configurations_view import *
from djangoapp.view.access_management import *
from djangoapp.view.user_profile import *
from djangoapp.view.email_config_views import *
from djangoapp.view.location_details_view import *

app_name = 'djangoapp'

urlpatterns = [
    # --------------------------- User View -------------------------------------
    path('minda/get_user_profile',get_user_profile,name='minda/get_user_profile'),
    path('minda/get_all_employee',get_all_employee),
    path('minda/add_employee_user',add_employee_user.as_view()),
    path('minda/forgot_password',forgot_password.as_view()),
    path('minda/set_password',set_password.as_view()),
    path('minda/get_designation',get_designation.as_view()),
    path('minda/get_departments',get_departments.as_view()), 
    path('minda/add_designation',add_designation.as_view()),
    path('minda/department_config',department_config.as_view()),
    path('minda/get_user_role',get_user_role.as_view()),
    # --------------------------------Access Managment-----------------------
    path('minda/add_module',InjestModuleData.as_view()),
    path('minda/add_access',UserAccessManagement.as_view()),
    path('minda/get_access_list',GetAccessList.as_view()),
    path('minda/get_employee_access_list',GetEmployeeAcessList.as_view()),
    path('minda/save_dup_access_module',save_dup_access_module,name='minda/save_dup_access_module'),
    path('minda/get_roles',get_roles.as_view()),
    path('minda/get_location_details',get_location_details,name = 'add_location_details'),
    path('minda/add_location_details',add_location_details,name = 'add_location_details'),
    path('minda/update_email_configs',update_email_configs,name='minda/update_email_configs'),
    path('minda/add_role',add_role,name='minda/add_role'),
    path('minda/user_login_status',user_login_status,name='minda/user_login_status'),
    path('person_details', Person_details.as_view(), name='person_details'),
    # path('date_details', Date_details.as_view(), name='date_details'),
    # path('wakeup_sleep_time_details', Wakeup_sleep_time_details.as_view(), name='wakeup_sleep_time_details'),
    path('breakfast_details', Breakfast_details.as_view(), name='breakfast_details'),
    path('lunch_details', Lunch_details.as_view(), name='lunch_details'),
    path('dinner_details', Dinner_details.as_view(), name='dinner_details'),
    # path('calculate_total_calories', Calculate_total_calories.as_view(), name='calculate_total_calories'),
    path('weight_details', Weight_details.as_view(), name='weight_details'),
    path('exercise_details',Exercise_details.as_view(), name='exercise_details'),
    path('bmi_details',BMI_details.as_view(), name='bmi_details'),
    path('subject_name',Subject_name.as_view(), name='subject_name'),
    path('subject_all_details',Subject_all_details.as_view(), name='subject_all_details'),
    path('office_working_details',Office_working_details.as_view(), name='office_working_details'),
    path('job_profile_details',Job_profile_details.as_view(), name='job_profile_details'),
    path('generate_otp',GenerateOTPView.as_view(), name='generate_otp'),
]
