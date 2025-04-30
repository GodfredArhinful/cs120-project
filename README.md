# Mobile Stroke Unit Management System

A Django-based web application for managing mobile stroke unit operations, patient care, and clinical workflows.

## Features

- Patient management and tracking
- Real-time vital signs monitoring
- NIHSS score tracking
- Consultation management
- Alert system for critical events
- Dashboard with key metrics
- User authentication and role-based access

## Setup

1. Clone the repository:
```bash
git clone https://github.com/GodfredArhinful/cs120-project.git
cd cs120-project
```

2. Create and activate a virtual environment:
```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

3. Install dependencies:
```bash
pip install -r requirements.txt
```

4. Apply database migrations:
```bash
python manage.py migrate
```

5. Create a superuser:
```bash
python manage.py createsuperuser
```

6. Run the development server:
```bash
python manage.py runserver
```

## API Endpoints

### Authentication
- POST `/api/token/` - Obtain JWT token
- POST `/api/token/refresh/` - Refresh JWT token

### Patients
- GET `/api/patients/` - List all patients
- POST `/api/patients/` - Create new patient
- GET `/api/patients/{id}/` - Get patient details
- PUT `/api/patients/{id}/` - Update patient
- DELETE `/api/patients/{id}/` - Delete patient

### Vital Signs
- GET `/api/vital-signs/` - List all vital signs
- POST `/api/vital-signs/` - Create new vital signs record
- GET `/api/vital-signs/{id}/` - Get vital signs details

### Lab Results
- GET `/api/lab-results/` - List all lab results
- POST `/api/lab-results/` - Create new lab results
- GET `/api/lab-results/{id}/` - Get lab results details

### Imaging Studies
- GET `/api/imaging-studies/` - List all imaging studies
- POST `/api/imaging-studies/` - Create new imaging study
- GET `/api/imaging-studies/{id}/` - Get imaging study details

### NIHSS Scores
- GET `/api/nihss-scores/` - List all NIHSS scores
- POST `/api/nihss-scores/` - Create new NIHSS score
- GET `/api/nihss-scores/{id}/` - Get NIHSS score details

### Consultations
- GET `/api/consultations/` - List all consultations
- POST `/api/consultations/` - Create new consultation
- GET `/api/consultations/{id}/` - Get consultation details

### Alerts
- GET `/api/alerts/` - List all alerts
- POST `/api/alerts/{id}/acknowledge/` - Acknowledge an alert

## Security Considerations

- All API endpoints require authentication
- JWT tokens are used for authentication
- Data is stored securely following HIPAA guidelines
- All communications are encrypted
- Regular security audits are recommended

## Usage Example

1. Obtain a JWT token:
```bash
curl -X POST http://localhost:8000/api/token/ \
  -H "Content-Type: application/json" \
  -d '{"username":"your_username","password":"your_password"}'
```

2. Create a new patient:
```bash
curl -X POST http://localhost:8000/api/patients/ \
  -H "Authorization: Bearer your_token" \
  -H "Content-Type: application/json" \
  -d '{
    "name": "John Doe",
    "age": 65,
    "sex": "Male",
    "medical_history": "Hypertension, hyperlipidemia",
    "chief_complaint": "Sudden onset of weakness in left arm and leg"
  }'
```

## Development

- The system is built using Django and Django REST Framework
- Uses PostgreSQL as the database (recommended for production)
- Implements JWT authentication for secure API access
- Follows RESTful API design principles
- Implements automatic alerting based on critical values

## Contributing

1. Fork the repository
2. Create your feature branch (`git checkout -b feature/AmazingFeature`)
3. Commit your changes (`git commit -m 'Add some AmazingFeature'`)
4. Push to the branch (`git push origin feature/AmazingFeature`)
5. Open a Pull Request

## License

This project is licensed under the MIT License - see the LICENSE file for details. 