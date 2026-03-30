# 📌 Digital Queue System for Real Places

## 🚀 Project Overview

This project is a **Digital Queue Management System** designed to replace physical waiting lines with a **virtual, real-time queue system**.

Users can join queues remotely, track their position live, and receive notifications when it's their turn.

---

## 🎯 Objectives

* Eliminate physical waiting lines
* Provide real-time queue updates
* Improve service efficiency
* Enable remote queue participation

---

## 🛠️ Tech Stack

### Backend

* Django
* Django REST Framework (DRF)
* Django Channels (WebSockets - Phase 2)
* Celery + Redis (Background tasks - Phase 3)

### Frontend

* React

### Other Integrations

* Twilio API (SMS notifications)
* Geopy (Geo-fencing)

---

## ⚙️ Core Features

### ✅ Phase 1 (Core System)

* Join queue
* View queue status
* Admin: call next / skip
* Basic wait-time estimation

### ⚡ Phase 2

* Real-time updates (WebSockets)

### 📩 Phase 3

* SMS notifications

### 📍 Phase 4

* Geo-fencing (prevent ghost queuing)

### 🧠 Phase 5

* Smart routing (priority services)
* Snooze/delay management
* Improved wait-time prediction

---

## 🧩 System Features (Detailed)

### 1. Real-Time Queue Updates

* Live position tracking
* No page refresh required
* Powered by WebSockets

### 2. Automated Notifications

* SMS alerts for queue updates
* Reminder when turn is near

### 3. Admin Dashboard

* Call next customer
* Skip/no-show handling
* Transfer customers between services

### 4. Service Categorization

* Multiple services with priority levels
* Smart queue routing

### 5. Predictive Wait-Time Engine

Formula:
WaitTime = PeopleInFront × AverageServiceTime

* Uses last served customers
* Dynamically updates estimates

### 6. Geo-Fencing

* Restricts queue access based on location
* Prevents fake/remote queue abuse

### 7. Snooze Feature

* User can delay their turn once
* Managed using priority/position logic

### 8. Multi-Channel Check-In

* QR code entry
* Web-based joining
* Kiosk for walk-ins

---

## 📂 Project Structure

```
queue-system/
│
├── backend/
│   ├── configuration/
│   ├── apps/
│   │   ├── users/
│   │   ├── queues/
│   │   ├── services/
│   │   ├── notifications/
│   │   └── analytics/
│   │
│   └── core/
│
└── README.md
```

---

## 🔌 API Development Plan

### Phase 1 APIs

* POST /api/queue/join/
* GET /api/queue/
* GET /api/queue/<id>/
* POST /api/admin/call-next/
* POST /api/admin/skip/

---

## 👥 Team Workflow

* Backend team builds APIs first
* Frontend team consumes APIs
* API contract must be shared (Postman/Swagger)

---

## 🚀 Getting Started (Backend)

```bash
# create virtual environment
python -m venv venv

# activate
venv\Scripts\activate  # Windows

# install dependencies
pip install -r requirements.txt

# run migrations
python manage.py migrate

# start server
python manage.py runserver
```

---

## .env file setup
```.env
INFOBIP_BASE_URL=https://your_unique_url.api.infobip.com
INFOBIP_API_KEY=your_secret_key_here
```

## 📌 Future Improvements

* AI-based wait-time prediction
* Analytics dashboard
* Multi-location support
* Mobile app integration

---


