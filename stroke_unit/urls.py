from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import (
    PatientViewSet, VitalSignsViewSet, LabResultViewSet,
    ImagingStudyViewSet, NIHSSScoreViewSet, ConsultationViewSet,
    AlertViewSet
)
from . import views

router = DefaultRouter()
router.register(r'patients', PatientViewSet)
router.register(r'vital-signs', VitalSignsViewSet)
router.register(r'lab-results', LabResultViewSet)
router.register(r'imaging-studies', ImagingStudyViewSet)
router.register(r'nihss-scores', NIHSSScoreViewSet)
router.register(r'consultations', ConsultationViewSet)
router.register(r'alerts', AlertViewSet)

app_name = 'stroke_unit'

urlpatterns = [
    # API URLs
    path('api/', include(router.urls)),
    
    # Template URLs
    path('', views.DashboardView.as_view(), name='dashboard'),
    
    # Patient URLs
    path('patients/', views.PatientListView.as_view(), name='patient_list'),
    path('patients/create/', views.PatientCreateView.as_view(), name='patient_create'),
    path('patients/<int:pk>/', views.PatientDetailView.as_view(), name='patient_detail'),
    
    # Vital Signs URLs
    path('vitals/create/', views.VitalSignsCreateView.as_view(), name='vital_signs_create'),
    
    # NIHSS Score URLs
    path('nihss/create/', views.NIHSSCreateView.as_view(), name='nihss_create'),
    
    # Consultation URLs
    path('consultations/', views.ConsultationListView.as_view(), name='consultation_list'),
    path('consultations/create/', views.ConsultationCreateView.as_view(), name='consultation_create'),
    path('consultations/<int:pk>/', views.ConsultationDetailView.as_view(), name='consultation_detail'),
    
    # Alert URLs
    path('alerts/', views.AlertListView.as_view(), name='alert_list'),
    path('api/alerts/<int:pk>/acknowledge/', views.AlertAcknowledgeView.as_view(), name='alert_acknowledge'),
    path('api/alerts/', views.AlertCountView.as_view(), name='alert_count'),
    
    # User Profile
    path('profile/', views.UserProfileView.as_view(), name='profile'),
    
    # Authentication
    path('register/', views.RegisterView.as_view(), name='register'),
] 