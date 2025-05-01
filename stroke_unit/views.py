from django.shortcuts import render
from rest_framework import viewsets, status
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from django.contrib.auth.models import User
from .models import (
    Patient, VitalSigns, LabResult, ImagingStudy,
    NIHSSScore, Consultation, Alert
)
from .serializers import (
    PatientSerializer, VitalSignsSerializer, LabResultSerializer,
    ImagingStudySerializer, NIHSSScoreSerializer, ConsultationSerializer,
    AlertSerializer
)
from django.views.generic import TemplateView, ListView, DetailView, CreateView, UpdateView
from django.views import View
from django.contrib.auth.mixins import LoginRequiredMixin
from django.utils import timezone
from django.db.models import Count, Avg, F, ExpressionWrapper, DurationField
from django.http import JsonResponse
from django.shortcuts import get_object_or_404
from datetime import timedelta
from django.urls import reverse_lazy
from django.contrib import messages
from .forms import UserRegistrationForm, PatientForm, ConsultationForm

# Create your views here.

class PatientViewSet(viewsets.ModelViewSet):
    queryset = Patient.objects.all()
    serializer_class = PatientSerializer
    permission_classes = [IsAuthenticated]

    @action(detail=True, methods=['get'])
    def vital_signs(self, request, pk=None):
        patient = self.get_object()
        vital_signs = patient.vital_signs.all()
        serializer = VitalSignsSerializer(vital_signs, many=True)
        return Response(serializer.data)

    @action(detail=True, methods=['get'])
    def lab_results(self, request, pk=None):
        patient = self.get_object()
        lab_results = patient.lab_results.all()
        serializer = LabResultSerializer(lab_results, many=True)
        return Response(serializer.data)

    @action(detail=True, methods=['get'])
    def imaging_studies(self, request, pk=None):
        patient = self.get_object()
        imaging_studies = patient.imaging_studies.all()
        serializer = ImagingStudySerializer(imaging_studies, many=True)
        return Response(serializer.data)

    @action(detail=True, methods=['get'])
    def nihss_scores(self, request, pk=None):
        patient = self.get_object()
        nihss_scores = patient.nihss_scores.all()
        serializer = NIHSSScoreSerializer(nihss_scores, many=True)
        return Response(serializer.data)

    @action(detail=True, methods=['get'])
    def consultations(self, request, pk=None):
        patient = self.get_object()
        consultations = patient.consultations.all()
        serializer = ConsultationSerializer(consultations, many=True)
        return Response(serializer.data)

    @action(detail=True, methods=['get'])
    def alerts(self, request, pk=None):
        patient = self.get_object()
        alerts = patient.alerts.all()
        serializer = AlertSerializer(alerts, many=True)
        return Response(serializer.data)

class VitalSignsViewSet(viewsets.ModelViewSet):
    queryset = VitalSigns.objects.all()
    serializer_class = VitalSignsSerializer
    permission_classes = [IsAuthenticated]

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)
        
        # Check for critical vital signs
        vital_signs = serializer.instance
        self._check_critical_vitals(vital_signs)
        
        headers = self.get_success_headers(serializer.data)
        return Response(serializer.data, status=status.HTTP_201_CREATED, headers=headers)

    def _check_critical_vitals(self, vital_signs):
        if (vital_signs.blood_pressure_systolic > 185 or 
            vital_signs.blood_pressure_diastolic > 110 or
            vital_signs.heart_rate < 60 or vital_signs.heart_rate > 100 or
            vital_signs.respiratory_rate < 12 or vital_signs.respiratory_rate > 20 or
            vital_signs.oxygen_saturation < 95):
            
            Alert.objects.create(
                patient=vital_signs.patient,
                alert_type='CRITICAL',
                message='Critical vital signs detected'
            )

class LabResultViewSet(viewsets.ModelViewSet):
    queryset = LabResult.objects.all()
    serializer_class = LabResultSerializer
    permission_classes = [IsAuthenticated]

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)
        
        # Check for critical lab results
        lab_result = serializer.instance
        self._check_critical_labs(lab_result)
        
        headers = self.get_success_headers(serializer.data)
        return Response(serializer.data, status=status.HTTP_201_CREATED, headers=headers)

    def _check_critical_labs(self, lab_result):
        if (lab_result.glucose_level and (lab_result.glucose_level < 50 or lab_result.glucose_level > 400) or
            lab_result.inr and lab_result.inr >= 3 or
            lab_result.platelet_count and lab_result.platelet_count < 100000):
            
            Alert.objects.create(
                patient=lab_result.patient,
                alert_type='CRITICAL',
                message='Critical lab results detected'
            )

