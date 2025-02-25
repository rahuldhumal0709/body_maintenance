from django.db import models
from django.contrib.auth.models import User
import datetime
from django.contrib.auth.hashers import make_password, check_password

# Create your models here.
# --------------------------------User Configs---------------------------------------------------
def get_current_dt():
    return datetime.datetime.now()

def get_current_date():
    return datetime.datetime.now().date()

class role(models.Model):
    role_name=models.CharField(max_length=100)
    role_type=models.IntegerField()
    is_deleted=models.BooleanField(default=False)
    

class role_group(models.Model):
    group_name=models.CharField(max_length=200)
    description=models.CharField(max_length=200,default='')
    

class access_module(models.Model):
    module_name = models.CharField(max_length=100)
    
    
class access_module_config(models.Model):
    module_name = models.ForeignKey(access_module,on_delete=models.CASCADE)
    role = models.ForeignKey(role,on_delete=models.CASCADE)
    create_access = models.BooleanField(default=False)
    read_access = models.BooleanField(default=False)
    update_access = models.BooleanField(default=False)
    delete_access = models.BooleanField(default=False)

class api_list(models.Model):
    api_endpoint = models.CharField(max_length=300,null=True,blank=True)
    api_type = models.CharField(max_length=250,null=True, blank=True)
    module_name = models.ForeignKey(access_module,on_delete=models.CASCADE)
    create_access = models.BooleanField(default=False)
    read_access = models.BooleanField(default=False)
    update_access = models.BooleanField(default=False)
    delete_access = models.BooleanField(default=False)
# class base_access_module(models.Model):
#     module_name=models.CharField(max_length=100)
#     role_id=models.ForeignKey(role,on_delete=models.CASCADE)

class otp_records(models.Model):
    contact = models.BigIntegerField(null=True,default=0)
    otp = models.BigIntegerField(null=False)
    generated_at = models.DateTimeField(null=True)
    email=models.CharField(max_length=100)

class forgot_password_log(models.Model):
    first_name=models.CharField(max_length=100,null=True)
    last_name=models.CharField(max_length=100,null=True)
    email=models.CharField(max_length=100,null=True)
    otp=models.CharField(max_length=100,null=True)
    created_on=models.DateTimeField(default = get_current_dt)

class duplicate_access_module_config(models.Model):#NEW
    module_name_id = models.CharField(max_length=100)
    role_id = models.ForeignKey(role,on_delete=models.CASCADE)
    create_access = models.BooleanField(default=False)
    read_access = models.BooleanField(default=False)
    update_access = models.BooleanField(default=False)
    delete_access = models.BooleanField(default=False)

class module_config(models.Model):
	module_name = models.CharField(max_length=50, default="")

	def __str__(self) -> str:
		return self.module_name

class customer_details_config(models.Model):
	client_name=  models.CharField(max_length=70, default="")
	phone = models.BigIntegerField(default=False)
	emailaddress = models.CharField(max_length=70, default="")
	database_access = models.CharField(max_length=70, default="")
	module_access = models.ForeignKey(module_config,on_delete=models.DO_NOTHING)

	def __str__(self) -> str:
		return self.id

class depart_config(models.Model):
	department_name = models.CharField(max_length=70, default="")
	description = models.CharField(max_length=70, default="")
	is_viewable = models.BooleanField(default=True)
	def __str__(self):
		return self.department_name

class desig_config(models.Model):
    designation = models.CharField(max_length=70, default="")
    description = models.CharField(max_length=70, default="")
    is_deleted = models.BooleanField(default=False)
    
    def __str__(self):
        return self.designation

class trac_location_details(models.Model):
    location_name = models.CharField(max_length=200)

class employee_config(models.Model):
    unique_id = models.CharField(max_length = 15)
    auth_user_id = models.ForeignKey(User, on_delete=models.DO_NOTHING,null = True)
    first_name = models.CharField(max_length=70, default="")
    location=models.ForeignKey(trac_location_details,on_delete=models.SET_NULL,null = True)
    last_name = models.CharField(max_length=70, null=True)
    dateof_joining = models.DateField(default = get_current_date)
    phone = models.BigIntegerField(null=True)
    emailaddress = models.CharField(max_length=70, default="")
    department =  models.ForeignKey(depart_config, on_delete=models.DO_NOTHING)
    designation = models.ForeignKey(desig_config, on_delete=models.DO_NOTHING)
    is_deleted = models.BooleanField(default=False)
    created_on = models.DateTimeField(default = get_current_dt)
    action = models.CharField(max_length = 100,default = "Insert")
    is_active = models.BooleanField(default= True)
    
    def __str__(self):
        return f'{self.first_name} {self.last_name}'
    
