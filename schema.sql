-- ============================================================
--  Manipal Hospital Management System -- Database Schema
-- ============================================================

CREATE DATABASE IF NOT EXISTS manipal_hospital
    CHARACTER SET utf8mb4
    COLLATE utf8mb4_unicode_ci;

USE manipal_hospital;

-- -------------------------------------------------------
--  DOCTORS
-- -------------------------------------------------------
CREATE TABLE IF NOT EXISTS doctors (
    id             INT AUTO_INCREMENT PRIMARY KEY,
    name           VARCHAR(120)  NOT NULL,
    email          VARCHAR(180)  UNIQUE NOT NULL,
    password       VARCHAR(255)  NOT NULL,
    phone          VARCHAR(20),
    department     VARCHAR(100),
    specialization VARCHAR(120),
    created_at     TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- -------------------------------------------------------
--  PATIENTS
-- -------------------------------------------------------
CREATE TABLE IF NOT EXISTS patients (
    id          INT AUTO_INCREMENT PRIMARY KEY,
    name        VARCHAR(120)  NOT NULL,
    email       VARCHAR(180)  UNIQUE NOT NULL,
    password    VARCHAR(255)  NOT NULL,
    phone       VARCHAR(20),
    dob         DATE,
    blood_group VARCHAR(5),
    created_at  TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- -------------------------------------------------------
--  APPOINTMENTS
-- -------------------------------------------------------
CREATE TABLE IF NOT EXISTS appointments (
    id               INT AUTO_INCREMENT PRIMARY KEY,
    patient_id       INT  NOT NULL,
    doctor_id        INT  NOT NULL,
    department       VARCHAR(100),
    appointment_date DATE NOT NULL,
    status           VARCHAR(50) DEFAULT 'scheduled',
    created_at       TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (patient_id) REFERENCES patients(id) ON DELETE CASCADE,
    FOREIGN KEY (doctor_id)  REFERENCES doctors(id)  ON DELETE CASCADE
);

-- -------------------------------------------------------
--  MEDICINES
-- -------------------------------------------------------
CREATE TABLE IF NOT EXISTS medicines (
    id            INT AUTO_INCREMENT PRIMARY KEY,
    doctor_id     INT  NOT NULL,
    patient_id    INT  NOT NULL,
    medicine_name VARCHAR(180) NOT NULL,
    dosage        VARCHAR(180),
    issued_date   DATE,
    notes         TEXT,
    created_at    TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (doctor_id)  REFERENCES doctors(id)  ON DELETE CASCADE,
    FOREIGN KEY (patient_id) REFERENCES patients(id) ON DELETE CASCADE
);

-- -------------------------------------------------------
--  DOCTOR SCHEDULES
-- -------------------------------------------------------
CREATE TABLE IF NOT EXISTS schedules (
    id            INT AUTO_INCREMENT PRIMARY KEY,
    doctor_id     INT  NOT NULL,
    schedule_date DATE NOT NULL,
    time_start    TIME,
    time_end      TIME,
    notes         VARCHAR(500),
    created_at    TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (doctor_id) REFERENCES doctors(id) ON DELETE CASCADE
);

-- -------------------------------------------------------
--  SAMPLE DATA
-- -------------------------------------------------------
INSERT INTO doctors (name, email, password, phone, department, specialization) VALUES
  ('Arjun Sharma',   'arjun@manipal.com',  'doctor123', '9876541001', 'Cardiology',       'Interventional Cardiologist'),
  ('Priya Menon',    'priya@manipal.com',  'doctor123', '9876541002', 'Neurology',        'Consultant Neurologist'),
  ('Ravi Kumar',     'ravi@manipal.com',   'doctor123', '9876541003', 'Orthopedics',      'Orthopedic Surgeon'),
  ('Sunita Rao',     'sunita@manipal.com', 'doctor123', '9876541004', 'Pediatrics',       'Pediatrician'),
  ('Mehul Joshi',    'mehul@manipal.com',  'doctor123', '9876541005', 'General Medicine', 'General Physician'),
  ('Kavitha Nair',   'kavitha@manipal.com','doctor123', '9876541006', 'Dermatology',      'Dermatologist'),
  ('Deepak Pillai',  'deepak@manipal.com', 'doctor123', '9876541007', 'ENT',              'ENT Specialist'),
  ('Ananya Bose',    'ananya@manipal.com', 'doctor123', '9876541008', 'Ophthalmology',    'Ophthalmologist');

INSERT INTO patients (name, email, password, phone, dob, blood_group) VALUES
  ('Rahul Nair',    'rahul@gmail.com',   'patient123', '9812300001', '1990-05-15', 'O+'),
  ('Anjali Singh',  'anjali@gmail.com',  'patient123', '9812300002', '1985-11-22', 'B+'),
  ('Mohan Verma',   'mohan@gmail.com',   'patient123', '9812300003', '2000-03-08', 'A-');

INSERT INTO appointments (patient_id, doctor_id, department, appointment_date, status) VALUES
  (1, 1, 'Cardiology',       '2025-03-10', 'completed'),
  (1, 2, 'Neurology',        '2025-03-18', 'completed'),
  (2, 3, 'Orthopedics',      '2025-03-20', 'completed'),
  (3, 4, 'Pediatrics',       '2025-03-22', 'scheduled');

INSERT INTO medicines (doctor_id, patient_id, medicine_name, dosage, issued_date, notes) VALUES
  (1, 1, 'Atorvastatin 20mg', '1 tablet at night',          '2025-03-10', 'Take with water'),
  (1, 1, 'Aspirin 75mg',      '1 tablet daily after meals', '2025-03-10', 'Do not skip'),
  (2, 1, 'Levetiracetam',     '500mg twice daily',          '2025-03-18', 'Monitor for side-effects'),
  (3, 2, 'Ibuprofen 400mg',   '1 tablet thrice daily',      '2025-03-20', 'After food only');

INSERT INTO schedules (doctor_id, schedule_date, time_start, time_end, notes) VALUES
  (1, '2026-03-27', '09:00', '13:00', 'Morning OPD'),
  (1, '2026-03-28', '14:00', '17:00', 'Afternoon consultations'),
  (2, '2026-03-27', '10:00', '12:00', 'Neurology clinic'),
  (3, '2026-03-29', '08:00', '14:00', 'Surgery day');
