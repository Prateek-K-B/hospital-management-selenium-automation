from flask import Flask, render_template, request, redirect, url_for, session, flash
from models import db, User, Doctor, Patient, Department, Appointment, Treatment, DoctorAvailability
from config import Config
from datetime import datetime, timedelta, date
from functools import wraps
import json

app = Flask(__name__)
app.config.from_object(Config)
app.config['SESSION_COOKIE_SAMESITE'] = 'Lax'
app.config['SESSION_COOKIE_SECURE'] = False
app.config['PERMANENT_SESSION_LIFETIME'] = timedelta(hours=24)
db.init_app(app)

# Time slots for appointments
TIME_SLOTS = [
    "09:00-10:00", "10:00-11:00", "11:00-12:00",
    "14:00-15:00", "15:00-16:00", "16:00-17:00"
]

# Decorator for login required
def login_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if 'user_id' not in session:
            flash('Please login to access this page.', 'warning')
            return redirect(url_for('login'))
        return f(*args, **kwargs)
    return decorated_function

# Decorator for role-based access
def role_required(role):
    def decorator(f):
        @wraps(f)
        def decorated_function(*args, **kwargs):
            if 'user_id' not in session:
                flash('Please login to access this page.', 'warning')
                return redirect(url_for('login'))
            user = User.query.get(session['user_id'])
            if user.role != role:
                flash('You do not have permission to access this page.', 'danger')
                return redirect(url_for('index'))
            return f(*args, **kwargs)
        return decorated_function
    return decorator

@app.route('/')
def index():
    if 'user_id' in session:
        user = User.query.get(session['user_id'])
        if user.role == 'admin':
            return redirect(url_for('admin_dashboard'))
        elif user.role == 'doctor':
            return redirect(url_for('doctor_dashboard'))
        elif user.role == 'patient':
            return redirect(url_for('patient_dashboard'))
    return redirect(url_for('login'))

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        email = request.form.get('email')
        password = request.form.get('password')
        
        user = User.query.filter_by(email=email).first()
        
        if user and user.check_password(password):
            if not user.is_active:
                flash('Your account has been deactivated. Please contact admin.', 'danger')
                return redirect(url_for('login'))
            
            session.permanent = True
            session['user_id'] = user.id
            session['user_role'] = user.role
            flash(f'Welcome back!', 'success')
            return redirect(url_for('index'))
        else:
            flash('Invalid email or password.', 'danger')
    
    return render_template('login.html')

@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        email = request.form.get('email')
        password = request.form.get('password')
        name = request.form.get('name')
        phone = request.form.get('phone')
        address = request.form.get('address')
        dob = request.form.get('dob')
        blood_group = request.form.get('blood_group')
        
        # Check if email already exists
        if User.query.filter_by(email=email).first():
            flash('Email already registered. Please login.', 'warning')
            return redirect(url_for('login'))
        
        # Create user
        user = User(email=email, role='patient')
        user.set_password(password)
        db.session.add(user)
        db.session.flush()
        
        # Create patient profile
        patient = Patient(
            user_id=user.id,
            name=name,
            phone=phone,
            address=address,
            date_of_birth=datetime.strptime(dob, '%Y-%m-%d').date() if dob else None,
            blood_group=blood_group
        )
        db.session.add(patient)
        db.session.commit()
        
        flash('Registration successful! Please login.', 'success')
        return redirect(url_for('login'))
    
    return render_template('register.html')

@app.route('/logout')
def logout():
    session.clear()
    flash('You have been logged out.', 'info')
    return redirect(url_for('login'))

# ==================== ADMIN ROUTES ====================

@app.route('/admin/dashboard')
@role_required('admin')
def admin_dashboard():
    total_doctors = Doctor.query.count()
    total_patients = Patient.query.count()
    total_appointments = Appointment.query.count()
    upcoming_appointments = Appointment.query.filter(
        Appointment.appointment_date >= date.today(),
        Appointment.status == 'Booked'
    ).count()
    
    return render_template('admin_dashboard.html',
                         total_doctors=total_doctors,
                         total_patients=total_patients,
                         total_appointments=total_appointments,
                         upcoming_appointments=upcoming_appointments)

