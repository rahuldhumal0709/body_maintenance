import json
import traceback
import random
from django.http import HttpResponse, JsonResponse
from rest_framework import generics
from djangoapp.models import *
import logging
import math
from djangoapp.utilities.user_auth import Auth
from rest_framework.permissions import IsAuthenticated
from psycopg2 import *
from rest_framework.decorators import api_view
from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth.decorators import login_required

logger = logging.getLogger(__name__)
logger = logging.getLogger("django")

backend_issue = "There is backend issue, please contact administrator"