class role_group_config(models.Model):
    group=models.ForeignKey(role_group,on_delete=models.CASCADE)
    role=models.ForeignKey(role,on_delete=models.CASCADE,null=True,default=None)
    department=models.ForeignKey(depart_config,on_delete=models.CASCADE)
    description=models.CharField(max_length=200,default='')

class employee_role(models.Model):
    roles=models.ForeignKey(role,on_delete=models.CASCADE)
    employee=models.ForeignKey(employee_config,on_delete=models.CASCADE,null=True)
    is_deleted=models.BooleanField(default=False)

class user_fcm_token(models.Model):
    us=models.ForeignKey(User,on_delete=models.DO_NOTHING)
    fcm_token=models.CharField(max_length=1000)
    
    
class apiresource_config(models.Model):
    api_url= models.CharField(max_length=60)
    
    def __str__(self) -> str:
        return self.api_url
    
class apiresource_grouppermission_config(models.Model):
    designation = models.ForeignKey(desig_config, on_delete=models.DO_NOTHING)
    api_url = models.ForeignKey(apiresource_config, on_delete=models.DO_NOTHING)
    
class dashboard_menu_config(models.Model):
    menu = models.CharField(max_length=60)
    
    def __str__(self) -> str:
        return self.menu
    
class dashboard_menu_grouppermission_config(models.Model):
    designation = models.ForeignKey(desig_config, on_delete=models.DO_NOTHING)
    menu_grouppermission = models.ForeignKey(dashboard_menu_config, on_delete=models.DO_NOTHING)

#--------------------------------------------bm---------------------------------------------
class trac_rework_access(models.Model):
    password = models.CharField(max_length=256)

class module_access(models.Model):
    user = models.ForeignKey(User,on_delete = models.DO_NOTHING) 
    module_access = models.ForeignKey(module_config,on_delete = models.DO_NOTHING)
    
class EmailConfiguration(models.Model):
    smtp_host = models.CharField(max_length=255, default="smtp-mail.outlook.com")
    smtp_port = models.PositiveIntegerField(default=587)
    smtp_user = models.EmailField()
    smtp_password = models.CharField(max_length=255)
    use_tls = models.BooleanField(default=True)
    use_ssl = models.BooleanField(default=False)
    updated_at = models.DateTimeField(auto_now=True)

class bm_person_info(models.Model):
    MALE = 'M'
    FEMALE = 'F'
    OTHER = 'O'

    GENDER_CHOICES = [
        (MALE, 'Male'),
        (FEMALE, 'Female'),
        (OTHER, 'Other'),
    ]
    user = models.ForeignKey(User,on_delete=models.CASCADE)
    first_name = models.CharField(max_length=100)
    last_name = models.CharField(max_length=100)
    dob = models.DateField()
    gender = models.CharField(max_length=1, choices=GENDER_CHOICES)
    height = models.FloatField(help_text="Height in cm")
    education = models.CharField(max_length=100)
    permanent_address = models.CharField(max_length=255)
    current_address = models.CharField(max_length=255)
    marital_status = models.BooleanField()

class bm_meal_type(models.Model):
    name = models.CharField(max_length=50)

class bm_meal(models.Model):
    user = models.ForeignKey(User,on_delete=models.CASCADE)
    date = models.DateField(default=get_current_date)
    meal_type = models.ForeignKey(bm_meal_type,on_delete=models.CASCADE)
    meal = models.CharField(max_length=100)
    description = models.TextField()

class bm_weight(models.Model):
    user = models.ForeignKey(User,on_delete=models.CASCADE)
    date = models.DateField(default=get_current_date)
    weight = models.FloatField(help_text="Weight in kg",default=0)

class bm_exercise(models.Model):
    user = models.ForeignKey(User,on_delete=models.CASCADE)
    date = models.DateField(default=get_current_date)
    start_time = models.TimeField()
    end_time = models.TimeField()
    sets_of_parts = models.JSONField()
    efforts = models.DecimalField(max_digits=5, decimal_places=2)

