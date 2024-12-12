import logging
logger = logging.getLogger(__name__)
logger = logging.getLogger('django')
import re
# import phonenumbers
from datetime import datetime


def validate_id(id):
    """validation of integer"""
    if id.isdigit():
        return True
    else:
        return False
    
def validate_name(name):
    '''validating name'''
    pattern = r'^[A-Za-z\s]+$'
    
    if re.match(pattern,name):
        return True
    else:
        return False
    
# #pending 
# def validate_contact(contact):
#     if contact.isdigit() and len(contact)==10:
#         return True
#     else:
#        return False
        


def validate_amount(amount):
    '''Validating amount field'''
    if amount>=0:
        return True
    else:
        return False
    
   
def validate_string_only(comment):
    '''Validating string field'''
    if comment.isdigit():
        return False
    else:
        return True
    
def validate_date(date):
    '''Validating date field'''
    pattern= r"\d{4}-\d{2}-\d{2}"
    if re.findall(pattern,date):
        return True
    else:
        return False

   
def validate_email(email):
    '''validating email field'''
    pattern = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
    
    if re.match(pattern,email):
        return True
    else:
        return False
    
# def validate_contact(contact):
#     '''Validating contact field'''
#     phone_number = phonenumbers.parse(contact,"IN")
    
#     if phonenumbers.is_valid_number(phone_number):
#         return True
#     else:
#         return False

def validate_contact(contact):
    '''Validating contact field'''
    # Check if the contact number is exactly 10 digits long
    if re.fullmatch(r'\d{10}', contact):
        return True
    else:
        return False

def validate_bool_value(value):
    '''Validating Boolean values'''
    if value =='true' or value =='false' or value=='False' or value=='True':
        return True
    else:
        return False

    
def validate_IFSC_code(ifsc):
    '''Validating IFSC Code for Banks in India'''
    pattern = re.compile(r'^[A-Z]{4}0[A-Z0-9]{6}$')
    
    if re.match(pattern, ifsc):
        return True
    else:
        return False
    
def validate_account_num(number):
    '''Validating Account Number for Banks in India'''
    if len(str(number)) >=8 and len(str(number))<=18:
        if str(number).isdigit():
            return True
        else:
            return False
    else:
            return False
        
def validate_upi_id(upi_id):
    '''Validating UPI id for Banks in India'''
    upi_pattern = r"^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+$" #valid: username.user@upi
    
    if re.match(upi_pattern, upi_id):
        return True
    else:
        return False
# --------------------------PM-----------------------------------------

def validate_value(value):
    if str(value).isdigit() or float(value)>=0 or float(value)<=0:
        return True
    else:
        return False
    

def operational_status_check(status):
    if status=='active' or status=='Active' or status == 'inactive' or status=='Inactive' or status=='maintenance' or status=='Under Maintenance':
        return True
    
    else:
        return False
    

def lifecycle_stage_check(stage):
    if stage=='new' or stage=='New' or stage=='used' or stage=='Used' or stage =='refurbished' or stage == 'Refurbished':
        return True
    
    else:
        return False
    
def boolen_check(value):
    if value == 'true':
        value=True
        return value
    else:
        value=False
        return value
    
# -----------------------------------------------------------------------------