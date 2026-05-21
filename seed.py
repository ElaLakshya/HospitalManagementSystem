# =============================================================
#  MANIPAL HOSPITAL — Database Seed Script
#  Run this ONCE to populate all tables with sample data.
#  Command: python seed.py
# =============================================================

import mysql.connector
from mysql.connector import Error
from werkzeug.security import generate_password_hash
from datetime import date, timedelta
import random

# ── Same DB config as app.py ──────────────────────────────────
DB_CONFIG = {
    'host':     'localhost',
    'user':     'root',
    'password': 'mysqllakshyA1@',           # <-- same password as in app.py
    'database': 'manipal_hospital',
    'charset':  'utf8mb4',
}

# ── All sample data ───────────────────────────────────────────

DOCTORS = [
    # (name, email, password, phone, dept_name, specialization)
    ('Arjun Mehta',       'arjun.mehta@manipal.com',     'doctor123', '9811001001', 'Cardiology',       'Interventional Cardiology'),
    ('Priya Sharma',      'priya.sharma@manipal.com',    'doctor123', '9811001002', 'Cardiology',       'Echocardiography'),
    ('Rohan Verma',       'rohan.verma@manipal.com',     'doctor123', '9811001003', 'Neurology',        'Epilepsy & Seizure Disorders'),
    ('Sneha Iyer',        'sneha.iyer@manipal.com',      'doctor123', '9811001004', 'Neurology',        'Stroke & Cerebrovascular Disease'),
    ('Karthik Nair',      'karthik.nair@manipal.com',    'doctor123', '9811001005', 'Orthopedics',      'Joint Replacement Surgery'),
    ('Deepa Pillai',      'deepa.pillai@manipal.com',    'doctor123', '9811001006', 'Orthopedics',      'Sports Medicine'),
    ('Amit Bose',         'amit.bose@manipal.com',       'doctor123', '9811001007', 'Pediatrics',       'Neonatal Care'),
    ('Ritu Singh',        'ritu.singh@manipal.com',      'doctor123', '9811001008', 'Pediatrics',       'Pediatric Pulmonology'),
    ('Vikram Rao',        'vikram.rao@manipal.com',      'doctor123', '9811001009', 'Oncology',         'Medical Oncology'),
    ('Anjali Desai',      'anjali.desai@manipal.com',    'doctor123', '9811001010', 'Oncology',         'Radiation Oncology'),
    ('Suresh Kumar',      'suresh.kumar@manipal.com',    'doctor123', '9811001011', 'Dermatology',      'Cosmetic Dermatology'),
    ('Meena Joshi',       'meena.joshi@manipal.com',     'doctor123', '9811001012', 'Dermatology',      'Pediatric Dermatology'),
    ('Rajesh Patel',      'rajesh.patel@manipal.com',    'doctor123', '9811001013', 'General Medicine',  'Diabetes & Endocrinology'),
    ('Kavitha Reddy',     'kavitha.reddy@manipal.com',   'doctor123', '9811001014', 'General Medicine',  'Infectious Diseases'),
    ('Sanjay Gupta',      'sanjay.gupta@manipal.com',    'doctor123', '9811001015', 'Emergency',        'Trauma & Critical Care'),
]

PATIENTS = [
    # (name, email, password, phone, dob, blood_group)
    ('Rahul Khanna',      'rahul.khanna@gmail.com',      'patient123', '9900001001', '1990-04-15', 'A+'),
    ('Pooja Agarwal',     'pooja.agarwal@gmail.com',     'patient123', '9900001002', '1985-08-22', 'B+'),
    ('Manish Tiwari',     'manish.tiwari@gmail.com',     'patient123', '9900001003', '1978-11-30', 'O+'),
    ('Sunita Yadav',      'sunita.yadav@gmail.com',      'patient123', '9900001004', '1995-02-10', 'AB+'),
    ('Deepak Mishra',     'deepak.mishra@gmail.com',     'patient123', '9900001005', '1982-06-05', 'A-'),
    ('Anita Srivastava',  'anita.sri@gmail.com',         'patient123', '9900001006', '1998-09-18', 'B-'),
    ('Vikas Sharma',      'vikas.sharma@gmail.com',      'patient123', '9900001007', '1975-12-25', 'O-'),
    ('Nisha Gupta',       'nisha.gupta@gmail.com',       'patient123', '9900001008', '1992-03-07', 'AB-'),
    ('Arun Pandey',       'arun.pandey@gmail.com',       'patient123', '9900001009', '1988-07-14', 'A+'),
    ('Kavya Menon',       'kavya.menon@gmail.com',       'patient123', '9900001010', '2001-01-20', 'B+'),
    ('Suresh Nambiar',    'suresh.nambiar@gmail.com',    'patient123', '9900001011', '1970-05-03', 'O+'),
    ('Preethi Balan',     'preethi.balan@gmail.com',     'patient123', '9900001012', '1994-10-11', 'A+'),
    ('Mohit Saxena',      'mohit.saxena@gmail.com',      'patient123', '9900001013', '1983-04-28', 'AB+'),
    ('Rekha Jain',        'rekha.jain@gmail.com',        'patient123', '9900001014', '1967-02-16', 'B+'),
    ('Tarun Malhotra',    'tarun.malhotra@gmail.com',    'patient123', '9900001015', '1999-08-09', 'O+'),
    ('Swati Chauhan',     'swati.chauhan@gmail.com',     'patient123', '9900001016', '1991-06-23', 'A-'),
    ('Nitesh Dubey',      'nitesh.dubey@gmail.com',      'patient123', '9900001017', '1986-11-17', 'B+'),
    ('Roshni Kapoor',     'roshni.kapoor@gmail.com',     'patient123', '9900001018', '2000-03-30', 'AB+'),
    ('Gaurav Shukla',     'gaurav.shukla@gmail.com',     'patient123', '9900001019', '1977-09-04', 'O-'),
    ('Divya Nair',        'divya.nair@gmail.com',        'patient123', '9900001020', '1993-12-12', 'A+'),
]

