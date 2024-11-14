import random
import json
import traceback
from django.http import JsonResponse
from rest_framework import generics
import logging

logger = logging.getLogger(__name__)

#=================================== Exercise =============================================================

class GenerateOTPView(generics.ListCreateAPIView):
    
    def generate_otp(self):
        """Helper function to generate a 6-digit OTP."""
        digits = [str(i) for i in range(10)]
        return ''.join(random.choice(digits) for _ in range(6))

    def get(self, request, *args, **kwargs):
        try:
            otp = self.generate_otp()
            logger.info("OTP generated successfully")

            return JsonResponse({
                "status": "success",
                "message": "OTP generated successfully",
                "data": otp
            }, status=200)

        except Exception as e:
            logger.error("Error generating OTP: %s", e)
            traceback.print_exc()
            return JsonResponse({
                "status": "failed",
                "message": "There is a backend issue, please contact the administrator"
            }, status=500)
