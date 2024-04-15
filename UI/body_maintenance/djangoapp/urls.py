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


app_name = 'djangoapp'

urlpatterns = [
    path('person_details', Person_details.as_view(), name='person_details'),
    path('date_details', Date_details.as_view(), name='date_details'),
    path('wakeup_sleep_time_details', Wakeup_sleep_time_details.as_view(), name='wakeup_sleep_time_details'),
    path('breakfast_details', Breakfast_details.as_view(), name='breakfast_details'),
    path('lunch_details', Lunch_details.as_view(), name='lunch_details'),
    path('dinner_details', Dinner_details.as_view(), name='dinner_details'),
    path('calculate_total_calories', Calculate_total_calories.as_view(), name='calculate_total_calories'),
    path('weight_details', Weight_details.as_view(), name='weight_details'),
    path('exercise_details',Exercise_details.as_view(), name='exercise_details'),
    path('bmi_details',BMI_details.as_view(), name='bmi_details'),
    path('subject_name',Subject_name.as_view(), name='subject_name'),
    path('subject_all_details',Subject_all_details.as_view(), name='subject_all_details'),
    path('office_working_details',Office_working_details.as_view(), name='office_working_details'),
    path('job_profile_details',Job_profile_details.as_view(), name='job_profile_details'),
]