MEDICINES = [
    # (medicine_name, dosage, notes)
    ('Metformin',        '500mg twice daily',       'Take after meals. Monitor blood sugar weekly.'),
    ('Atorvastatin',     '10mg once at night',      'Avoid grapefruit juice. Check liver function every 3 months.'),
    ('Amlodipine',       '5mg once daily',          'Take at the same time each day. Monitor blood pressure.'),
    ('Aspirin',          '75mg once daily',         'Take with food to avoid stomach upset.'),
    ('Paracetamol',      '500mg three times daily', 'Do not exceed 4 doses in 24 hours.'),
    ('Omeprazole',       '20mg before breakfast',   'Take 30 minutes before eating.'),
    ('Azithromycin',     '500mg once daily x5days', 'Complete the full course even if feeling better.'),
    ('Cetirizine',       '10mg once at night',      'May cause drowsiness. Avoid driving.'),
    ('Ibuprofen',        '400mg three times daily', 'Take with food. Avoid if history of ulcers.'),
    ('Losartan',         '50mg once daily',         'Monitor kidney function and potassium levels.'),
    ('Levothyroxine',    '50mcg once daily',        'Take on empty stomach 30 min before breakfast.'),
    ('Pantoprazole',     '40mg once daily',         'Take before meals.'),
    ('Amoxicillin',      '500mg three times daily', 'Complete full 7-day course.'),
    ('Prednisolone',     '10mg once daily',         'Do not stop suddenly. Taper dose as directed.'),
    ('Salbutamol',       '2 puffs when needed',     'Shake inhaler before use. Rinse mouth after.'),
]

# ── Main seeding function ─────────────────────────────────────

