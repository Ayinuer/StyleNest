# StyleNest – Privacy-First Direct Marketing Platform

## Overview
StyleNest is a full-stack Django web application designed to help shop owners build direct relationships with their customers through secure subscription capture and campaign-based messaging.

This project is a Minimum Viable Product (MVP) demonstrating:
- Full-stack development with Django
- Privacy-first customer data handling
- QR-code-based subscription workflows
- Campaign management and analytics
- Clean, responsive UI design

Unlike traditional marketing platforms, StyleNest enables direct communication without relying on social media algorithms.

---

## Live Project
https://your-app-name.herokuapp.com/

---

## Features

### Shop Owner System
- Secure registration and login
- Personal dashboard
- Shop profile management

### QR Code Subscription
- Unique QR code for each shop
- Customers scan to subscribe
- Downloadable QR codes

### Privacy-Centric Design
- Phone numbers are encrypted
- No raw data exposed to shop owners
- Secure backend-controlled communication

### Subscriber Management
- Total / active / inactive tracking
- Birth month collection
- Easy unsubscribe functionality

### Campaign System
- Create campaigns
- Message templates (sale, new arrivals, etc.)
- Campaign tracking

### Analytics Dashboard
- Subscriber insights
- Campaign performance
- Chart.js visual graphs

### UI / UX
- Mobile-first design
- Premium dashboard layout
- Clean and modern interface

---

## User Flows

### Shop Owner Flow
1. Register account  
2. Login  
3. Access dashboard  
4. Generate QR code  
5. Share QR code  
6. Collect subscribers  
7. Create campaigns  
8. View analytics  

### Shopper Flow
1. Scan QR code  
2. Open subscription page  
3. Enter phone number  
4. Select birth month  
5. Submit form  
6. Receive updates  
7. Unsubscribe anytime  

---

## Tech Stack

### Backend
- Django (Python)

### Frontend
- HTML5
- CSS3 (Bootstrap + custom)
- JavaScript

### Database
- SQLite (development)
- PostgreSQL (production)

### Tools
- qrcode (QR generation)
- Chart.js (analytics)
- Django ORM

### Deployment
- Heroku

---

## Project Structure

StyleNest/
│
├── accounts/         # authentication & dashboard
├── shops/            # shop profiles & QR generation
├── subscribers/      # subscription logic
├── campaigns/        # campaigns & analytics
├── core/             # utilities
│
├── templates/        # HTML files
├── static/           # CSS, JS, images
├── media/            # QR codes & uploads
│
├── manage.py
└── requirements.txt

---

## Database Models

### ShopOwnerProfile
- Linked to Django User
- Stores shop details
- Generates QR code

### Subscriber
- Encrypted phone number
- Birth month
- Active status

### Campaign
- Title, message, template
- Status tracking
- Sent / delivered counts

---

## Security & Privacy
- Phone numbers encrypted (Fernet)
- No direct access to customer data
- Privacy-first architecture

---

## Current MVP Features
- Authentication system
- Dashboard UI
- QR code generation
- Subscription system
- Campaign creation
- Basic analytics
- Responsive design

---

## Future Improvements
- Twilio SMS integration
- WhatsApp messaging
- Scheduled campaigns
- Advanced analytics
- Customer segmentation
- REST API (DRF)
- Notifications system

---

## Deployment

### Run Locally

git clone https://github.com/your-username/stylenest.git  
cd stylenest  
python -m venv venv  
source venv/bin/activate  
pip install -r requirements.txt  
python manage.py migrate  
python manage.py runserver  

---

## Author
Ayinuer Aihaiti  
Full Stack Developer  

---

## Final Notes
StyleNest solves a real business problem:
Helping shops build direct customer relationships securely and effectively.

This project demonstrates:
- Strong backend logic
- Clean UI/UX design
- Real-world application
- Scalable architecture
