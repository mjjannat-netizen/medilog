from flask import Flask, render_template, request, redirect, url_for
import pymysql

app = Flask(__name__)

def get_db():
    return pymysql.connect(
        host='localhost',
        user='root',
        password='#MJsq21L#',
        database='medilog'
    )

@app.route('/')
def index():
    return render_template('index.html')

# ========== PATIENTS ==========
@app.route('/patients')
def patients():
    db = get_db()
    cursor = db.cursor()
    cursor.execute("SELECT * FROM patients")
    data = cursor.fetchall()
    db.close()
    return render_template('patients.html', patients=data)

@app.route('/patients/add', methods=['GET', 'POST'])
def add_patient():
    if request.method == 'POST':
        name = request.form['name']
        age = request.form['age']
        gender = request.form['gender']
        phone = request.form['phone']
        address = request.form['address']
        db = get_db()
        cursor = db.cursor()
        cursor.execute("INSERT INTO patients (name, age, gender, phone, address) VALUES (%s, %s, %s, %s, %s)",
                      (name, age, gender, phone, address))
        db.commit()
        db.close()
        return redirect(url_for('patients'))
    return render_template('add_patient.html')

@app.route('/patients/delete/<int:id>')
def delete_patient(id):
    db = get_db()
    cursor = db.cursor()
    cursor.execute("DELETE FROM patients WHERE patient_id = %s", (id,))
    db.commit()
    db.close()
    return redirect(url_for('patients'))

# ========== DOCTORS ==========
@app.route('/doctors')
def doctors():
    db = get_db()
    cursor = db.cursor()
    cursor.execute("SELECT * FROM doctors")
    data = cursor.fetchall()
    db.close()
    return render_template('doctors.html', doctors=data)

@app.route('/doctors/add', methods=['GET', 'POST'])
def add_doctor():
    if request.method == 'POST':
        name = request.form['name']
        specialization = request.form['specialization']
        phone = request.form['phone']
        db = get_db()
        cursor = db.cursor()
        cursor.execute("INSERT INTO doctors (name, specialization, phone) VALUES (%s, %s, %s)",
                      (name, specialization, phone))
        db.commit()
        db.close()
        return redirect(url_for('doctors'))
    return render_template('add_doctor.html')

@app.route('/doctors/delete/<int:id>')
def delete_doctor(id):
    db = get_db()
    cursor = db.cursor()
    cursor.execute("DELETE FROM doctors WHERE doctor_id = %s", (id,))
    db.commit()
    db.close()
    return redirect(url_for('doctors'))

# ========== APPOINTMENTS ==========
@app.route('/appointments')
def appointments():
    db = get_db()
    cursor = db.cursor()
    cursor.execute("""
        SELECT a.appointment_id, p.name, d.name, a.appointment_date, a.status
        FROM appointments a
        JOIN patients p ON a.patient_id = p.patient_id
        JOIN doctors d ON a.doctor_id = d.doctor_id
    """)
    data = cursor.fetchall()
    db.close()
    return render_template('appointments.html', appointments=data)

@app.route('/appointments/add', methods=['GET', 'POST'])
def add_appointment():
    db = get_db()
    cursor = db.cursor()
    cursor.execute("SELECT patient_id, name FROM patients")
    patients = cursor.fetchall()
    cursor.execute("SELECT doctor_id, name FROM doctors")
    doctors = cursor.fetchall()
    if request.method == 'POST':
        patient_id = request.form['patient_id']
        doctor_id = request.form['doctor_id']
        date = request.form['date']
        status = request.form['status']
        cursor.execute("INSERT INTO appointments (patient_id, doctor_id, appointment_date, status) VALUES (%s, %s, %s, %s)",
                      (patient_id, doctor_id, date, status))
        db.commit()
        db.close()
        return redirect(url_for('appointments'))
    db.close()
    return render_template('add_appointment.html', patients=patients, doctors=doctors)

@app.route('/appointments/delete/<int:id>')
def delete_appointment(id):
    db = get_db()
    cursor = db.cursor()
    cursor.execute("DELETE FROM appointments WHERE appointment_id = %s", (id,))
    db.commit()
    db.close()
    return redirect(url_for('appointments'))

# ========== PATIENT HISTORY VIEW ==========
@app.route('/history')
def history():
    db = get_db()
    cursor = db.cursor()
    cursor.execute("SELECT * FROM patient_appointment_view")
    data = cursor.fetchall()
    db.close()
    return render_template('history.html', records=data)

if __name__ == '__main__':
    app.run(debug=True)