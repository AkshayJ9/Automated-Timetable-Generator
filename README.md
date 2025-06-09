# 🗓️ Automated Timetable Generator

![Python](https://img.shields.io/badge/Backend-Django-green?logo=django)
![HTML](https://img.shields.io/badge/Frontend-HTML%2FCSS%2FJS-blue)
![Database](https://img.shields.io/badge/Database-SQLite-lightgrey?logo=sqlite)
![Status](https://img.shields.io/badge/Project-Completed-brightgreen)
![License](https://img.shields.io/badge/License-MIT-yellow)

🎓 A Final Year Project by Akshay Jadhav

> A smart, conflict-free, and automated class timetable generation system using Django and SQLite, complete with user roles, CSV uploads, and per-class/faculty views.

---

## 🚀 Overview

The **Automated Timetable Generator** is a full-stack web application built to eliminate the hassle of manual timetable creation for colleges and academic institutions. It efficiently handles timetable generation for multiple years and divisions, avoiding all faculty and room conflicts. The project supports second-year, third-year, and final-year students, along with faculty-wise schedule generation.

---

## 🧠 Project Flow

![Project Flow](./406547e0-073f-4635-ba4e-8bf8d7db5781.png)

---

## ✨ Key Features

- 🔐 **Secure Login/Authentication** for Admin
- 📤 conflict free containing teacher and subject data
- ⚙️ Auto-generation of **conflict-free** academic timetables
- 👨‍🏫 **Faculty-wise** and **Class-wise** schedule views
- 📚 Separate timetable creation for **SE / TE / BE divisions**
- 📄 Print-friendly HTML timetable layouts
- ⚡ Simple, responsive UI using vanilla HTML/CSS/JS
- 🧾 Timetable viewing and update interface
- 🛡️ Error handling for invalid uploads and conflicting data

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

### 🚀 Setup Instructions

bash
# Clone the repo
git clone https://github.com/AkshayJ9/Automated-Timetable-Generator.git
cd Automated-Timetable-Generator

# Create virtual environment
python -m venv venv
venv\Scripts\activate    # For Windows

# Install dependencies
pip install -r requirements.txt

# Migrate database
python manage.py makemigrations
python manage.py migrate

# Run the server
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

