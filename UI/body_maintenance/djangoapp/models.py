from django.db import models

# Create your models here.
class bm_person_info(models.Model):
    MALE = 'M'
    FEMALE = 'F'
    OTHER = 'O'

    GENDER_CHOICES = [
        (MALE, 'Male'),
        (FEMALE, 'Female'),
        (OTHER, 'Other'),
    ]
    person_name = models.CharField(max_length=100)
    dob = models.DateField()
    gender = models.CharField(max_length=1, choices=GENDER_CHOICES)
    height = models.FloatField(help_text="Height in cm")
    education = models.CharField(max_length=100)
    permanent_address = models.CharField(max_length=255)
    current_address = models.CharField(max_length=255)
    marital_status = models.BooleanField()

# class bm_date(models.Model):
#     date = models.DateField()

class bm_daily_wakeup_sleep_time(models.Model):
    person_name = models.ForeignKey(bm_person_info,on_delete=models.CASCADE)
    date = models.DateField(null=True)
    wakeup_time = models.TimeField()
    sleep_time = models.TimeField(null=True)

class bm_breakfast(models.Model):
    person_name = models.ForeignKey(bm_person_info,on_delete=models.CASCADE)
    date = models.DateField(null=True)
    breakfast_meal = models.CharField(max_length=100)
    quantity = models.CharField(max_length=100)
    dish_calories = models.IntegerField()

class bm_lunch(models.Model):
    person_name = models.ForeignKey(bm_person_info,on_delete=models.CASCADE)
    date = models.DateField(null=True)
    lunch_menu = models.CharField(max_length=100)
    quantity = models.CharField(max_length=100)
    dish_calories = models.IntegerField()

class bm_dinner(models.Model):
    person_name = models.ForeignKey(bm_person_info,on_delete=models.CASCADE)
    date = models.DateField(null=True)
    dinner_menu = models.CharField(max_length=100)
    quantity = models.CharField(max_length=100)
    dish_calories = models.IntegerField()

class bm_total_calories(models.Model):
    person_name = models.ForeignKey(bm_person_info,on_delete=models.CASCADE)
    date = models.DateField(null=True)
    total_calories = models.IntegerField()

class bm_weight(models.Model):
    person_name = models.ForeignKey(bm_person_info,on_delete=models.CASCADE)
    date = models.DateField(null=True)
    weight = models.FloatField(help_text="Weight in kg",default=0)

class bm_exercise(models.Model):
    person_name = models.ForeignKey(bm_person_info,on_delete=models.CASCADE)
    date = models.DateField(null=True)
    start_time = models.TimeField()
    end_time = models.TimeField()
    sets_of_parts = models.JSONField()
    efforts = models.DecimalField(max_digits=5, decimal_places=2)

class bm_bmi(models.Model):
    person_name = models.ForeignKey(bm_person_info,on_delete=models.CASCADE)
    date = models.DateField(null=True)
    height = models.FloatField(help_text="Height in cm")
    weight = models.FloatField(help_text="Weight in kg")
    bmi = models.FloatField(help_text="BMI in kg/m2")
    result = models.CharField(max_length=100)

class bm_office(models.Model):
    person_name = models.ForeignKey(bm_person_info,on_delete=models.CASCADE)
    date = models.DateField(null=True)
    start_time = models.TimeField()
    end_time = models.TimeField()
    work = models.CharField(max_length=100)
    description = models.TextField()
    efforts = models.DecimalField(max_digits=5, decimal_places=2)

class bm_subject_names(models.Model):
    subject_name = models.CharField(max_length=100)

class bm_subject_details(models.Model):
    person_name = models.ForeignKey(bm_person_info,on_delete=models.CASCADE)
    date = models.DateField(null=True)
    start_time = models.TimeField()
    end_time = models.TimeField()
    subject_name = models.ForeignKey(bm_subject_names,on_delete=models.CASCADE)
    topic = models.CharField(max_length=100)
    description = models.TextField()
    efforts = models.DecimalField(max_digits=5, decimal_places=2)
    is_any_que_solved = models.BooleanField(default=False)
    how_many_que = models.IntegerField()

class bm_job_profile(models.Model):
    person_name = models.ForeignKey(bm_person_info,on_delete=models.CASCADE)
    date = models.DateField(null=True)
    company_name = models.CharField(max_length=100)
    is_referral = models.BooleanField(default=False)
    referral_person_name = models.CharField(null=True,max_length=100)
    platform_name = models.CharField(null=True,max_length=100)
    for_which_role = models.CharField(null=True,max_length=100)
    resume = models.FileField(upload_to='resume',default='')

# class banking(models.Model):
#     person_name = models.ForeignKey(bm_person_info,on_delete=models.CASCADE)
#     to = models.CharField(max_length=100)
#     actual_amount = models.IntegerField()
#     credited_date = models.DateField()
#     is_emi = models.BooleanField()
#     total_emi = models.IntegerField()
#     emi_amount =  models.IntegerField()
#     due_date = models.DateField()