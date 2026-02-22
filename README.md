📌 Description

This is a modern web app for task management and study planning. Users can add tasks with deadlines and priorities, mark them as completed, filter by status, and track productivity statistics.
Frontend: HTML + CSS (with dark theme)
Backend: Python + Flask
Database: SQLite
Authorization: Registration and login via Flask-Login

Functionality
✅ User registration and authorization
✅ Add/remove tasks
✅ Mark tasks as completed
✅ Filters: All / Active / Completed
✅ Deadline and priority (Low / Medium / High)
✅ Productivity statistics
✅ Dark theme with a toggle button

Installation:
1. Clone the repository:
git clone https://github.com/<username>/To_Do_App.git
cd To_Do_App

2. Create a virtual environment and install dependencies:
python3 -m venv venv
source venv/bin/activate      # Linux / MacOS
venv\Scripts\activate         # Windows
pip install -r requirements.txt

3. Launch the application: python app.py

4. Open in browser: http://127.0.0.1:5000/

Project structure:
To_Do_App/
├── app.py
├── requirements.txt
├── templates/
│ ├── base.html
│ ├── login.html
│ ├── register.html
│ ├── dashboard.html
│ └── stats.html
├── static/
│ └── style.css
├── .gitignore
└── venv/ (not committed)

Screenshots:
<img width="1440" height="821" alt="Dashboard" src="https://github.com/user-attachments/assets/82b943f2-b066-49c6-8eb6-296c9f1b0915" />
<img width="1440" height="820" alt="AddTask1" src="https://github.com/user-attachments/assets/6aad74e5-f119-4a8f-9eb9-f4833ccea0d0" />
<img width="1440" height="820" alt="AddTask2" src="https://github.com/user-attachments/assets/55b123a1-f2ff-4f40-ace5-2d068c4c45fe" />
<img width="1439" height="822" alt="Stats" src="https://github.com/user-attachments/assets/3743c418-8c14-48ca-8fa2-826a4a22c0b1" />
<img width="1440" height="820" alt="Dark mode" src="https://github.com/user-attachments/assets/a071d02b-5df7-44c9-8d22-00ddab05a6c9" />

Used:
Python 3.14
Flask
Flask-Login
Flask-SQLAlchemy
SQLite
HTML/CSS

Notes
The database.db is created automatically on first launch.
This database is not included in the repository for security reasons.

   
