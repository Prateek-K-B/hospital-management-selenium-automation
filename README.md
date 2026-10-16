# Hospital Management System – Selenium Automation Testing

A web-based Hospital Management System built with Flask, with an automated UI testing suite developed using Selenium WebDriver, Python, and Pytest.

![Python](https://img.shields.io/badge/Python-3.8+-3776AB?style=flat&logo=python&logoColor=white)
![Flask](https://img.shields.io/badge/Flask-3.0.0-black?style=flat&logo=flask&logoColor=white)
![Selenium](https://img.shields.io/badge/Selenium-WebDriver-43B02A?style=flat&logo=selenium&logoColor=white)
![Pytest](https://img.shields.io/badge/Pytest-Testing-0A9EDC?style=flat&logo=pytest&logoColor=white)
![SQLite](https://img.shields.io/badge/Database-SQLite-003B57?style=flat&logo=sqlite&logoColor=white)

---

## Project Overview

The Hospital Management System is a web application designed to simplify hospital operations by supporting three user roles: Administrators, Doctors, and Patients.

The application supports doctor management, appointment scheduling, doctor availability, patient registration, and treatment records.

This project also includes a Selenium automation testing suite to validate important application functionalities through automated browser testing.

### Key Highlights

- Role-based access for Admin, Doctor, and Patient.
- Doctor registration and management.
- Appointment booking and management.
- Doctor availability management.
- Patient registration and login.
- Doctor search functionality.
- Automated UI testing using Selenium WebDriver.
- Test execution and HTML report generation using Pytest.

---

## Application Features

### Admin Features

- Manage doctor registrations.
- Approve or remove doctors.
- View hospital appointments.
- Search doctors by name or specialization.
- Monitor appointment information.

### Doctor Features

- Manage availability and time slots.
- View patient appointments.
- Confirm or cancel appointments.
- Maintain treatment records.
- Add diagnoses and prescriptions.

### Patient Features

- Register and log in.
- Browse available doctors.
- View doctor specializations and qualifications.
- Book appointments.
- View appointment history.
- Access treatment records and prescriptions.

---

## Tech Stack

### Application Technologies

| Technology | Purpose |
|---|---|
| Python | Application programming language |
| Flask | Web application framework |
| Flask-SQLAlchemy | Database integration |
| SQLAlchemy | Object-relational mapping |
| SQLite | Database |
| HTML and CSS | Web page structure and styling |
| Bootstrap | Responsive user interface |
| Jinja2 | HTML templating |
| Werkzeug | Security utilities and password hashing |

### Automation Testing Technologies

| Technology | Purpose |
|---|---|
| Python | Writing automation scripts |
| Selenium WebDriver | Browser automation |
| Pytest | Test execution and assertions |
| pytest-html | HTML test report generation |
| Google Chrome | Browser used for testing |
| PyCharm | Development environment |
| Git and GitHub | Version control and project hosting |

---

## Automated Testing

The project includes a UI automation testing suite developed using Selenium WebDriver and Python.

Pytest is used to organize and execute the test cases, while pytest-html generates an HTML report containing the execution results.

### Test Coverage

The automation suite contains 10 test cases across four test modules.

| Test Module | Test Scenarios |
|---|---|
| `test_login.py` | Valid patient login, invalid password, and invalid email |
| `test_registration.py` | Patient registration |
| `test_doctors.py` | Doctor listing, doctor search, department dropdown, and appointment button |
| `test_appointments.py` | Appointment booking page and date selection |

### Test Execution Results

The following results were recorded during a successful local test execution.

| Metric | Result |
|---|---:|
| Total Test Cases | 10 |
| Passed | 10 |
| Failed | 0 |
| Skipped | 0 |
| Execution Time | Approximately 77 seconds |

**Result:** All 10 automated test cases passed in the recorded execution.

### HTML Test Report

An HTML report is generated after the test suite runs.

Report location:

`reports/report.html`

The report includes test names, execution status, and overall test results.

---

## Project Structure

```text
hospital-management-system-main/
│
├── app.py
├── config.py
├── models.py
├── init_db.py
├── requirements.txt
├── README.md
├── Project_Report.pdf
│
├── instance/
│   └── hospital.db
│
├── static/
│   └── style.css
│
├── templates/
│   ├── base.html
│   ├── index.html
│   ├── login.html
│   ├── register.html
│   ├── admin_dashboard.html
│   ├── manage_doctors.html
│   ├── all_appointments.html
│   ├── search_doctors.html
│   ├── doctor_dashboard.html
│   ├── doctor_availability.html
│   ├── doctor_appointments.html
│   ├── add_treatment.html
│   ├── patient_dashboard.html
│   ├── browse_doctors.html
│   ├── book_appointment.html
│   └── patient_appointments.html
│
├── tests/
│   ├── test_appointments.py
│   ├── test_doctors.py
│   ├── test_login.py
│   └── test_registration.py
│
└── reports/
    └── report.html