@app.route('/admin/doctors', methods=['GET', 'POST'])
@role_required('admin')
def manage_doctors():
    if request.method == 'POST':
        action = request.form.get('action')
        
        if action == 'add':
            email = request.form.get('email')
            password = request.form.get('password')
            name = request.form.get('name')
            department_id = request.form.get('department_id')
            experience = request.form.get('experience')
            qualification = request.form.get('qualification')
            phone = request.form.get('phone')
            
            # Check if email exists
            if User.query.filter_by(email=email).first():
                flash('Email already exists.', 'danger')
                return redirect(url_for('manage_doctors'))
            
            # Create user
            user = User(email=email, role='doctor')
            user.set_password(password)
            db.session.add(user)
            db.session.flush()
            
            # Create doctor profile
            doctor = Doctor(
                user_id=user.id,
                name=name,
                department_id=department_id,
                experience_years=experience,
                qualification=qualification,
                phone=phone
            )
            db.session.add(doctor)
            db.session.commit()
            flash('Doctor added successfully!', 'success')
        
        elif action == 'edit':
            doctor_id = request.form.get('doctor_id')
            doctor = Doctor.query.get(doctor_id)
            if doctor:
                doctor.name = request.form.get('name')
                doctor.department_id = request.form.get('department_id')
                doctor.experience_years = request.form.get('experience')
                doctor.qualification = request.form.get('qualification')
                doctor.phone = request.form.get('phone')
                db.session.commit()
                flash('Doctor updated successfully!', 'success')
        
        elif action == 'delete':
            doctor_id = request.form.get('doctor_id')
            doctor = Doctor.query.get(doctor_id)
            if doctor:
                user = doctor.user
                user.is_active = False
                db.session.commit()
                flash('Doctor deactivated successfully!', 'success')
        
        return redirect(url_for('manage_doctors'))
    
    doctors = Doctor.query.join(User).filter(User.is_active == True).all()
    departments = Department.query.all()
    return render_template('manage_doctors.html', doctors=doctors, departments=departments)

@app.route('/admin/appointments')
@role_required('admin')
def manage_appointments():
    appointments = Appointment.query.order_by(Appointment.appointment_date.desc()).all()
    return render_template('manage_appointments.html', appointments=appointments)

@app.route('/admin/search')
@role_required('admin')
def admin_search():
    query = request.args.get('q', '')
    search_type = request.args.get('type', 'doctor')
    
    results = []
    if query:
        if search_type == 'doctor':
            results = Doctor.query.join(Department).filter(
                db.or_(
                    Doctor.name.ilike(f'%{query}%'),
                    Department.name.ilike(f'%{query}%')
                )
            ).all()
        elif search_type == 'patient':
            results = Patient.query.filter(
                db.or_(
                    Patient.name.ilike(f'%{query}%'),
                    Patient.phone.ilike(f'%{query}%'),
                    Patient.id == query if query.isdigit() else False
                )
            ).all()
    
    return render_template('admin_search.html', results=results, query=query, search_type=search_type)

# ==================== DOCTOR ROUTES ====================

@app.route('/doctor/dashboard')
@role_required('doctor')
def doctor_dashboard():
    user = User.query.get(session['user_id'])
    doctor = user.doctor
    
    # Today's appointments
    today_appointments = Appointment.query.filter(
        Appointment.doctor_id == doctor.id,
        Appointment.appointment_date == date.today()
    ).all()
    
    # This week's appointments
    week_end = date.today() + timedelta(days=7)
    week_appointments = Appointment.query.filter(
        Appointment.doctor_id == doctor.id,
        Appointment.appointment_date >= date.today(),
        Appointment.appointment_date <= week_end
    ).all()
    
    # Unique patients
    patients = Patient.query.join(Appointment).filter(
        Appointment.doctor_id == doctor.id
    ).distinct().all()
    
    return render_template('doctor_dashboard.html',
                         doctor=doctor,
                         today_appointments=today_appointments,
                         week_appointments=week_appointments,
                         patients=patients)

