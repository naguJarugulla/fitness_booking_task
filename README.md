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

bash
git clone https://github.com/naguJarugulla/fitness_booking_task.git
cd fitness_booking_task

##Create and activate virtual environment:
python -m venv env
env\Scripts\activate  # For Windows
# OR
source env/bin/activate  # For Mac/Linux
#===============Install dependencies:
pip install -r requirements.txt

#==============Run the application:
python app.py
#==========================API Endpoints
---GET /classes
Description: Returns all upcoming classes.
curl "http://127.0.0.1:5000/classes"

or
curl "http://127.0.0.1:5000/classes?tz=UTC"

----GET /bookings?email=<email>
Description: Get bookings for a specific client email.
Sample cURL:
curl "http://127.0.0.1:5000/bookings?email=test@example.com"
----POST /book
Description: Books a slot in a fitness class.
Required Fields:
class_id
client_name
client_email
Sample cURL
curl -X POST http://127.0.0.1:5000/book ^
  -d "class_id=1" ^
  -d "client_name=Ravi" ^
  -d "client_email=ravi@example.com"

Project Files
app.py – Flask application with routes and logic
templates/booking.html – HTML form for class booking
requirements.txt – List of dependencies
fitness_database.db – SQLite DB (auto-generated)


