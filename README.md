# 🗓️ Automated Timetable Generator

🎓 A Final Year Project by **TEAM GCOERC - Group 32**

> A smart, conflict-free, and automated class timetable generation system using Django and SQLite, complete with user roles, CSV uploads, and per-class/faculty views.

---

## 🚀 Overview

The **Automated Timetable Generator** is a full-stack web application built to eliminate the hassle of manual timetable creation for colleges and academic institutions. It efficiently generates optimized, conflict-free timetables for multiple academic years and divisions. The project supports timetables for Second Year (SE), Third Year (TE), and Final Year (BE) students, along with faculty-wise schedules — all managed through a simple and intuitive interface.

---

## ✨ Key Features

- 🔐 Secure login/authentication for admin  
- 📤 Upload teacher-subject data via CSV files  
- ⚙️ Automated generation of conflict-free timetables  
- 👨‍🏫 Faculty-wise and class-wise timetable views  
- 📚 Separate timetable generation for SE, TE, and BE divisions  
- 🖨️ Printable and user-friendly timetable layouts  
- ⚡ Lightweight frontend built with vanilla HTML/CSS/JavaScript  
- 🧾 Timetable viewing and update interface  
- 🛡️ Error handling for invalid or duplicate inputs  

---

## 🛠️ Tech Stack

| Layer       | Technology               |
|-------------|---------------------------|
| Frontend    | HTML5, CSS3, JavaScript   |
| Backend     | Django (Python)           |
| Database    | SQLite                    |
| Others      | CSV Uploads, Django Admin |

---

## 📁 Project Structure

├── app/
│ ├── migrations/
│ ├── templates/
│ ├── static/
│ ├── admin.py
│ ├── models.py
│ ├── views.py
│ └── urls.py
│
├── time_table/ # Django project settings
├── dataset/ # Input CSV files
├── db.sqlite3 # Database
├── manage.py # Django CLI
└── README.md


---


## 📝 How to Use

### 🔧 Prerequisites

- Python 3.x  
- pip (Python package manager)  

### ⚙️ Setup Instructions

bash
## Clone the repository
git clone https://github.com/AkshayJ9/Automated-Timetable-Generator.git
cd Automated-Timetable-Generator

## Create a virtual environment
python -m venv venv
venv\Scripts\activate      # On Windows

## Install dependencies
pip install -r requirements.txt

## Apply database migrations
python manage.py makemigrations
python manage.py migrate

## Start the development server
python manage.py runserver



## 👨‍💻 Authors

### 🧑‍💻 Akshay Jadhav  
📧 Email: [akshayj.contact@gmail.com](mailto:akshayj.contact@gmail.com)  
📱 Phone: +91-7249471395  
🔗 [LinkedIn](https://www.linkedin.com/in/akshaykjadhav/) • [GitHub](https://github.com/AkshayJ9)

---

### 👩‍💻 Sakshi Wani  
📧 Email: [sakshiwani2404@gmail.com](mailto:sakshiwani2404@gmail.com)

---

### 👩‍💻 Rupali Chavan  
📧 Email: [rupalichavan0009@gmail.com](mailto:rupalichavan0009@gmail.com)

---

### 🧑‍💻 Parag Iwanate  
📧 Email: [iwanateparag@gmail.com](mailto:iwanateparag@gmail.com)

