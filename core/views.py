from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status, viewsets
from rest_framework.permissions import IsAuthenticated
from .models import Tone, Persona, UserSettings, TargetProfile
from .serializers import (
    ToneSerializer, PersonaSerializer, 
    UserSettingsSerializer, TargetProfileSerializer
)


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