from django.db import models
from django.contrib.auth.models import User
from django.core.validators import MinValueValidator, MaxValueValidator

class Patient(models.Model):
    name = models.CharField(max_length=100)
    age = models.IntegerField()
    sex = models.CharField(max_length=1, choices=[('M', 'Male'), ('F', 'Female')])
    phone_number = models.CharField(max_length=20, blank=True)
    emergency_contact = models.CharField(max_length=200, blank=True)
    medical_history = models.TextField()
    chief_complaint = models.TextField()
    medications = models.TextField(blank=True)
    allergies = models.TextField(blank=True)
    discharged = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.name

class VitalSigns(models.Model):
    patient = models.ForeignKey(Patient, on_delete=models.CASCADE, related_name='vital_signs')
    blood_pressure_systolic = models.IntegerField()
    blood_pressure_diastolic = models.IntegerField()
    heart_rate = models.IntegerField()
    respiratory_rate = models.IntegerField()
    oxygen_saturation = models.IntegerField()
    temperature = models.DecimalField(max_digits=4, decimal_places=1)
    recorded_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Vitals for {self.patient.name} at {self.recorded_at}"

class LabResult(models.Model):
    patient = models.ForeignKey(Patient, on_delete=models.CASCADE, related_name='lab_results')
    cbc_normal = models.BooleanField()
    bmp_normal = models.BooleanField()
    coagulation_studies_normal = models.BooleanField()
    glucose_level = models.DecimalField(max_digits=5, decimal_places=1, null=True, blank=True)
    inr = models.DecimalField(max_digits=3, decimal_places=1, null=True, blank=True)
    platelet_count = models.IntegerField(null=True, blank=True)
    recorded_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Lab results for {self.patient.name} at {self.recorded_at}"

class ImagingStudy(models.Model):
    IMAGING_TYPES = [
        ('CT', 'CT Scan'),
        ('MRI', 'MRI'),
    ]
    
    patient = models.ForeignKey(Patient, on_delete=models.CASCADE, related_name='imaging_studies')
    imaging_type = models.CharField(max_length=3, choices=IMAGING_TYPES)
    findings = models.TextField()
    image_file = models.FileField(upload_to='imaging_studies/', null=True, blank=True)
    recorded_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.imaging_type} for {self.patient.name} at {self.recorded_at}"

class NIHSSScore(models.Model):
    patient = models.ForeignKey(Patient, on_delete=models.CASCADE, related_name='nihss_scores')
    score = models.IntegerField(validators=[MinValueValidator(0), MaxValueValidator(42)])
    consciousness = models.IntegerField(validators=[MinValueValidator(0), MaxValueValidator(3)])
    gaze = models.IntegerField(validators=[MinValueValidator(0), MaxValueValidator(2)])
    visual = models.IntegerField(validators=[MinValueValidator(0), MaxValueValidator(3)])
    facial_palsy = models.IntegerField(validators=[MinValueValidator(0), MaxValueValidator(3)])
    motor_arm_left = models.IntegerField(validators=[MinValueValidator(0), MaxValueValidator(4)])
    motor_arm_right = models.IntegerField(validators=[MinValueValidator(0), MaxValueValidator(4)])
    motor_leg_left = models.IntegerField(validators=[MinValueValidator(0), MaxValueValidator(4)])
    motor_leg_right = models.IntegerField(validators=[MinValueValidator(0), MaxValueValidator(4)])
    limb_ataxia = models.IntegerField(validators=[MinValueValidator(0), MaxValueValidator(2)])
    sensory = models.IntegerField(validators=[MinValueValidator(0), MaxValueValidator(2)])
    language = models.IntegerField(validators=[MinValueValidator(0), MaxValueValidator(3)])
    dysarthria = models.IntegerField(validators=[MinValueValidator(0), MaxValueValidator(2)])
    extinction = models.IntegerField(validators=[MinValueValidator(0), MaxValueValidator(2)])
    notes = models.TextField(blank=True)
    recorded_at = models.DateTimeField(auto_now_add=True)
    recorded_by = models.ForeignKey(User, on_delete=models.SET_NULL, null=True)

    def __str__(self):
        return f"NIHSS Score {self.score} for {self.patient.name}"

class Consultation(models.Model):
    CONSULTATION_TYPES = [
        ('Initial', 'Initial Consultation'),
        ('Follow-up', 'Follow-up'),
        ('Emergency', 'Emergency Consultation'),
    ]
    
    STATUS_CHOICES = [
        ('pending', 'Pending'),
        ('in_progress', 'In Progress'),
        ('completed', 'Completed'),
        ('cancelled', 'Cancelled'),
    ]

    patient = models.ForeignKey(Patient, on_delete=models.CASCADE, related_name='consultations')
    consulting_doctor = models.ForeignKey(User, on_delete=models.CASCADE)
    consultation_type = models.CharField(max_length=20, choices=CONSULTATION_TYPES, default='Initial')
    reason = models.TextField()
    notes = models.TextField(blank=True)
    diagnosis = models.TextField(blank=True)
    treatment_plan = models.TextField(blank=True)
    tpa_administered = models.BooleanField(default=False)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='pending')
    start_time = models.DateTimeField(null=True, blank=True)
    end_time = models.DateTimeField(null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"Consultation for {self.patient.name} by {self.consulting_doctor.get_full_name() or self.consulting_doctor.username}"

class Alert(models.Model):
    ALERT_TYPES = [
        ('CRITICAL', 'Critical Alert'),
        ('WARNING', 'Warning'),
        ('INFO', 'Information'),
    ]
    
    patient = models.ForeignKey(Patient, on_delete=models.CASCADE, related_name='alerts')
    alert_type = models.CharField(max_length=10, choices=ALERT_TYPES)
    message = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    acknowledged = models.BooleanField(default=False)
    acknowledged_by = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True)
    acknowledged_at = models.DateTimeField(null=True, blank=True)

    def __str__(self):
        return f"{self.alert_type} Alert for {self.patient.name}"