class ImagingStudyViewSet(viewsets.ModelViewSet):
    queryset = ImagingStudy.objects.all()
    serializer_class = ImagingStudySerializer
    permission_classes = [IsAuthenticated]

class NIHSSScoreViewSet(viewsets.ModelViewSet):
    queryset = NIHSSScore.objects.all()
    serializer_class = NIHSSScoreSerializer
    permission_classes = [IsAuthenticated]

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)
        
        # Check NIHSS score for tPA eligibility
        nihss_score = serializer.instance
        if nihss_score.score >= 4:
            Alert.objects.create(
                patient=nihss_score.patient,
                alert_type='INFO',
                message=f'NIHSS score {nihss_score.score} indicates potential tPA eligibility'
            )
        
        headers = self.get_success_headers(serializer.data)
        return Response(serializer.data, status=status.HTTP_201_CREATED, headers=headers)

class ConsultationViewSet(viewsets.ModelViewSet):
    queryset = Consultation.objects.all()
    serializer_class = ConsultationSerializer
    permission_classes = [IsAuthenticated]

    def perform_create(self, serializer):
        serializer.save(consulting_doctor=self.request.user)

class AlertViewSet(viewsets.ModelViewSet):
    queryset = Alert.objects.all()
    serializer_class = AlertSerializer
    permission_classes = [IsAuthenticated]

    @action(detail=True, methods=['post'])
    def acknowledge(self, request, pk=None):
        alert = self.get_object()
        alert.acknowledged = True
        alert.acknowledged_by = request.user
        alert.save()
        return Response({'status': 'alert acknowledged'})

class DashboardView(LoginRequiredMixin, TemplateView):
    template_name = 'stroke_unit/dashboard.html'
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        today = timezone.now().date()
        
        # Add user to context
        context['user'] = self.request.user
        
        # Get statistics
        context['active_patients_count'] = Patient.objects.filter(discharged=False).count()
        context['consultations_today'] = Consultation.objects.filter(created_at__date=today).count()
        context['critical_alerts'] = Alert.objects.filter(alert_type='CRITICAL', acknowledged=False).count()
        
        # Calculate average response time (time between alert creation and acknowledgment)
        acknowledged_alerts = Alert.objects.filter(acknowledged=True, acknowledged_at__isnull=False, created_at__isnull=False)
        if acknowledged_alerts.exists():
            avg_response_time = acknowledged_alerts.annotate(
                response_time=ExpressionWrapper(
                    F('acknowledged_at') - F('created_at'),
                    output_field=DurationField()
                )
            ).aggregate(avg_time=Avg('response_time'))['avg_time']
            context['avg_response_time'] = str(avg_response_time).split('.')[0] if avg_response_time else "N/A"
        else:
            context['avg_response_time'] = "N/A"
        
        # Get recent patients and alerts
        context['recent_patients'] = Patient.objects.order_by('-created_at')[:5]
        context['recent_alerts'] = Alert.objects.order_by('-created_at')[:5]
        
        return context

class PatientListView(LoginRequiredMixin, ListView):
    model = Patient
    template_name = 'stroke_unit/patient_list.html'
    context_object_name = 'patients'
    paginate_by = 10
    
    def get_queryset(self):
        queryset = Patient.objects.all()
        
        # Apply search filter
        search = self.request.GET.get('search')
        if search:
            queryset = queryset.filter(name__icontains=search)
        
        # Apply status filter
        status = self.request.GET.get('status')
        if status == 'active':
            queryset = queryset.filter(discharged=False)
        elif status == 'discharged':
            queryset = queryset.filter(discharged=True)
        
        # Apply sorting
        sort = self.request.GET.get('sort', '-created_at')
        queryset = queryset.order_by(sort)
        
        return queryset

class PatientDetailView(LoginRequiredMixin, DetailView):
    model = Patient
    template_name = 'stroke_unit/patient_detail.html'
    context_object_name = 'patient'

