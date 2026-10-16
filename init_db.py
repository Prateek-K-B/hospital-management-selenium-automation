from app import app
from models import db, User, Doctor, Patient, Department, Appointment, DoctorAvailability
from datetime import date, timedelta
import json

def init_database():
    with app.app_context():
        # Drop all tables and recreate
        db.drop_all()
        db.create_all()
        
        print("Creating database tables...")
        
        # Create departments
        departments_data = [
            {'name': 'Cardiology', 'description': 'Heart and cardiovascular system'},
            {'name': 'Neurology', 'description': 'Brain and nervous system'},
            {'name': 'Orthopedics', 'description': 'Bones, joints, and muscles'},
            {'name': 'Pediatrics', 'description': 'Children healthcare'},
            {'name': 'Dermatology', 'description': 'Skin, hair, and nails'},
            {'name': 'General Medicine', 'description': 'General health and wellness'}
        ]
        
        departments = []
        for dept_data in departments_data:
            dept = Department(**dept_data)
            db.session.add(dept)
            departments.append(dept)
        
        db.session.flush()
        print(f"Created {len(departments)} departments")
        
        # Create admin user
        admin = User(email='admin@hospital.com', role='admin')
        admin.set_password('admin123')
        db.session.add(admin)
        print("Created admin user (admin@hospital.com / admin123)")
        
        # Create sample doctors
        doctors_data = [
            {'email': 'dr.sharma@hospital.com', 'password': 'doctor123', 'name': 'Dr. Rajesh Sharma', 'dept_idx': 0, 'exp': 15, 'qual': 'MD Cardiology', 'phone': '9876543210'},
            {'email': 'dr.patel@hospital.com', 'password': 'doctor123', 'name': 'Dr. Priya Patel', 'dept_idx': 1, 'exp': 12, 'qual': 'MD Neurology', 'phone': '9876543211'},
            {'email': 'dr.kumar@hospital.com', 'password': 'doctor123', 'name': 'Dr. Amit Kumar', 'dept_idx': 2, 'exp': 10, 'qual': 'MS Orthopedics', 'phone': '9876543212'},
            {'email': 'dr.singh@hospital.com', 'password': 'doctor123', 'name': 'Dr. Sunita Singh', 'dept_idx': 3, 'exp': 8, 'qual': 'MD Pediatrics', 'phone': '9876543213'},
            {'email': 'dr.verma@hospital.com', 'password': 'doctor123', 'name': 'Dr. Anil Verma', 'dept_idx': 4, 'exp': 7, 'qual': 'MD Dermatology', 'phone': '9876543214'},
        ]
        
        doctors = []
        for doc_data in doctors_data:
            user = User(email=doc_data['email'], role='doctor')
            user.set_password(doc_data['password'])
            db.session.add(user)
            db.session.flush()
            
            doctor = Doctor(
                user_id=user.id,
                name=doc_data['name'],
                department_id=departments[doc_data['dept_idx']].id,
                experience_years=doc_data['exp'],
                qualification=doc_data['qual'],
                phone=doc_data['phone']
            )
            db.session.add(doctor)
            doctors.append(doctor)
        
        db.session.flush()
        print(f"Created {len(doctors)} doctors")
        
        # Set availability for doctors (next 7 days)
        time_slots = ["09:00-10:00", "10:00-11:00", "11:00-12:00", "14:00-15:00", "15:00-16:00", "16:00-17:00"]
        for doctor in doctors:
            for i in range(7):
                day = date.today() + timedelta(days=i)
                availability = DoctorAvailability(
                    doctor_id=doctor.id,
                    available_date=day,
                    time_slots=json.dumps(time_slots)
                )
                db.session.add(availability)
        
        print("Set doctor availability for next 7 days")
        
        # Create sample patients
        patients_data = [
            {'email': 'patient1@email.com', 'password': 'patient123', 'name': 'Rahul Mehta', 'phone': '9123456789', 'address': '123 MG Road, Mumbai', 'dob': '1990-05-15', 'blood': 'O+'},
            {'email': 'patient2@email.com', 'password': 'patient123', 'name': 'Sneha Reddy', 'phone': '9123456790', 'address': '456 Park Street, Delhi', 'dob': '1985-08-20', 'blood': 'A+'},
            {'email': 'patient3@email.com', 'password': 'patient123', 'name': 'Vikram Joshi', 'phone': '9123456791', 'address': '789 Brigade Road, Bangalore', 'dob': '1995-03-10', 'blood': 'B+'},
        ]
        
        patients = []
        for pat_data in patients_data:
            user = User(email=pat_data['email'], role='patient')
            user.set_password(pat_data['password'])
            db.session.add(user)
            db.session.flush()
            
            patient = Patient(
                user_id=user.id,
                name=pat_data['name'],
                phone=pat_data['phone'],
                address=pat_data['address'],
                date_of_birth=date.fromisoformat(pat_data['dob']),
                blood_group=pat_data['blood']
            )
            db.session.add(patient)
            patients.append(patient)
        
        db.session.flush()
        print(f"Created {len(patients)} patients")
        
        # Create sample appointments
        appointments_data = [
            {'patient_idx': 0, 'doctor_idx': 0, 'days_ahead': 1, 'slot': '09:00-10:00', 'status': 'Booked'},
            {'patient_idx': 1, 'doctor_idx': 1, 'days_ahead': 2, 'slot': '10:00-11:00', 'status': 'Booked'},
            {'patient_idx': 2, 'doctor_idx': 2, 'days_ahead': 0, 'slot': '14:00-15:00', 'status': 'Completed'},
        ]
        
        for appt_data in appointments_data:
            appointment = Appointment(
                patient_id=patients[appt_data['patient_idx']].id,
                doctor_id=doctors[appt_data['doctor_idx']].id,
                appointment_date=date.today() + timedelta(days=appt_data['days_ahead']),
                time_slot=appt_data['slot'],
                status=appt_data['status']
            )
            db.session.add(appointment)
        
        print(f"Created {len(appointments_data)} sample appointments")
        
        db.session.commit()
        print("\n✅ Database initialized successfully!")
        print("\n📋 Login Credentials:")
        print("=" * 50)
        print("Admin: admin@hospital.com / admin123")
        print("Doctor: dr.sharma@hospital.com / doctor123")
        print("Patient: patient1@email.com / patient123")
        print("=" * 50)

if __name__ == '__main__':
    init_database()
