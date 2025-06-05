from flask import Flask, request, render_template
from datetime import datetime
from zoneinfo import ZoneInfo
import sqlite3
import logging
import os

app = Flask(__name__)

logging.basicConfig(level=logging.INFO)

# Create SQLite Database if not exists the tables classes and booking
def init_db():
    connection = sqlite3.connect('fitness_database.db')
    cursor = connection.cursor()

    cursor.execute('''
        CREATE TABLE IF NOT EXISTS classes(
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            class_name TEXT NOT NULL,
            date_time TEXT NOT NULL,
            instructor TEXT NOT NULL,
            available_slots INTEGER NOT NULL
        )
    ''')

    cursor.execute('''
        CREATE TABLE IF NOT EXISTS bookings(
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            class_id INTEGER NOT NULL,
            client_name TEXT NOT NULL,
            client_email TEXT NOT NULL,
            FOREIGN KEY(class_id) REFERENCES classes(id)
        )
    ''')

    connection.commit()
    connection.close()

#=========================== Fill default classes data if table is empty
def fill_the_classes():
    connection = sqlite3.connect('fitness_database.db')
    cursor = connection.cursor()
    cursor.execute('SELECT COUNT(*) FROM classes')
    if cursor.fetchone()[0] == 0:
        classes = [
            ('Yoga', '2025-06-07T07:00:00+05:30', 'Ramya', 20),
            ('Zumba', '2025-06-08T08:30:00+05:30', 'Raju', 5),
            ('HIIT', '2025-06-09T06:30:00+05:30', 'Rani', 20)
        ]
        cursor.executemany('INSERT INTO classes (class_name, date_time, instructor, available_slots) VALUES (?, ?, ?, ?)', classes)
        connection.commit()
    connection.close()



#Returns a list of all upcoming fitness classes (name, date/time, instructor, available slots)

@app.route('/classes', methods=['GET'])
def get_classes():
    user_tz = request.args.get('tz', 'Asia/Kolkata')
    try:
        zone = ZoneInfo(user_tz)
    except Exception:
        zone = ZoneInfo('Asia/Kolkata')

    connection = sqlite3.connect('fitness_database.db')
    cursor = connection.cursor()
    cursor.execute("SELECT * FROM classes")
    rows = cursor.fetchall()
    connection.close()

    result = []
    for row in rows:
        ist_time = datetime.fromisoformat(row[2])
        local_time = ist_time.astimezone(zone)
        result.append({
            "id": row[0],
            "name": row[1],
            "datetime": local_time.strftime('%Y-%m-%d %H:%M:%S'),
            "instructor": row[3],
            "available_slots": row[4]
        })
    return {"classes": result}


#=====================================================
# Accepts a booking request (class_id, client_name, client_email) Validates if slots are available, and reduces available slots upon successful booking



@app.route('/book', methods=['GET', 'POST'])
def book_class():
    connection = sqlite3.connect('fitness_database.db')
    cursor = connection.cursor()

    if request.method == 'POST':
        class_id = request.form.get('class_id')
        name = request.form.get('client_name')
        email = request.form.get('client_email')

        if not all([class_id, name, email]):
            connection.close()
            return "Missing required fields", 400

        cursor.execute("SELECT class_name, date_time, instructor, available_slots FROM classes WHERE id = ?", (class_id,))
        result = cursor.fetchone()

        if not result:
            connection.close()
            return "Class not found", 404
        if result[3] <= 0:
            connection.close()
            return "No slots available", 400

        cursor.execute(
            "INSERT INTO bookings (class_id, client_name, client_email) VALUES (?, ?, ?)",
            (class_id, name, email)
        )
        cursor.execute("UPDATE classes SET available_slots = available_slots - 1 WHERE id = ?", (class_id,))
        connection.commit()
        connection.close()

        logging.info(f"Booking successful for {name} ({email}) in class {class_id}")

        return f"""
        <h2>Booking Successful!</h2>
        <p><strong>Class:</strong> {result[0]}</p>
        <p><strong>Date & Time:</strong> {result[1]}</p>
        <p><strong>Instructor:</strong> {result[2]}</p>
        <p><strong>Booked for:</strong> {name}</p>
        """
    else:
        cursor.execute("SELECT id, class_name FROM classes")
        classes = cursor.fetchall()
        connection.close()
        return render_template('booking.html', classes=classes)



#=============================================================================
#Returns all bookings made by a specific email address


@app.route('/bookings', methods=['GET'])
def get_bookings():
    email = request.args.get('email')
    if not email:
        return {"error": "Email is required"}, 400

    connection = sqlite3.connect('fitness_database.db')
    cursor = connection.cursor()
    cursor.execute('''
        SELECT c.class_name, c.date_time, c.instructor
        FROM bookings b JOIN classes c ON b.class_id = c.id
        WHERE b.client_email = ?
    ''', (email,))
    rows = cursor.fetchall()
    connection.close()

    bookings = []
    for row in rows:
        bookings.append({
            "class_name": row[0],
            "datetime": row[1],
            "instructor": row[2]
        })

    return {"bookings": bookings}

if __name__ == '__main__':
    init_db()
    fill_the_classes()
    app.run(debug=True)