class PatientCreateView(LoginRequiredMixin, CreateView):
    model = Patient
    form_class = PatientForm
    template_name = 'stroke_unit/patient_form.html'
    success_url = reverse_lazy('stroke_unit:patient_list')

    def form_valid(self, form):
        messages.success(self.request, 'Patient created successfully.')
        return super().form_valid(form)

    def form_invalid(self, form):
        messages.error(self.request, 'Please correct the errors below.')
        return super().form_invalid(form)

class VitalSignsCreateView(LoginRequiredMixin, CreateView):
    model = VitalSigns
    template_name = 'stroke_unit/vital_signs_form.html'
    fields = ['patient', 'blood_pressure_systolic', 'blood_pressure_diastolic', 
              'heart_rate', 'respiratory_rate', 'oxygen_saturation', 'temperature']
    
    def get_initial(self):
        initial = super().get_initial()
        patient_id = self.request.GET.get('patient')
        if patient_id:
            initial['patient'] = get_object_or_404(Patient, id=patient_id)
        return initial

class NIHSSCreateView(LoginRequiredMixin, CreateView):
    model = NIHSSScore
    template_name = 'stroke_unit/nihss_form.html'
    fields = ['patient', 'score']
    
    def get_initial(self):
        initial = super().get_initial()
        patient_id = self.request.GET.get('patient')
        if patient_id:
            initial['patient'] = get_object_or_404(Patient, id=patient_id)
        return initial

class ConsultationListView(LoginRequiredMixin, ListView):
    model = Consultation
    template_name = 'stroke_unit/consultation_list.html'
    context_object_name = 'consultations'
    paginate_by = 10
    ordering = ['-created_at']

class ConsultationCreateView(LoginRequiredMixin, CreateView):
    model = Consultation
    form_class = ConsultationForm
    template_name = 'stroke_unit/consultation_form.html'
    success_url = reverse_lazy('stroke_unit:consultation_list')

    def get_initial(self):
        initial = super().get_initial()
        patient_id = self.request.GET.get('patient')
        if patient_id:
            initial['patient'] = get_object_or_404(Patient, id=patient_id)
        return initial

    def form_valid(self, form):
        form.instance.consulting_doctor = self.request.user
        messages.success(self.request, 'Consultation created successfully.')
        return super().form_valid(form)

    def form_invalid(self, form):
        messages.error(self.request, 'Please correct the errors below.')
        return super().form_invalid(form)

class AlertListView(LoginRequiredMixin, ListView):
    model = Alert
    template_name = 'stroke_unit/alert_list.html'
    context_object_name = 'alerts'
    paginate_by = 10
    ordering = ['-created_at']

class AlertAcknowledgeView(LoginRequiredMixin, View):
    def post(self, request, pk):
        alert = get_object_or_404(Alert, pk=pk)
        if not alert.acknowledged:
            alert.acknowledged = True
            alert.acknowledged_by = request.user
            alert.acknowledged_at = timezone.now()
            alert.save()
        return JsonResponse({'status': 'success'})

class AlertCountView(LoginRequiredMixin, View):
    def get(self, request):
        count = Alert.objects.filter(acknowledged=False).count()
        return JsonResponse({'count': count})

class UserProfileView(LoginRequiredMixin, UpdateView):
    template_name = 'stroke_unit/profile.html'
    fields = ['first_name', 'last_name', 'email']
    
    def get_object(self):
        return self.request.user

class RegisterView(CreateView):
    template_name = 'stroke_unit/register.html'
    form_class = UserRegistrationForm
    success_url = reverse_lazy('login')

    def form_valid(self, form):
        response = super().form_valid(form)
        messages.success(self.request, 'Registration successful! Please log in.')
        return response

    def form_invalid(self, form):
        messages.error(self.request, 'Registration failed. Please correct the errors below.')
        return super().form_invalid(form)

class ConsultationDetailView(LoginRequiredMixin, DetailView):
    model = Consultation
    template_name = 'stroke_unit/consultation_detail.html'
    context_object_name = 'consultation'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        consultation = self.get_object()
        context['patient'] = consultation.patient
        context['vital_signs'] = consultation.patient.vital_signs.filter(
            created_at__lte=consultation.created_at
        ).order_by('-created_at').first()
        context['nihss_score'] = consultation.patient.nihss_scores.filter(
            created_at__lte=consultation.created_at
        ).order_by('-created_at').first()
        return context
