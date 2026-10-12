🎓 Student Management System with AI Chatbot

A comprehensive web-based Student Management System developed using Python, Django, SQLite, and Bootstrap, with an integrated AI-powered chatbot using Ollama and Llama 3.2.

The application provides a centralized platform for managing students, teachers, courses, subjects, attendance, fees, assignments, examinations, and academic results.

It combines traditional academic management functionality with conversational AI to create an interactive user experience.

🚀 Key Features

🤖 AI-Powered Chatbot (Ollama + Llama 3.2)

The application integrates a locally running AI chatbot powered by Ollama and the Llama 3.2 language model.

Features:

- Interactive chatbot interface within the web application
- Natural language question-answering
- AI-generated responses to general queries
- Backend integration between Django and Ollama
- Local LLM execution without requiring a cloud AI API key
- Conversational assistance through the application interface

How it works:

1. The user enters a question in the chatbot interface.
2. JavaScript sends the question to the Django backend.
3. Django forwards the request to the locally running Ollama model.
4. Llama 3.2 processes the question and generates a response.
5. Django returns the generated response to the frontend.
6. The chatbot displays the response to the user.

AI Chatbot Architecture:

User
  |
  v
Chatbot Interface
  |
  v
JavaScript / HTTP Request
  |
  v
Django Backend
  |
  v
Ollama (Llama 3.2)
  |
  v
Generated Response
  |
  v
Django Backend
  |
  v
Chatbot Interface

Note: The current chatbot provides general conversational assistance. Database-aware answers, such as retrieving individual student fees, attendance, and results, are planned enhancements.

🔐 Authentication and User Management

- User login and logout
- Django authentication system
- Secure password handling
- Authenticated access to application features
- Session management

👨‍🎓 Student Management

- Add, view, update, and delete student records
- Upload student profile photographs
- Manage admission numbers and personal details
- Store parent and contact information
- Assign students to courses
- Search students by name or admission number

👨‍🏫 Teacher Management

- Add, view, update, and delete teacher records
- Store teacher IDs, qualifications, and experience
- Manage contact information
- Assign subjects to teachers
- Search teacher records

📚 Course and Subject Management

- Create, update, and delete courses
- Store course codes, duration, and semesters
- Add and manage subjects
- Associate subjects with courses
- Store subject codes and semester details

📅 Attendance Management

- Record student attendance
- Assign subjects and teachers
- Mark attendance as Present, Absent, or Late
- Add attendance remarks
- Update and delete attendance records
- Prevent duplicate attendance entries for the same student, subject, and date

💰 Fee Management

- Add, edit, view, and delete fee records
- Generate and store receipt numbers
- Manage fee amounts and due dates
- Track payment dates
- Monitor payment statuses: Paid, Pending, and Partial
- Search fee records

📝 Assignment Management

- Create and assign student assignments
- Associate assignments with subjects and teachers
- Manage due dates and submission dates
- Track Pending, Submitted, and Late statuses
- Record assignment marks
- Search and manage assignments

🧪 Examination Management

- Create, edit, and delete examinations
- Associate examinations with subjects
- Set examination dates
- Define total and passing marks
- Store examination descriptions
- Search examinations

📊 Result Management

- Record student examination marks
- Automatically calculate grades
- Automatically determine Pass/Fail status
- Manage student examination results
- Search results by student or examination

📈 Interactive Dashboard

The dashboard displays key academic statistics, including:

- Total Students
- Total Teachers
- Total Courses
- Total Subjects
- Attendance Records
- Pending Fees
- Total Exams
- Recent Students

It also provides navigation to the application's major modules.

🛠️ Technology Stack

Category| Technologies
Programming Language| Python
Backend Framework| Django
Frontend| HTML5, CSS3, JavaScript
UI Framework| Bootstrap, Bootstrap Icons
Database| SQLite
AI / LLM| Ollama, Llama 3.2
ORM| Django ORM
Version Control| Git, GitHub
Development Environment| Visual Studio Code

🏗️ Project Architecture

The application follows Django's Model-View-Template (MVT) architecture.

Student Management System
│
├── accounts/
│   └── Authentication and user management
│
├── dashboard/
│   └── Dashboard and statistics
│
├── students/
│   └── Student records
│
├── teachers/
│   └── Teacher records
│
├── courses/
│   └── Course and subject management
│
├── attendance/
│   └── Attendance tracking
│
├── fees/
│   └── Fee management
│
├── assignments/
│   └── Assignment management
│
├── exams/
│   └── Examination management
│
├── results/
│   └── Result and grade management
│
└── AI Chatbot Integration
    └── Django + Ollama + Llama 3.2

🗃️ Database Design

The system uses relational database models connected through Django ORM.

Key Relationships:

- Student → Course
- Course → Subjects
- Teacher → Subjects
- Student → Attendance
- Student → Fees
- Student → Assignments
- Subject → Exams
- Student + Exam → Result

These relationships maintain structured academic records and enable efficient data retrieval.

🎯 Automatic Grade Calculation

The application calculates student grades based on examination marks.

Marks| Grade
90 and above| A+
80–89| A
70–79| B
60–69| C
50–59| D
Below 50| F

Pass/Fail status is calculated by comparing the student's marks with the passing marks defined for the examination.

⚙️ Installation and Setup

1. Clone the Repository

git clone https://github.com/PavitraVaidya/Student_Management_System.git
cd Student_Management_System

2. Create a Virtual Environment

python -m venv venv

Activate it on Windows:

venv\Scripts\activate

3. Install Dependencies

pip install -r requirements.txt

If a requirements file is not available, install Django and the additional packages used by the project.

4. Apply Database Migrations

python manage.py migrate

5. Install Ollama

Download Ollama from:

https://ollama.com/download

Download the Llama 3.2 model:

ollama pull llama3.2

Make sure Ollama is running before using the chatbot.

6. Start the Django Server

python manage.py runserver

Open the application at:

http://127.0.0.1:8000/

🔮 Future Enhancements

- Role-based dashboards for Admin, Teacher, and Student
- Database-aware AI chatbot using Retrieval-Augmented Generation (RAG)
- Secure, role-specific AI responses for attendance, fees, and results
- Attendance percentage calculation
- Automated fee receipt generation
- PDF report cards
- Excel and CSV exports
- Email notifications
- REST API integration
- Advanced analytics and visualization
- Cloud deployment

💡 What I Learned

Developing this application strengthened my understanding of:

- Django MVT architecture
- Relational database design
- Django ORM and model relationships
- Authentication and session management
- CRUD operations and backend validation
- Modular application development
- Integrating local large language models with web applications
- Debugging and handling application errors
- Connecting frontend interfaces with backend services

👩‍💻 Author

Pavitra Vaidya

Aspiring Python Developer | Python Full-Stack Development | AI/ML Enthusiast

GitHub: https://github.com/PavitraVaidya

LinkedIn: https://www.linkedin.com/in/pavitra-vaidya/

---

⭐ If you find this project interesting, consider starring the repository.

Built with Python, Django, SQLite, and Ollama.