@app.route('/doctor/availability', methods=['GET', 'POST'])
@role_required('doctor')
def doctor_availability():
    user = User.query.get(session['user_id'])
    doctor = user.doctor
    
    if request.method == 'POST':
        # Clear existing availability
        DoctorAvailability.query.filter_by(doctor_id=doctor.id).delete()
        
        # Add new availability for next 7 days
        for i in range(7):
            day_date = date.today() + timedelta(days=i)
            day_key = f'day_{i}'
            
            if request.form.get(day_key):
                selected_slots = request.form.getlist(f'slots_{i}')
                if selected_slots:
                    availability = DoctorAvailability(
                        doctor_id=doctor.id,
                        available_date=day_date,
                        time_slots=json.dumps(selected_slots)
                    )
                    db.session.add(availability)
        
        db.session.commit()
        flash('Availability updated successfully!', 'success')
        return redirect(url_for('doctor_dashboard'))
    
    # Get existing availability
    availabilities = {}
    for avail in doctor.availabilities:
        # Use ISO format string as key instead of date object for template compatibility
        availabilities[avail.available_date.isoformat()] = json.loads(avail.time_slots)
    
    # Generate next 7 days
    next_7_days = [(date.today() + timedelta(days=i)) for i in range(7)]
    
    return render_template('doctor_availability.html',
                         doctor=doctor,
                         next_7_days=next_7_days,
                         availabilities=availabilities,
                         time_slots=TIME_SLOTS)

@app.route('/doctor/appointment/<int:appointment_id>', methods=['GET', 'POST'])
@role_required('doctor')
def appointment_details(appointment_id):
    appointment = Appointment.query.get_or_404(appointment_id)
    user = User.query.get(session['user_id'])
    
    # Verify doctor owns this appointment
    if appointment.doctor_id != user.doctor.id:
        flash('Unauthorized access.', 'danger')
        return redirect(url_for('doctor_dashboard'))
    
    if request.method == 'POST':
        action = request.form.get('action')
        
        if action == 'complete':
            diagnosis = request.form.get('diagnosis')
            prescription = request.form.get('prescription')
            notes = request.form.get('notes')
            
            # Create treatment record
            treatment = Treatment(
                appointment_id=appointment.id,
                diagnosis=diagnosis,
                prescription=prescription,
                notes=notes
            )
            db.session.add(treatment)
            
            # Update appointment status
            appointment.status = 'Completed'
            db.session.commit()
            
            flash('Treatment added and appointment marked as completed!', 'success')
            return redirect(url_for('doctor_dashboard'))
        
        elif action == 'cancel':
            appointment.status = 'Cancelled'
            db.session.commit()
            flash('Appointment cancelled.', 'info')
            return redirect(url_for('doctor_dashboard'))
    
    # Get patient history
    patient_history = Appointment.query.filter(
        Appointment.patient_id == appointment.patient_id,
        Appointment.status == 'Completed'
    ).order_by(Appointment.appointment_date.desc()).all()
    
    return render_template('appointment_details.html',
                         appointment=appointment,
                         patient_history=patient_history)

# ==================== PATIENT ROUTES ====================

@app.route('/patient/dashboard')
@role_required('patient')
def patient_dashboard():
    user = User.query.get(session['user_id'])
    patient = user.patient
    
    # Get all departments
    departments = Department.query.all()
    
    # Upcoming appointments
    upcoming_appointments = Appointment.query.filter(
        Appointment.patient_id == patient.id,
        Appointment.appointment_date >= date.today(),
        Appointment.status == 'Booked'
    ).order_by(Appointment.appointment_date).all()
    
    return render_template('patient_dashboard.html',
                         patient=patient,
                         departments=departments,
                         upcoming_appointments=upcoming_appointments)

@app.route('/patient/doctors')
@role_required('patient')
def browse_doctors():
    department_id = request.args.get('department_id')
    search_query = request.args.get('q', '')
    
    query = Doctor.query.join(User).filter(User.is_active == True)
    
    if department_id:
        query = query.filter(Doctor.department_id == department_id)
    
    if search_query:
        query = query.join(Department).filter(
            db.or_(
                Doctor.name.ilike(f'%{search_query}%'),
                Department.name.ilike(f'%{search_query}%')
            )
        )
    
    doctors = query.all()
    departments = Department.query.all()
    
    return render_template('browse_doctors.html',
                         doctors=doctors,
                         departments=departments,
                         selected_department=department_id,
                         search_query=search_query)

