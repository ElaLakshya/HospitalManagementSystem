# 🏥 Manipal Hospital — Setup & Run Guide

This project is a full-stack web application built with:
- **Backend + Frontend:** Python (Flask framework with Jinja2 HTML templates)
- **Database:** MySQL
- **Styling:** CSS

Follow every step below in order. Do not skip any step.

---

## PART 1 — INSTALL THE REQUIRED SOFTWARE

### Step 1: Install Python

1. Go to https://www.python.org/downloads/
2. Download Python 3.10 or newer
3. During installation on Windows, **tick the checkbox that says "Add Python to PATH"** before clicking Install
4. After installation, open a terminal (Command Prompt on Windows, Terminal on Mac/Linux) and verify it worked:

```
python --version
```

You should see something like `Python 3.11.4`. If you see an error, restart your computer and try again.

---

### Step 2: Install MySQL

**Windows:**
1. Go to https://dev.mysql.com/downloads/installer/
2. Download the MySQL Installer (the smaller "web" version is fine)
3. Run the installer, choose "Developer Default" setup type
4. Set a root password when asked — **write this password down, you will need it later**
5. Complete the installation

**macOS:**
```
brew install mysql
brew services start mysql
```
(If you don't have Homebrew: https://brew.sh)

**Ubuntu / Debian Linux:**
```
sudo apt update
sudo apt install mysql-server
sudo systemctl start mysql
sudo mysql_secure_installation
```

---

## PART 2 — SET UP THE PROJECT FOLDER

### Step 3: Place the Project Files

Unzip or copy the project folder somewhere easy to find, for example:

```
C:\Users\YourName\Desktop\manipal_hospital\     (Windows)
/Users/yourname/Desktop/manipal_hospital/       (Mac)
/home/yourname/manipal_hospital/                (Linux)
```

The folder should look like this inside:

```
manipal_hospital/
├── app.py
├── schema.sql
├── requirements.txt
├── static/
│   └── style.css
└── templates/
    ├── base.html
    ├── index.html
    ├── login.html
    ├── signup.html
    ├── doctor_dashboard.html
    ├── doctor_schedule.html
    ├── doctor_medicines.html
    ├── patient_dashboard.html
    ├── patient_appointments.html
    ├── make_appointment.html
    ├── departments.html
    └── department_detail.html
```

---

### Step 4: Open a Terminal Inside the Project Folder

**Windows:**
- Open the `manipal_hospital` folder in File Explorer
- Click the address bar at the top, type `cmd`, press Enter
- A Command Prompt window will open already inside that folder

**Mac / Linux:**
```
cd /path/to/manipal_hospital
```

All remaining commands must be run from inside this folder.

---

### Step 5: Create a Virtual Environment

A virtual environment keeps the project's Python packages separate from the rest of your system.

```
python -m venv venv
```

Now activate it:

**Windows:**
```
venv\Scripts\activate
```

**Mac / Linux:**
```
source venv/bin/activate
```

After activation you will see `(venv)` appear at the start of your terminal line. This means it is working.

---

### Step 6: Install Python Packages

With the virtual environment active, run:

```
pip install -r requirements.txt
```

This installs Flask, the MySQL connector, and Werkzeug (for password security). Wait for it to finish.

---

## PART 3 — LINK THE DATABASE (MySQL)

### Step 7: Log Into MySQL

**Windows (if MySQL was installed via installer):**
Open the "MySQL Command Line Client" from the Start Menu. It will ask for your root password.

**Mac / Linux (from your terminal):**
```
mysql -u root -p
```
Enter the root password you set during installation.

---

### Step 8: Create the Database and All Tables

Once you are inside the MySQL shell (you will see `mysql>`), run:

```sql
source /full/path/to/manipal_hospital/schema.sql
```

Replace the path with the actual path to your schema.sql file. For example:

- Windows: `source C:/Users/YourName/Desktop/manipal_hospital/schema.sql`
- Mac/Linux: `source /Users/yourname/Desktop/manipal_hospital/schema.sql`

**Alternatively**, you can run it directly from your terminal (not inside MySQL shell):

```
mysql -u root -p < schema.sql
```

This command creates the `manipal_hospital` database, creates all 5 tables (departments, doctors, patients, appointments, medicines_issued), and seeds 8 departments automatically.

After it runs, verify it worked by typing inside the MySQL shell:

```sql
USE manipal_hospital;
SHOW TABLES;
```

You should see 5 tables listed. Type `exit` to leave the MySQL shell.

---

### Step 9: Connect app.py to Your MySQL Database

Open the file `app.py` in any text editor (Notepad, VS Code, etc.).

Find this section near the top of the file (around line 15):

```python
DB_CONFIG = {
    'host':     'localhost',
    'user':     'root',
    'password': '',          # <-- SET YOUR MYSQL PASSWORD HERE
    'database': 'manipal_hospital',
    'charset':  'utf8mb4',
}
```

Replace the empty `''` between the quotes with your MySQL root password. For example, if your password is `admin123`:

```python
    'password': 'admin123',
```

Save the file.

If you did not set a MySQL password during installation, leave it as empty quotes `''`.

---

## PART 4 — START THE WEBSITE

### Step 10: Run the Flask Application

Make sure your terminal is inside the `manipal_hospital` folder and the virtual environment is still active (you should see `(venv)` at the start of the line).

Run:

```
python app.py
```

You should see output like this:

```
 * Running on http://127.0.0.1:5000
 * Running on http://0.0.0.0:5000
 * Debug mode: on
```

---

### Step 11: Open the Website in Your Browser

Open any web browser (Chrome, Firefox, Edge) and go to:

```
http://localhost:5000
```

The Manipal Hospital homepage will appear with the live clock, date, day display, and login/signup options.

---

## PART 5 — USING THE WEBSITE

### How to Register

1. Click **"Create New Account"** on the homepage
2. Select **Doctor** or **Patient** using the toggle buttons at the top of the form
3. Fill in your details:
   - **Doctor:** Name, Email, Phone, Password, Department, Specialization
   - **Patient:** Name, Email, Phone, Password, Date of Birth, Blood Group
4. Click **"Create Account"**
5. You will be redirected to the login page

### How to Login

1. Click **"Login to Your Account"** on the homepage
2. Select **Doctor** or **Patient** toggle
3. Enter your email and password
4. Click **Login**

### How to Browse as Guest (No Account Needed)

1. Click **"Continue as Guest"** on the homepage
2. You can browse all departments and view which doctors are in each department
3. You cannot book appointments or access dashboards as a guest

---

## PART 6 — FEATURES BY USER TYPE

### Doctor Features (after logging in as Doctor)
| Page | What it does |
|------|-------------|
| Dashboard | Shows your name, department, upcoming appointments count |
| Schedule | Monthly calendar with days marked 1–30, shows patient appointments |
| Departments | Browse all departments and their doctors |
| Medicines | See all medicines you have issued; add new medicine records |

### Patient Features (after logging in as Patient)
| Page | What it does |
|------|-------------|
| Dashboard | Shows your profile, upcoming and total appointments |
| Appointments | Full history of past appointments with doctor name, department, date, status |
| Book Appointment | Choose a department, then a doctor, then a date |
| Departments | Browse all departments and their doctors |

---

## PART 7 — STOPPING AND RESTARTING

### To Stop the Website
Press `Ctrl + C` in the terminal where the app is running.

### To Start Again Later
Every time you want to start the website again:

1. Open a terminal in the `manipal_hospital` folder
2. Activate the virtual environment:
   - Windows: `venv\Scripts\activate`
   - Mac/Linux: `source venv/bin/activate`
3. Make sure MySQL is running (it usually starts automatically after the first install)
4. Run: `python app.py`
5. Open `http://localhost:5000` in your browser

You do NOT need to run `schema.sql` or `pip install` again after the first time.

---

## PART 8 — TROUBLESHOOTING

**Problem: "python is not recognized as a command"**
Solution: Python was not added to PATH. Reinstall Python and tick "Add to PATH" during setup, or restart your computer.

**Problem: "Access denied for user root"**
Solution: Wrong MySQL password in app.py. Open app.py, find DB_CONFIG, and correct the password field.

**Problem: "ModuleNotFoundError: No module named flask"**
Solution: Virtual environment is not activated. Run `venv\Scripts\activate` (Windows) or `source venv/bin/activate` (Mac/Linux) and then `pip install -r requirements.txt` again.

**Problem: "Can't connect to MySQL server on localhost"**
Solution: MySQL is not running. Start it:
- Windows: Open Services (search in Start Menu) → find MySQL → click Start
- Mac: `brew services start mysql`
- Linux: `sudo systemctl start mysql`

**Problem: "Table doesn't exist"**
Solution: You haven't run schema.sql yet. Follow Step 8 again.

**Problem: Port 5000 already in use**
Solution: At the bottom of app.py, change the port number:
```python
app.run(debug=True, host='0.0.0.0', port=5001)
```
Then open `http://localhost:5001` instead.

---

## Customer Care
📞 **9800098000**
✉️ **manipalcare@gmail.com**
