from djangoapp.models import *

def email_authenticate_access(password):
    access_pass = EmailAccessPassword.objects.first()
    if access_pass is not None:
        return access_pass.check_password(password)
    return False

def status_change_access(password):
    access_pass = InterlockAccessPassword.objects.first()
    if access_pass is not None:
        return access_pass.check_password(password)
    return False