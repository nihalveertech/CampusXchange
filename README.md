# CampusXchange
CampusXchange is a comprehensive, full-stack inspired web application developed to establish a unified and intelligent digital ecosystem within a college campus.
# 🎓 CampusXchange

## 📌 Overview

**CampusXchange** is a full-stack web application designed to create a centralized digital ecosystem within a campus. The platform enables students to exchange resources, interact with peers, and manage campus-related activities efficiently.

Built using a structured backend framework and modular frontend templates, the application demonstrates scalable architecture and clean project organization suitable for real-world deployment.

---

## 🎯 Objective

The primary goal of this project is to:

* Enable seamless **resource exchange** among students
* Provide a **centralized communication platform**
* Demonstrate **full-stack development skills** with structured architecture

---

## ✨ Key Features

* 🔄 Student-to-student resource exchange system
* 👥 User authentication (Login / Password Reset)
* 📊 Dashboard with analytics (Doughnut Chart Visualization)
* 📢 Organized content & navigation system
* 🛒 Exchange / Sell functionality
* 📱 Responsive UI using template-based rendering

---

## 🛠️ Tech Stack

### 🔹 Backend

* Python 3.12
* Django Framework

### 🔹 Frontend

* HTML5
* CSS3
* JavaScript

### 🔹 Database

* SQLite3

---

## 📁 Project Structure

```id="struct1"
singhnihal/                  # Root Directory
│
├── .venv/                   # Virtual Environment (ignored in Git)
│
├── technihal/               # Main Application Module
│   ├── items/               # App for item management
│   ├── nihalhome/           # Core app logic
│   ├── static/              # Static files (CSS, JS, images)
│   ├── technihal/           # Project configuration files
│   ├── templates/           # HTML Templates
│   │   ├── base.html
│   │   ├── buy.html
│   │   ├── dashboard.html
│   │   ├── doughnut.html
│   │   ├── exchange.html
│   │   ├── index.html
│   │   ├── item_.html
│   │   ├── login.html
│   │   ├── password_reset.html
│   │   └── sell.html
│   │
│   ├── db.sqlite3          # Database file
│   ├── manage.py           # Django management script
│   ├── main.py             # Entry point (if used)
│   └── .gitignore          # Git ignore rules
│
└── External Libraries (auto-generated)
    ├── Python 3.12
    ├── site-packages
    ├── DLLs, Lib, etc.
    └── IDE-related files (ignored)
```

---

## ⚙️ Installation & Setup

### 1️⃣ Clone the Repository

```id="setup1"
git clone https://github.com/your-username/CampusXchange.git
cd CampusXchange
```

---

### 2️⃣ Create Virtual Environment

```id="setup2"
python -m venv .venv
```

---

### 3️⃣ Activate Virtual Environment

**Windows:**

```id="setup3"
.venv\Scripts\activate
```

---

### 4️⃣ Install Dependencies

```id="setup4"
pip install -r requirements.txt
```

*(If requirements.txt is not present, install Django manually)*

```id="setup5"
pip install django
```

---

### 5️⃣ Run Migrations

```id="setup6"
python manage.py migrate
```

---

### 6️⃣ Run Development Server

```id="setup7"
python manage.py runserver
```

---

### 7️⃣ Open in Browser

```id="setup8"
http://127.0.0.1:8000/
```

---

## 🔐 Authentication Features

* User Login System
* Password Reset Functionality
* Session Handling

---

## 📊 Dashboard & Visualization

* Integrated **doughnut chart UI**
* Displays user-related insights and activity overview

---

## 🚀 Future Enhancements

* 🔐 Advanced authentication (JWT / OAuth)
* 💬 Real-time chat system
* 📱 Mobile responsive optimization
* ☁️ Deployment on cloud (AWS / Render / Vercel)
* 🧠 AI-based recommendation system

---

## ⚠️ Notes

* `.venv/`, external libraries, and IDE files are excluded using `.gitignore`
* SQLite is used for development; production DB can be upgraded to PostgreSQL/MySQL

---

## 👨‍💻 Author

**Nihalveer Singh**
Second-Year Engineering Student
Aspiring Software Developer

---

## ⭐ Contribution & Support

If you find this project useful, consider giving it a ⭐ on GitHub. Contributions and suggestions are welcome.

---
