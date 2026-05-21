# ============================================================
#   MANIPAL HOSPITAL — Flask Application
#   app.py
# ============================================================
from flask import (Flask, render_template, request, redirect,
                   url_for, session, flash)
from functools import wraps
import mysql.connector
from mysql.connector import Error
from werkzeug.security import generate_password_hash, check_password_hash
from datetime import datetime
import calendar as cal_module

app = Flask(__name__)
app.secret_key = 'manipal_hospital_secret_key_2024'

# ── Database config ──────────────────────────────────────────
DB_CONFIG = {
    'host':     'localhost',
    'user':     'root',
    'password': 'mysqllakshyA1@',          # <-- SET YOUR MYSQL PASSWORD HERE
    'database': 'manipal_hospital',
    'charset':  'utf8mb4',
}

def get_db():
    try:
        return mysql.connector.connect(**DB_CONFIG)
    except Error as e:
        print(f"[DB ERROR] {e}")
        return None

def time_info():
    now = datetime.now()
    return {
        'time': now.strftime('%H:%M'),
        'date': now.strftime('%d %B %Y'),
        'day':  now.strftime('%A'),
    }

# ── Decorators ───────────────────────────────────────────────
def doctor_required(f):
    @wraps(f)
    def wrapper(*a, **kw):
        if session.get('user_type') != 'doctor':
            flash('Please login as a Doctor to access this page.', 'error')
            return redirect(url_for('login'))
        return f(*a, **kw)
    return wrapper

def patient_required(f):
    @wraps(f)
    def wrapper(*a, **kw):
        if session.get('user_type') != 'patient':
            flash('Please login as a Patient to access this page.', 'error')
            return redirect(url_for('login'))
        return f(*a, **kw)
    return wrapper

# ── HOME ─────────────────────────────────────────────────────
@app.route('/')
def index():
    return render_template('index.html', ti=time_info())

# ── GUEST ────────────────────────────────────────────────────
@app.route('/guest')
def guest():
    session['user_type'] = 'guest'
    session['user_name'] = 'Guest'
    return redirect(url_for('departments'))

# ── LOGIN ────────────────────────────────────────────────────
@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        utype    = request.form.get('user_type')
        email    = request.form.get('email', '').strip()
        password = request.form.get('password', '')

        db = get_db()
        if not db:
            flash('Database connection failed. Please try again.', 'error')
            return render_template('login.html', ti=time_info())

        cur = db.cursor(dictionary=True)
        table = 'doctors' if utype == 'doctor' else 'patients'
        cur.execute(f"SELECT * FROM {table} WHERE email = %s", (email,))
        user = cur.fetchone()
        cur.close(); db.close()

        if user and check_password_hash(user['password'], password):
            session['user_id']   = user['id']
            session['user_type'] = utype
            session['user_name'] = user['name']
            return redirect(url_for('doctor_dashboard' if utype == 'doctor'
                                    else 'patient_dashboard'))
        flash('Invalid email or password.', 'error')

    return render_template('login.html', ti=time_info())

# ── SIGNUP ───────────────────────────────────────────────────
@app.route('/signup', methods=['GET', 'POST'])
def signup():
    db = get_db()
    departments = []
    if db:
        cur = db.cursor(dictionary=True)
        cur.execute("SELECT * FROM departments ORDER BY name")
        departments = cur.fetchall()
        cur.close(); db.close()

    if request.method == 'POST':
        utype    = request.form.get('user_type')
        name     = request.form.get('name', '').strip()
        email    = request.form.get('email', '').strip()
        password = request.form.get('password', '')
        phone    = request.form.get('phone', '').strip()
        hpw      = generate_password_hash(password)

        db2 = get_db()
        if not db2:
            flash('Database error. Please try again.', 'error')
            return render_template('signup.html', ti=time_info(),
                                   departments=departments)
        cur = db2.cursor()
        try:
            if utype == 'doctor':
                dept_id = request.form.get('department_id')
                spec    = request.form.get('specialization', '').strip()
                cur.execute(
                    "INSERT INTO doctors (name,email,password,phone,department_id,specialization)"
                    " VALUES (%s,%s,%s,%s,%s,%s)",
                    (name, email, hpw, phone, dept_id, spec))
            else:
                dob   = request.form.get('dob')
                blood = request.form.get('blood_group', '')
                cur.execute(
                    "INSERT INTO patients (name,email,password,phone,dob,blood_group)"
                    " VALUES (%s,%s,%s,%s,%s,%s)",
                    (name, email, hpw, phone, dob, blood))
            db2.commit()
            flash('Account created! Please login.', 'success')
            return redirect(url_for('login'))
        except Error as e:
            db2.rollback()
            flash(f'Registration failed: {e}', 'error')
        finally:
            cur.close(); db2.close()

    return render_template('signup.html', ti=time_info(),
                           departments=departments)

