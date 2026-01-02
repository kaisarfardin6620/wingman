from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status, viewsets
from rest_framework.permissions import IsAuthenticated
from django.contrib.auth import get_user_model
from authentication.utils import send_otp_via_email, verify_otp_via_email
from .models import Tone, Persona, UserSettings, TargetProfile
from .serializers import (
    ToneSerializer, PersonaSerializer, 
    UserSettingsSerializer, TargetProfileSerializer,
    PasscodeVerifySerializer, ResetPasscodeSerializer
)

User = get_user_model()

class ConfigDataView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        tones = Tone.objects.filter(is_active=True)
        personas = Persona.objects.filter(is_active=True)
        
        return Response({
            "tones": ToneSerializer(tones, many=True).data,
            "personas": PersonaSerializer(personas, many=True).data
        })

class UserSettingsView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        settings, created = UserSettings.objects.get_or_create(user=request.user)
        serializer = UserSettingsSerializer(settings)
        return Response(serializer.data)

    def patch(self, request):
        settings, created = UserSettings.objects.get_or_create(user=request.user)
        serializer = UserSettingsSerializer(settings, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response({"message": "Settings updated", "data": serializer.data})
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class TargetProfileViewSet(viewsets.ModelViewSet):
    permission_classes = [IsAuthenticated]
    serializer_class = TargetProfileSerializer

    def get_queryset(self):
        return TargetProfile.objects.filter(user=self.request.user).order_by('-created_at')

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)


class VerifyPasscodeView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request):
        serializer = PasscodeVerifySerializer(data=request.data)
        if serializer.is_valid():
            passcode_input = serializer.validated_data['passcode']
            user_settings = request.user.settings
            
            if not user_settings.passcode_lock_enabled:
                return Response({"message": "Passcode is not enabled."}, status=status.HTTP_200_OK)

            if user_settings.check_passcode(passcode_input):
                return Response({"success": True, "message": "Unlocked"}, status=status.HTTP_200_OK)
            else:
                return Response({"success": False, "error": "Incorrect passcode"}, status=status.HTTP_400_BAD_REQUEST)
        
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class ForgotPasscodeRequestView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request):
        if send_otp_via_email(request.user.email):
            return Response({"message": "OTP sent to your email."}, status=status.HTTP_200_OK)
        return Response({"error": "Failed to send OTP."}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

class ResetPasscodeConfirmView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request):
        serializer = ResetPasscodeSerializer(data=request.data)
        if serializer.is_valid():
            email = request.user.email
            otp = serializer.validated_data['otp']
            new_code = serializer.validated_data['new_passcode']

            if verify_otp_via_email(email, otp):
                settings = request.user.settings
                settings.set_passcode(new_code)
                settings.passcode_lock_enabled = True 
                settings.save()
                return Response({"message": "Passcode reset successfully."}, status=status.HTTP_200_OK)
            else:
                return Response({"error": "Invalid or expired OTP"}, status=status.HTTP_400_BAD_REQUEST)
        
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)