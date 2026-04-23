# 🌱 Crop Tracker System

## 📌 Overview
Crop Tracker System is a Django-based web application used to manage agricultural fields, crops, and agents. It helps track the progress of crops from planting to harvest.

---

## 🚀 Features

### 👨‍💼 Admin
- Create and manage fields
- Assign agents to fields
- View all field records
- Track crop progress (Planted, Growing, Ready, Harvested)

### 👨‍🌾 Agent
- View only assigned fields
- Update field progress
- Access personal dashboard

---

## 🧠 System Description

The system uses role-based access:
- **Admin** has full control of the system.
- **Agents** only see and manage their assigned fields.

Each field contains:
- Name
- Crop type
- Planting date
- Current growth stage
- Assigned agent

---

## 🛠️ Tech Stack
- Django (Python)
- PostgreSQL / MySQL
- HTML, CSS, Bootstrap
- JavaScript

---

## ⚙️ Installation

```bash
git clone <your-repo-link>
cd crop-tracker-system
pip install -r requirements.txt
python manage.py migrate
python manage.py runserver