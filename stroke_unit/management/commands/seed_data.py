from django.core.management.base import BaseCommand
from django.contrib.auth import get_user_model
from django.utils import timezone
from stroke_unit.models import Patient, Consultation, VitalSigns, NIHSSScore, Alert
import random
from datetime import timedelta

User = get_user_model()

class Command(BaseCommand):
    help = 'Seeds the database with initial data for testing'

    def handle(self, *args, **kwargs):
        self.stdout.write('Seeding data...')

        # Create test users
        if not User.objects.filter(username='doctor1').exists():
            doctor1 = User.objects.create_user(
                username='doctor1',
                password='testpass123',
                first_name='John',
                last_name='Doe',
                email='doctor1@example.com',
                is_staff=True
            )
        else:
            doctor1 = User.objects.get(username='doctor1')

        if not User.objects.filter(username='doctor2').exists():
            doctor2 = User.objects.create_user(
                username='doctor2',
                password='testpass123',
                first_name='Jane',
                last_name='Smith',
                email='doctor2@example.com',
                is_staff=True
            )
        else:
            doctor2 = User.objects.get(username='doctor2')

        # Create test patients
        patient_data = [
            {
                'name': 'Alice Johnson',
                'age': 65,
                'sex': 'F',
                'phone_number': '555-0101',
                'emergency_contact': 'Bob Johnson (Husband) 555-0102',
                'chief_complaint': 'Sudden onset of right-sided weakness',
                'medical_history': 'Hypertension, Diabetes',
                'medications': 'Metformin, Lisinopril',
                'allergies': 'Penicillin',
            },
            {
                'name': 'Michael Brown',
                'age': 72,
                'sex': 'M',
                'phone_number': '555-0103',
                'emergency_contact': 'Sarah Brown (Daughter) 555-0104',
                'chief_complaint': 'Slurred speech and facial drooping',
                'medical_history': 'Atrial fibrillation',
                'medications': 'Warfarin',
                'allergies': 'None',
            },
            {
                'name': 'Emily Davis',
                'age': 58,
                'sex': 'F',
                'phone_number': '555-0105',
                'emergency_contact': 'James Davis (Son) 555-0106',
                'chief_complaint': 'Severe headache and confusion',
                'medical_history': 'Migraine',
                'medications': 'Sumatriptan',
                'allergies': 'Sulfa drugs',
            }
        ]

        created_patients = []
        for data in patient_data:
            patient, created = Patient.objects.get_or_create(
                name=data['name'],
                defaults=data
            )
            created_patients.append(patient)
            if created:
                self.stdout.write(f'Created patient: {patient.name}')

        # Create consultations
        consultation_types = ['Initial', 'Follow-up', 'Emergency']
        statuses = ['pending', 'in_progress', 'completed']

        for patient in created_patients:
            for _ in range(random.randint(1, 3)):
                consultation = Consultation.objects.create(
                    patient=patient,
                    consulting_doctor=random.choice([doctor1, doctor2]),
                    consultation_type=random.choice(consultation_types),
                    reason=f'Consultation for {patient.chief_complaint}',
                    notes='Test consultation notes',
                    status=random.choice(statuses),
                    created_at=timezone.now() - timedelta(days=random.randint(0, 30))
                )
                self.stdout.write(f'Created consultation for {patient.name}')

                # Create vital signs
                VitalSigns.objects.create(
                    patient=patient,
                    blood_pressure_systolic=random.randint(110, 180),
                    blood_pressure_diastolic=random.randint(60, 100),
                    heart_rate=random.randint(60, 100),
                    respiratory_rate=random.randint(12, 20),
                    temperature=round(random.uniform(36.5, 38.5), 1),
                    oxygen_saturation=random.randint(94, 100)
                )

                # Create NIHSS scores
                NIHSSScore.objects.create(
                    patient=patient,
                    score=random.randint(0, 42),
                    consciousness=random.randint(0, 3),
                    gaze=random.randint(0, 2),
                    visual=random.randint(0, 3),
                    facial_palsy=random.randint(0, 3),
                    motor_arm_left=random.randint(0, 4),
                    motor_arm_right=random.randint(0, 4),
                    motor_leg_left=random.randint(0, 4),
                    motor_leg_right=random.randint(0, 4),
                    limb_ataxia=random.randint(0, 2),
                    sensory=random.randint(0, 2),
                    language=random.randint(0, 3),
                    dysarthria=random.randint(0, 2),
                    extinction=random.randint(0, 2)
                )

        # Create alerts
        alert_types = ['CRITICAL', 'WARNING', 'INFO']
        alert_messages = [
            'Patient showing signs of deterioration',
            'Vital signs outside normal range',
            'New lab results available',
            'Medication due',
            'Follow-up required'
        ]

        for patient in created_patients:
            for _ in range(random.randint(1, 3)):
                Alert.objects.create(
                    patient=patient,
                    alert_type=random.choice(alert_types),
                    message=random.choice(alert_messages),
                    acknowledged=random.choice([True, False]),
                    acknowledged_by=random.choice([doctor1, doctor2]) if random.choice([True, False]) else None,
                    created_at=timezone.now() - timedelta(hours=random.randint(0, 48))
                )

        self.stdout.write(self.style.SUCCESS('Successfully seeded database')) 