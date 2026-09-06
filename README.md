# 🎓 Student Management System

A web-based Student Management System developed using Python and Django.

This project provides a centralized platform for managing students, teachers, courses, attendance, fees, assignments, examinations, and academic results.

## 🚀 Features

### 🔐 Authentication
- User login
- User authentication
- Secure access to the management system
- Logout functionality

### 👨‍🎓 Student Management
- Add students
- View student details
- Edit student information
- Delete students
- Upload student photo
- Store admission number
- Store personal and contact details
- Assign students to courses
- Search students

### 👨‍🏫 Teacher Management
- Add teachers
- View teacher details
- Edit teacher information
- Delete teachers
- Store teacher ID
- Store qualification and experience
- Store contact information
- Assign subjects to teachers
- Search teachers

### 📚 Course Management
- Add courses
- View courses
- Edit courses
- Delete courses
- Store course code
- Store course duration
- Store total semesters

### 📖 Subject Management
- Add subjects
- Assign subjects to courses
- Store subject code
- Store semester information
- Manage subjects related to each course

### 📅 Attendance Management
- Record student attendance
- Select student, subject, and teacher
- Mark attendance as:
  - Present
  - Absent
  - Late
- Add attendance remarks
- View attendance details
- Edit attendance records
- Delete attendance records
- Prevent duplicate attendance records for the same student, subject, and date

### 💰 Fee Management
- Add fee records
- View fee details
- Edit fee records
- Delete fee records
- Store receipt number
- Store fee amount
- Store due date
- Store payment date
- Track payment status:
  - Paid
  - Pending
  - Partial
- Search fee records

### 📝 Assignment Management
- Add assignments
- Assign assignments to students
- Assign subjects and teachers
- Set assignment due dates
- Record submission dates
- Track assignment status:
  - Pending
  - Submitted
  - Late
- Store assignment marks
- View, edit, and delete assignments
- Search assignments

### 🧪 Exam Management
- Add examinations
- Assign subjects to exams
- Set examination dates
- Set total marks
- Set passing marks
- Add exam descriptions
- View exam details
- Edit exams
- Delete exams
- Search examinations

### 📊 Result Management
- Add student examination results
- Select student and examination
- Enter marks
- Automatically calculate grades
- Automatically determine Pass/Fail
- View result details
- Edit results
- Delete results
- Search results

## 📈 Dashboard

The dashboard provides an overview of the entire student management system.

It displays:

- Total Students
- Total Teachers
- Total Courses
- Total Subjects
- Attendance Records
- Pending Fees
- Total Exams
- Recent Students

The dashboard provides quick access to important modules through the sidebar.

## 🛠️ Technologies Used

### Backend
- Python
- Django

### Frontend
- HTML5
- CSS3
- Bootstrap
- Bootstrap Icons
- JavaScript

### Database
- SQLite

### Development Tools
- Visual Studio Code
- Git
- GitHub

## 🗂️ Main Django Applications

The project is divided into multiple Django applications:

- `accounts` – Authentication and user management
- `dashboard` – Dashboard and statistics
- `students` – Student management
- `teachers` – Teacher management
- `courses` – Course and subject management
- `attendance` – Student attendance management
- `fees` – Fee management
- `assignments` – Assignment management
- `exams` – Examination management
- `results` – Examination results and grades

## 🗃️ Database Relationships

The project uses relational database models to connect different entities.

### Student
A student belongs to a course and can have:

- Attendance records
- Fee records
- Assignments
- Examination results

### Teacher
A teacher can be associated with a subject and can manage:

- Attendance
- Assignments

### Course
A course contains multiple subjects.

### Subject
A subject belongs to a course and can be associated with:

- Teachers
- Attendance records
- Assignments
- Exams

### Exam
An exam belongs to a subject and can have results for multiple students.

### Result
A result connects a student with an exam and stores:

- Marks
- Grade
- Pass/Fail status

## 🔄 Grade Calculation

The system automatically calculates grades based on marks.

| Marks | Grade |
|------:|:-----:|
| 90 and above | A+ |
| 80 - 89 | A |
| 70 - 79 | B |
| 60 - 69 | C |
| 50 - 59 | D |
| Below 50 | F |

The system also compares the student's marks with the examination's passing marks to determine the result.

## 🔎 Search Functionality

Search functionality is implemented across multiple modules.

Users can search for:

- Students by name or admission number
- Teachers by name
- Fees by student or receipt number
- Assignments by student, subject, or assignment title
- Exams by exam name or subject
- Results by student or exam

## 🔐 Data Management

The application provides CRUD operations across the major modules.

CRUD stands for:

- **Create** – Add new records
- **Read** – View existing records
- **Update** – Edit records
- **Delete** – Remove records

These operations are implemented for students, teachers, courses, attendance, fees, assignments, exams, and results.

## 🎯 Project Objectives

The main objectives of the project are:

- Digitize student record management
- Reduce manual record keeping
- Manage student and teacher information
- Track attendance efficiently
- Manage student fees
- Manage assignments and examinations
- Maintain academic results
- Provide quick access to student information
- Provide centralized academic management

## 💡 Key Highlights

- Modular Django application structure
- Relational database design
- Django ModelForm-based forms
- CRUD functionality
- Search functionality
- Authentication
- Dashboard statistics
- Automatic grade calculation
- Attendance status management
- Fee status tracking
- Responsive Bootstrap interface
- Student photo upload functionality

## 📌 Future Enhancements

Possible future improvements include:

- Role-based access for Admin, Teachers, and Students
- Student-specific dashboard
- Teacher-specific dashboard
- Attendance percentage calculation
- Automated fee receipts
- Report card generation
- PDF reports
- Excel/CSV export
- Email notifications
- Advanced filtering and pagination
- Graphs and analytics
- REST API integration
- Online deployment

## 👨‍💻 Author

**Pavitra Vaidya**

Student Management System developed as a Django web development project.