# ── LOGOUT ───────────────────────────────────────────────────
@app.route('/logout')
def logout():
    session.clear()
    flash('You have been logged out.', 'info')
    return redirect(url_for('index'))

# ── DEPARTMENTS (common — guest, doctor, patient) ─────────────
@app.route('/departments')
def departments():
    db = get_db()
    depts = []
    if db:
        cur = db.cursor(dictionary=True)
        cur.execute("""
            SELECT d.*, COUNT(doc.id) AS doctor_count
            FROM departments d
            LEFT JOIN doctors doc ON doc.department_id = d.id
            GROUP BY d.id
            ORDER BY d.name
        """)
        depts = cur.fetchall()
        cur.close(); db.close()
    return render_template('departments.html', departments=depts, ti=time_info())

@app.route('/departments/<int:dept_id>')
def department_detail(dept_id):
    db = get_db()
    dept, doctors = None, []
    if db:
        cur = db.cursor(dictionary=True)
        cur.execute("SELECT * FROM departments WHERE id = %s", (dept_id,))
        dept = cur.fetchone()
        cur.execute("SELECT * FROM doctors WHERE department_id = %s ORDER BY name",
                    (dept_id,))
        doctors = cur.fetchall()
        cur.close(); db.close()
    return render_template('department_detail.html', dept=dept,
                           doctors=doctors, ti=time_info())

# ── DOCTOR DASHBOARD ─────────────────────────────────────────
@app.route('/doctor/dashboard')
@doctor_required
def doctor_dashboard():
    did = session['user_id']
    db  = get_db()
    doc, upcoming, med_count = None, 0, 0
    if db:
        cur = db.cursor(dictionary=True)
        cur.execute("""
            SELECT d.*, dept.name AS dept_name
            FROM doctors d
            LEFT JOIN departments dept ON dept.id = d.department_id
            WHERE d.id = %s
        """, (did,))
        doc = cur.fetchone()
        cur.execute("SELECT COUNT(*) AS c FROM appointments WHERE doctor_id=%s AND date>=CURDATE()", (did,))
        upcoming = cur.fetchone()['c']
        cur.execute("SELECT COUNT(*) AS c FROM medicines_issued WHERE doctor_id=%s", (did,))
        med_count = cur.fetchone()['c']
        cur.close(); db.close()
    return render_template('doctor_dashboard.html', doc=doc,
                           upcoming=upcoming, med_count=med_count, ti=time_info())

# ── DOCTOR SCHEDULE ──────────────────────────────────────────
@app.route('/doctor/schedule')
@doctor_required
def doctor_schedule():
    did = session['user_id']
    now = datetime.now()
    year, month = now.year, now.month
    month_name   = now.strftime('%B %Y')
    num_days     = cal_module.monthrange(year, month)[1]
    first_weekday= cal_module.monthrange(year, month)[0]   # 0=Mon

    db = get_db()
    events = {}
    if db:
        cur = db.cursor(dictionary=True)
        cur.execute("""
            SELECT a.*, p.name AS patient_name
            FROM appointments a
            JOIN patients p ON p.id = a.patient_id
            WHERE a.doctor_id=%s AND MONTH(a.date)=%s AND YEAR(a.date)=%s
        """, (did, month, year))
        for row in cur.fetchall():
            d = row['date'].day
            events.setdefault(d, []).append(row)
        cur.close(); db.close()

    return render_template('doctor_schedule.html',
                           month_name=month_name, num_days=num_days,
                           first_weekday=first_weekday, events=events,
                           ti=time_info())

# ── DOCTOR MEDICINES ─────────────────────────────────────────
@app.route('/doctor/medicines')
@doctor_required
def doctor_medicines():
    did = session['user_id']
    db  = get_db()
    medicines, patients = [], []
    if db:
        cur = db.cursor(dictionary=True)
        cur.execute("""
            SELECT m.*, p.name AS patient_name
            FROM medicines_issued m
            JOIN patients p ON p.id = m.patient_id
            WHERE m.doctor_id = %s
            ORDER BY m.date_issued DESC
        """, (did,))
        medicines = cur.fetchall()
        cur.execute("SELECT id, name FROM patients ORDER BY name")
        patients = cur.fetchall()
        cur.close(); db.close()
    return render_template('doctor_medicines.html', medicines=medicines,
                           patients=patients, ti=time_info())