@app.route('/patient/book/<int:doctor_id>', methods=['GET', 'POST'])
@role_required('patient')
def book_appointment(doctor_id):
    doctor = Doctor.query.get_or_404(doctor_id)
    user = User.query.get(session['user_id'])
    patient = user.patient
    
    if request.method == 'POST':
        appointment_date = request.form.get('appointment_date')
        time_slot = request.form.get('time_slot')
        
        # Convert to date object
        appt_date = datetime.strptime(appointment_date, '%Y-%m-%d').date()
        
        # Check for conflicts
        existing = Appointment.query.filter(
            Appointment.doctor_id == doctor_id,
            Appointment.appointment_date == appt_date,
            Appointment.time_slot == time_slot,
            Appointment.status == 'Booked'
        ).first()
        
        if existing:
            flash('This time slot is already booked. Please choose another.', 'danger')
            return redirect(url_for('book_appointment', doctor_id=doctor_id))
        
        # Create appointment
        appointment = Appointment(
            patient_id=patient.id,
            doctor_id=doctor_id,
            appointment_date=appt_date,
            time_slot=time_slot,
            status='Booked'
        )
        db.session.add(appointment)
        db.session.commit()
        
        flash('Appointment booked successfully!', 'success')
        return redirect(url_for('patient_dashboard'))
    
    # Get doctor availability for next 7 days
    next_7_days = []
    for i in range(7):
        day = date.today() + timedelta(days=i)
        availability = DoctorAvailability.query.filter_by(
            doctor_id=doctor_id,
            available_date=day
        ).first()
        
        available_slots = []
        if availability:
            all_slots = json.loads(availability.time_slots)
            # Check which slots are not booked
            for slot in all_slots:
                existing = Appointment.query.filter(
                    Appointment.doctor_id == doctor_id,
                    Appointment.appointment_date == day,
                    Appointment.time_slot == slot,
                    Appointment.status == 'Booked'
                ).first()
                if not existing:
                    available_slots.append(slot)
        
        next_7_days.append({
            'date': day,
            'slots': available_slots
        })
    
    return render_template('book_appointment.html',
                         doctor=doctor,
                         next_7_days=next_7_days)

@app.route('/patient/appointments')
@role_required('patient')
def appointment_history():
    user = User.query.get(session['user_id'])
    patient = user.patient
    
    appointments = Appointment.query.filter(
        Appointment.patient_id == patient.id
    ).order_by(Appointment.appointment_date.desc()).all()
    
    return render_template('appointment_history.html', appointments=appointments)

@app.route('/patient/cancel/<int:appointment_id>')
@role_required('patient')
def cancel_appointment(appointment_id):
    appointment = Appointment.query.get_or_404(appointment_id)
    user = User.query.get(session['user_id'])
    
    # Verify patient owns this appointment
    if appointment.patient_id != user.patient.id:
        flash('Unauthorized access.', 'danger')
        return redirect(url_for('patient_dashboard'))
    
    if appointment.status == 'Booked':
        appointment.status = 'Cancelled'
        db.session.commit()
        flash('Appointment cancelled successfully.', 'info')
    else:
        flash('Cannot cancel this appointment.', 'warning')
    
    return redirect(url_for('appointment_history'))

@app.route('/patient/profile', methods=['GET', 'POST'])
@role_required('patient')
def edit_profile():
    user = User.query.get(session['user_id'])
    patient = user.patient
    
    if request.method == 'POST':
        patient.name = request.form.get('name')
        patient.phone = request.form.get('phone')
        patient.address = request.form.get('address')
        dob = request.form.get('dob')
        if dob:
            patient.date_of_birth = datetime.strptime(dob, '%Y-%m-%d').date()
        patient.blood_group = request.form.get('blood_group')
        
        db.session.commit()
        flash('Profile updated successfully!', 'success')
        return redirect(url_for('patient_dashboard'))
    
    return render_template('edit_profile.html', patient=patient)

if __name__ == '__main__':
    app.run(debug=True)
