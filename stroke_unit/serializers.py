from rest_framework import serializers
from django.contrib.auth.models import User
from .models import (
    Patient, VitalSigns, LabResult, ImagingStudy,
    NIHSSScore, Consultation, Alert
)

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'username', 'email', 'first_name', 'last_name']

class PatientSerializer(serializers.ModelSerializer):
    class Meta:
        model = Patient
        fields = '__all__'

class VitalSignsSerializer(serializers.ModelSerializer):
    class Meta:
        model = VitalSigns
        fields = '__all__'

class LabResultSerializer(serializers.ModelSerializer):
    class Meta:
        model = LabResult
        fields = '__all__'

class ImagingStudySerializer(serializers.ModelSerializer):
    class Meta:
        model = ImagingStudy
        fields = '__all__'

class NIHSSScoreSerializer(serializers.ModelSerializer):
    class Meta:
        model = NIHSSScore
        fields = '__all__'

class ConsultationSerializer(serializers.ModelSerializer):
    neurologist = UserSerializer(read_only=True)
    
    class Meta:
        model = Consultation
        fields = '__all__'

class AlertSerializer(serializers.ModelSerializer):
    acknowledged_by = UserSerializer(read_only=True)
    
    class Meta:
        model = Alert
        fields = '__all__' 