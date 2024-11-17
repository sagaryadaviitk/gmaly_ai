import random, string
from datetime import timedelta
from django.contrib.auth import get_user_model
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from django.utils import timezone
from users.models import User, OneTimeOTP
from users.models import OneTimeOTP, UserProfile


User = get_user_model()


class SendOTPView(APIView):
    def post(self, request):
        mobile = request.data.get('mobile')

        if not mobile:
            return Response({"error": "Mobile number is required"}, status=status.HTTP_400_BAD_REQUEST)

        try:
            # Check if the user exists or create a new user
            user, created = User.objects.get_or_create(mobile=mobile)

            # Generate OTP
            otp = ''.join(random.choices(string.digits, k=6))

            # Set OTP expiry time (e.g., 5 minutes from now)
            expiry_at = timezone.now() + timedelta(minutes=5)

            # Create OTP entry in the database
            OneTimeOTP.objects.create(user=user, otp=otp, expiry_at=expiry_at)

            # Send OTP to the user (you would use an SMS service in a real implementation)
            print(f"OTP for {mobile}: {otp}")  # For testing purposes

            return Response({"message": "OTP sent successfully."}, status=status.HTTP_200_OK)

        except Exception as e:
            return Response({"error": f"Failed to send OTP: {str(e)}"}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


class VerifyOTPView(APIView):
    def post(self, request):
        mobile = request.data.get('mobile')
        otp = request.data.get('otp')
        first_name = request.data.get('first_name', None)
        last_name = request.data.get('last_name', None)
        email = request.data.get('email', None)

        if not mobile or not otp:
            return Response({"error": "Mobile number and OTP are required"}, status=status.HTTP_400_BAD_REQUEST)

        try:
            # Verify OTP for the user
            otp_record = OneTimeOTP.objects.filter(user__mobile=mobile, otp=otp, used=False).first()
            if not otp_record:
                return Response({"error": "Invalid OTP or OTP already used"}, status=status.HTTP_400_BAD_REQUEST)

            # Check if OTP has expired
            if timezone.now() > otp_record.expiry_at:
                return Response({"error": "OTP has expired"}, status=status.HTTP_400_BAD_REQUEST)

            # Get or create user by mobile number
            user, created = User.objects.get_or_create(mobile=mobile)
            # If the user does not have a profile, create it
            if not hasattr(user, 'userprofile'):
                # Ensure that profile information is provided if user profile does not exist
                if not first_name or not last_name or not email:
                    return Response({"error": "Profile information (first name, last name, email) is required."}, status=status.HTTP_400_BAD_REQUEST)
                
                # Validate email uniqueness
                if UserProfile.objects.filter(email=email).exists():
                    return Response({"error": "A user with this email already exists."}, status=status.HTTP_400_BAD_REQUEST)

                # Create the UserProfile
                UserProfile.objects.create(
                    user=user,
                    first_name=first_name,
                    last_name=last_name,
                    email=email
                )

            # Mark OTP as used only after profile creation succeeds
            otp_record.used = True
            otp_record.save()

            # Generate access and refresh tokens
            refresh = RefreshToken.for_user(user)

            return Response({
                "message": "User logged in successfully.",
                "access_token": str(refresh.access_token),
                "refresh_token": str(refresh)
            }, status=status.HTTP_200_OK)

        except Exception as e:
            return Response({"error": f"Failed to verify OTP: {str(e)}"}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
