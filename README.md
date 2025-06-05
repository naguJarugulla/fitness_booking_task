# Fitness Booking API

A simple booking API for a fictional fitness studio where users can view available classes and book a spot using Flask and SQLite.

---

##Features

- View upcoming fitness classes (`GET /classes`)
- Book a class via HTML form or `POST /book` API
- View all bookings by email (`GET /bookings`)
- Timezone support (IST to user’s timezone)
- Booking validation & slot update
- HTML form for user-friendly booking
---

## 🛠 Tech Stack

- **Backend**: Python, Flask
- **Database**: SQLite (in-memory or file-based)
- **Frontend**: HTML (for `/book` route)
- **Timezone Management**: `zoneinfo`
- **Logging**: Python `logging` module

---

##  Setup Instructions

1. **Clone the repository**:

## Create and activate virtual environment:

python -m venv env
env\Scripts\activate         # For Windows
# OR
source env/bin/activate      # For Mac/Linux
## Install dependencies:

pip install -r requirements.txt
## Run the application:

python app.py
Visit: http://127.0.0.1:5000

## 📬 API Endpoints
GET /classes
Returns all upcoming classes.

Example:

curl "http://127.0.0.1:5000/classes"
curl "http://127.0.0.1:5000/classes?tz=UTC"
GET /bookings?email=<email>
Get bookings for a specific client email.

Example:
curl "http://127.0.0.1:5000/bookings?email=test@example.com"
POST /book
Books a slot in a fitness class.
Required Fields:
class_id
client_name
client_email

Example:
curl -X POST http://127.0.0.1:5000/book \
  -d "class_id=1" \
  -d "client_name=Ravi" \
  -d "client_email=ravi@example.com"
Alternatively, use the HTML form at:

http://127.0.0.1:5000/book
## 📁 Project Files
app.py – Flask application with API routes and logic

templates/booking.html – HTML form for class booking

requirements.txt – List of dependencies

fitness_database.db – SQLite DB (auto-generated)