class bm_bmi(models.Model):
    user = models.ForeignKey(User,on_delete=models.CASCADE)
    date = models.DateField(default=get_current_date)
    height = models.FloatField(help_text="Height in cm")
    weight = models.FloatField(help_text="Weight in kg")
    bmi = models.FloatField(help_text="BMI in kg/m2")
    result = models.CharField(max_length=100)

class bm_office(models.Model):
    user = models.ForeignKey(User,on_delete=models.CASCADE)
    date = models.DateField(default=get_current_date)
    start_time = models.TimeField()
    end_time = models.TimeField()
    work = models.CharField(max_length=100)
    description = models.TextField()
    efforts = models.DecimalField(max_digits=5, decimal_places=2)

class bm_subject_names(models.Model):
    subject_name = models.CharField(max_length=100)

class bm_subject_details(models.Model):
    user = models.ForeignKey(User,on_delete=models.CASCADE)
    date = models.DateField(default=get_current_date)
    start_time = models.TimeField()
    end_time = models.TimeField()
    subject_name = models.ForeignKey(bm_subject_names,on_delete=models.CASCADE)
    topic = models.CharField(max_length=100)
    description = models.TextField()
    efforts = models.DecimalField(max_digits=5, decimal_places=2)
    is_any_que_solved = models.BooleanField(default=False)
    how_many_que = models.IntegerField()

class bm_job_profile(models.Model):
    user = models.ForeignKey(User,on_delete=models.CASCADE)
    date = models.DateField(default=get_current_date)
    company_name = models.CharField(max_length=100)
    is_referral = models.BooleanField(default=False)
    referral_person_name = models.CharField(null=True,max_length=100)
    platform_name = models.CharField(null=True,max_length=100)
    for_which_role = models.CharField(null=True,max_length=100)
    resume = models.FileField(upload_to='resume',default='')

#--------------------------------------Logging------------------------------------------
class EventLog(models.Model):
    EVENT_TYPES = [
        ('Interlocking', 'Interlocking'),
        ('Batch logs', 'Batch logs'),
        ('User logs', 'User Logs'),
        ('Configurations','Configurations')
    ]
    EVENT = [
        ('Insert' , 'Insert'),
        ('Update' , 'Update'),
        ('Delete' , 'Delete'),
        ('Lock' , 'Lock'),
        ('Unlock' , 'Unlock'),
        ('Login', 'Login'),
        ('Logout' , 'Logout'),
        ('Failed', 'Failed'),
    ]
    event_type = models.CharField(max_length=50, choices=EVENT_TYPES, verbose_name="Event Type")
    event = models.CharField(max_length=10,choices=EVENT,verbose_name='Events')
    event_description = models.TextField(verbose_name="Event Description")
    user = models.CharField(
        max_length=200,
        null=True, 
        blank=True, 
        verbose_name="User"
    )
    device_unique_id = models.CharField(
        max_length=200, 
        null=True, 
        blank=True, 
        verbose_name="Device"
    )
    batch_unique_id = models.CharField(
        max_length=200, 
        null=True, 
        blank=True, 
        verbose_name="Inventory"
    )
    timestamp = models.DateTimeField(default=get_current_dt, verbose_name="Timestamp")
    metadata = models.JSONField(null=True, blank=True, verbose_name="Metadata")

    def __str__(self):
        return f"{self.event_type} - {self.timestamp}"

    class Meta:
        db_table = 'djangoapp_event_logs'
        verbose_name = "Event Log"
        verbose_name_plural = "Event Logs"
        ordering = ['-timestamp']
        
class AccessPasswordManager(models.Manager):
    def create(self, **kwargs):
        if 'password' in kwargs:
            kwargs['password'] = make_password(kwargs['password'])
        return super().create(**kwargs)

    def update(self, **kwargs):
        if 'password' in kwargs:
            kwargs['password'] = make_password(kwargs['password'])
        return super().update(**kwargs)

class EmailAccessPassword(models.Model):
    password = models.CharField(max_length=300)

    objects = AccessPasswordManager()

    def check_password(self, raw_password):
        """Check a raw password against the hashed password."""
        return check_password(raw_password, self.password)

class InterlockAccessPassword(models.Model):
    password = models.CharField(max_length=300)

    objects = AccessPasswordManager()

    def check_password(self, raw_password):
        """Check a raw password against the hashed password."""
        return check_password(raw_password, self.password)