@app.route('/doctor/medicines/add', methods=['POST'])
@doctor_required
def add_medicine():
    did   = session['user_id']
    pid   = request.form.get('patient_id')
    med   = request.form.get('medicine_name', '').strip()
    dos   = request.form.get('dosage', '').strip()
    notes = request.form.get('notes', '').strip()
    dated = request.form.get('date_issued')
    db    = get_db()
    if db:
        cur = db.cursor()
        cur.execute(
            "INSERT INTO medicines_issued(doctor_id,patient_id,medicine_name,dosage,date_issued,notes)"
            " VALUES(%s,%s,%s,%s,%s,%s)",
            (did, pid, med, dos, dated, notes))
        db.commit()
        cur.close(); db.close()
        flash('Medicine record added.', 'success')
    return redirect(url_for('doctor_medicines'))

# ── PATIENT DASHBOARD ────────────────────────────────────────
@app.route('/patient/dashboard')
@patient_required
def patient_dashboard():
    pid = session['user_id']
    db  = get_db()
    pat, total, upcoming = None, 0, 0
    if db:
        cur = db.cursor(dictionary=True)
        cur.execute("SELECT * FROM patients WHERE id=%s", (pid,))
        pat = cur.fetchone()
        cur.execute("SELECT COUNT(*) AS c FROM appointments WHERE patient_id=%s", (pid,))
        total = cur.fetchone()['c']
        cur.execute("SELECT COUNT(*) AS c FROM appointments WHERE patient_id=%s AND date>=CURDATE()", (pid,))
        upcoming = cur.fetchone()['c']
        cur.close(); db.close()
    return render_template('patient_dashboard.html', pat=pat,
                           total=total, upcoming=upcoming, ti=time_info())

# ── PATIENT APPOINTMENTS ─────────────────────────────────────
@app.route('/patient/appointments')
@patient_required
def patient_appointments():
    pid = session['user_id']
    db  = get_db()
    appointments = []
    if db:
        cur = db.cursor(dictionary=True)
        cur.execute("""
            SELECT a.*, d.name AS doctor_name, dept.name AS dept_name
            FROM appointments a
            JOIN doctors d    ON d.id   = a.doctor_id
            JOIN departments dept ON dept.id = a.department_id
            WHERE a.patient_id = %s
            ORDER BY a.date DESC
        """, (pid,))
        appointments = cur.fetchall()
        cur.close(); db.close()
    return render_template('patient_appointments.html',
                           appointments=appointments, ti=time_info())

# ── MAKE APPOINTMENT ─────────────────────────────────────────
@app.route('/patient/make-appointment', methods=['GET', 'POST'])
@patient_required
def make_appointment():
    pid = session['user_id']
    db  = get_db()
    departments, doctors = [], []
    if db:
        cur = db.cursor(dictionary=True)
        cur.execute("SELECT * FROM departments ORDER BY name")
        departments = cur.fetchall()
        cur.execute("""
            SELECT d.id, d.name, d.specialization, dept.name AS dept_name, d.department_id
            FROM doctors d
            JOIN departments dept ON dept.id = d.department_id
            ORDER BY d.name
        """)
        doctors = cur.fetchall()
        cur.close(); db.close()

    if request.method == 'POST':
        dept_id = request.form.get('department_id')
        doc_id  = request.form.get('doctor_id')
        date    = request.form.get('date')
        notes   = request.form.get('notes', '').strip()
        db2     = get_db()
        if db2:
            cur = db2.cursor()
            cur.execute(
                "INSERT INTO appointments(patient_id,doctor_id,department_id,date,notes,status)"
                " VALUES(%s,%s,%s,%s,%s,'scheduled')",
                (pid, doc_id, dept_id, date, notes))
            db2.commit()
            cur.close(); db2.close()
            flash('Appointment booked successfully!', 'success')
            return redirect(url_for('patient_appointments'))

    return render_template('make_appointment.html', departments=departments,
                           doctors=doctors, ti=time_info())

# ── RUN ──────────────────────────────────────────────────────
if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5000)
