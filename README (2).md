# 🚪 Sagemcom RFID Access Control System

![Python](https://img.shields.io/badge/Python-3.10-blue)
![Flask](https://img.shields.io/badge/Flask-API-black)
![SQL Server](https://img.shields.io/badge/Database-SQL%20Server-red)
![ESP32](https://img.shields.io/badge/IoT-ESP32-orange)
![Arduino](https://img.shields.io/badge/Arduino-C++-green)
![License](https://img.shields.io/badge/License-Academic-lightgrey)
![Status](https://img.shields.io/badge/Status-Completed-brightgreen)

---

## 🧠 Overview

The **Sagemcom RFID Access Control System** is an IoT-based industrial solution developed as a Final Year Engineering Project (PFE) during an internship at **Sagemcom**.

It provides a secure and intelligent access control system using:
- Dual RFID readers (Entry + Workstation)
- ESP32 microcontroller
- Flask REST API backend
- Microsoft SQL Server database

---

## 🎯 Key Features

- 🔐 RFID-based authentication
- 🔁 Dual checkpoint verification
- ⏰ Shift & schedule validation
- 🧠 Role & skill-based access control
- 📊 Real-time logging system
- 💡 LCD + RGB LED feedback system
- 🛡️ Anti double-scan protection

---

## ⚙️ System Architecture

### Hardware
- ESP32 Microcontroller
- 2 × MFRC522 RFID Readers
- LCD 16x2 (I2C)
- RGB LED indicators
- WiFi module

### Software
- Python Flask API
- SQL Server Database
- SQLAlchemy ORM
- Arduino C++ firmware
- JSON communication protocol

---

## 📁 Project Structure

```
Sagemcom-RFID-Access-Control/
├── server.py
├── main.py
├── connexion.py
├── ArduinoIDE_File.txt
├── SQLQuery1.sql
├── models/
├── views/
└── example.db
```

---

## 🚀 Installation

### 1. Database Setup
Run `SQLQuery1.sql` in SQL Server to create the database.

### 2. Python Setup
```bash
python -m venv venv
venv\Scripts\activate
pip install flask sqlalchemy pandas pyodbc
```

### 3. Configuration
Update:
- connexion.py
- server.py

```python
server = "YOUR_SERVER_NAME"
database = "SAGEMCOM_DB"
```

### 4. ESP32 Setup
- Open Arduino code
- Configure WiFi credentials
- Set Flask API URL
- Upload to ESP32

### 5. Run System
```bash
python server.py
python main.py
```

---

## 🧪 Data Flow

RFID Scan → ESP32 → Flask API → SQL Server → Decision → Hardware Response

---

## 📊 Test Users

| UID | Name | Team | Role |
|-----|------|------|------|
| 63F5B428 | John Doe | Team 1 | Developer |
| C5D5963F | Jane Smith | Team 2 | Technician |
| 4A19044B | Alex Brown | Team 3 | Manager |
| ANONYME0 | Anonymous | Guest | - |

---

## 🚀 Future Improvements

- Web dashboard (React / Flask)
- Mobile application
- SMS / Email notifications
- Analytics dashboard
- QR + NFC support
- Multi-factor authentication

---

## 👨‍💻 Author

Final Year Engineering Project (PFE) – Sagemcom  
Developed by: Your Name  
2026

---

## 📄 License

Academic project – All rights reserved © 2026