def seed():
    try:
        db = mysql.connector.connect(**DB_CONFIG)
        cur = db.cursor(dictionary=True)
        print("\n✅ Connected to MySQL database: manipal_hospital\n")
    except Error as e:
        print(f"\n❌ Could not connect to MySQL: {e}")
        print("   Make sure MySQL is running and your password in seed.py is correct.\n")
        return

    # ── Fetch department IDs ──────────────────────────────────
    cur.execute("SELECT id, name FROM departments")
    dept_rows = cur.fetchall()
    if not dept_rows:
        print("❌ No departments found. Make sure you ran schema.sql first.")
        return
    dept_map = {d['name']: d['id'] for d in dept_rows}
    print(f"   Found {len(dept_map)} departments in database.")

    # ── Insert Doctors ────────────────────────────────────────
    print("\n── Inserting 15 Doctors ─────────────────────────────")
    doctor_ids = []
    doctor_dept_map = {}   # doctor_id → department_id
    skipped_doc = 0

    for name, email, password, phone, dept_name, spec in DOCTORS:
        dept_id = dept_map.get(dept_name)
        if not dept_id:
            print(f"   ⚠  Skipping {name} — department '{dept_name}' not found in DB.")
            skipped_doc += 1
            continue
        hashed = generate_password_hash(password)
        try:
            cur.execute(
                "INSERT INTO doctors (name, email, password, phone, department_id, specialization)"
                " VALUES (%s, %s, %s, %s, %s, %s)",
                (name, email, hashed, phone, dept_id, spec)
            )
            db.commit()
            doc_id = cur.lastrowid
            doctor_ids.append(doc_id)
            doctor_dept_map[doc_id] = dept_id
            print(f"   ✔  Dr. {name} ({dept_name})")
        except Error as e:
            db.rollback()
            if '1062' in str(e):
                print(f"   ⚠  Skipped {name} — email already exists.")
                # still fetch their id so appointments can reference them
                cur.execute("SELECT id, department_id FROM doctors WHERE email=%s", (email,))
                existing = cur.fetchone()
                if existing:
                    doctor_ids.append(existing['id'])
                    doctor_dept_map[existing['id']] = existing['department_id']
            else:
                print(f"   ❌ Error inserting {name}: {e}")

    # ── Insert Patients ───────────────────────────────────────
    print("\n── Inserting 20 Patients ────────────────────────────")
    patient_ids = []
    skipped_pat = 0

    for name, email, password, phone, dob, blood_group in PATIENTS:
        hashed = generate_password_hash(password)
        try:
            cur.execute(
                "INSERT INTO patients (name, email, password, phone, dob, blood_group)"
                " VALUES (%s, %s, %s, %s, %s, %s)",
                (name, email, hashed, phone, dob, blood_group)
            )
            db.commit()
            patient_ids.append(cur.lastrowid)
            print(f"   ✔  {name}  ({blood_group})")
        except Error as e:
            db.rollback()
            if '1062' in str(e):
                print(f"   ⚠  Skipped {name} — email already exists.")
                cur.execute("SELECT id FROM patients WHERE email=%s", (email,))
                existing = cur.fetchone()
                if existing:
                    patient_ids.append(existing['id'])
            else:
                print(f"   ❌ Error inserting {name}: {e}")

    if not doctor_ids or not patient_ids:
        print("\n❌ Not enough doctors or patients to create appointments. Exiting.")
        cur.close(); db.close()
        return

    # ── Insert Appointments ───────────────────────────────────
    print("\n── Inserting Appointments ───────────────────────────")
    today     = date.today()
    statuses  = ['scheduled', 'completed', 'completed', 'completed', 'cancelled']
    appt_count = 0

    # Give every patient at least 1-3 appointments
    for pat_id in patient_ids:
        num_appts = random.randint(1, 3)
        for _ in range(num_appts):
            doc_id  = random.choice(doctor_ids)
            dept_id = doctor_dept_map[doc_id]
            # Past dates for completed, future for scheduled
            offset  = random.randint(-90, 30)
            appt_date = today + timedelta(days=offset)
            status  = 'scheduled' if offset > 0 else random.choice(statuses)
            notes   = random.choice([
                'Regular checkup', 'Follow-up visit', 'First consultation',
                'Post-surgery review', 'Medication review', 'Test results discussion',
                'Routine screening', 'Second opinion', ''
            ])
            try:
                cur.execute(
                    "INSERT INTO appointments"
                    " (patient_id, doctor_id, department_id, date, status, notes)"
                    " VALUES (%s, %s, %s, %s, %s, %s)",
                    (pat_id, doc_id, dept_id, appt_date, status, notes)
                )
                db.commit()
                appt_count += 1
            except Error as e:
                db.rollback()
                print(f"   ❌ Appointment error: {e}")

    print(f"   ✔  {appt_count} appointments created across {len(patient_ids)} patients.")

    # ── Insert Medicines Issued ───────────────────────────────
    print("\n── Inserting Medicine Records ───────────────────────")
    med_count = 0

    # Each doctor issues 2-4 medicines to random patients
    for doc_id in doctor_ids:
        num_meds = random.randint(2, 4)
        chosen   = random.sample(MEDICINES, min(num_meds, len(MEDICINES)))
        for med_name, dosage, notes in chosen:
            pat_id    = random.choice(patient_ids)
            offset    = random.randint(-60, -1)
            med_date  = today + timedelta(days=offset)
            try:
                cur.execute(
                    "INSERT INTO medicines_issued"
                    " (doctor_id, patient_id, medicine_name, dosage, date_issued, notes)"
                    " VALUES (%s, %s, %s, %s, %s, %s)",
                    (doc_id, pat_id, med_name, dosage, med_date, notes)
                )
                db.commit()
                med_count += 1
            except Error as e:
                db.rollback()
                print(f"   ❌ Medicine error: {e}")

    print(f"   ✔  {med_count} medicine records created across {len(doctor_ids)} doctors.")

    cur.close()
    db.close()

    # ── Summary ───────────────────────────────────────────────
    print("\n" + "="*52)
    print("  ✅  SEEDING COMPLETE — Summary")
    print("="*52)
    print(f"  Doctors inserted   : {len(doctor_ids)}")
    print(f"  Patients inserted  : {len(patient_ids)}")
    print(f"  Appointments created: {appt_count}")
    print(f"  Medicine records   : {med_count}")
    print("="*52)
    print("\n  Login credentials for ALL doctors  → password: doctor123")
    print("  Login credentials for ALL patients → password: patient123")
    print("\n  Example doctor login:")
    print("    Email    : arjun.mehta@manipal.com")
    print("    Password : doctor123")
    print("\n  Example patient login:")
    print("    Email    : rahul.khanna@gmail.com")
    print("    Password : patient123")
    print()

if __name__ == '__main__':
    seed()