from flask import render_template, request, redirect, url_for, flash
from app import app, db
from app.models import User, Patient, Symptom
from flask_login import login_user, logout_user, login_required, current_user
import csv
import os
from werkzeug.utils import secure_filename

@app.route('/')
@app.route('/index')
def index():
    return render_template('index.html')


@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        username = request.form.get('username')
        email = request.form.get('email')
        password = request.form.get('password')
        user = User(username=username, email=email, password=password)
        db.session.add(user)
        db.session.commit()
        flash('Your account has been created!', 'success')
        return redirect(url_for('login'))
    return render_template('register.html')

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        email = request.form.get('email')
        password = request.form.get('password')
        user = User.query.filter_by(email=email).first()
        if user and user.password == password:
            login_user(user, remember=request.form.get('remember'))
            return redirect(url_for('index'))
        else:
            flash('Login Unsuccessful. Please check email and password', 'danger')
            print("Password yang dimasukkan:", password)
            print("Password yang disimpan di database:", user.password)
            print("Hasil pembandingan password:", check_password_hash(user.password, password))


    return render_template('login.html')

@app.route('/logout')
def logout():
    logout_user()
    return redirect(url_for('index'))

@app.route('/patients')
@login_required
def patients():
    patients = Patient.query.all()
    return render_template('patients.html', patients=patients)

@app.route('/patient/new', methods=['GET', 'POST'])
@login_required
def new_patient():
    if request.method == 'POST':
        name = request.form.get('name')
        age = request.form.get('age')
        diagnosis = request.form.get('diagnosis')
        patient = Patient(name=name, age=age, diagnosis=diagnosis)
        db.session.add(patient)
        db.session.commit()
        flash('Patient added successfully!', 'success')
        return redirect(url_for('patients'))
    return render_template('patient_form.html', title='New Patient')

@app.route('/patient/<int:patient_id>/edit', methods=['GET', 'POST'])
@login_required
def edit_patient(patient_id):
    patient = Patient.query.get_or_404(patient_id)
    if request.method == 'POST':
        patient.name = request.form.get('name')
        patient.age = request.form.get('age')
        patient.diagnosis = request.form.get('diagnosis')
        db.session.commit()
        flash('Patient updated successfully!', 'success')
        return redirect(url_for('patients'))
    return render_template('patient_form.html', title='Edit Patient', patient=patient)

@app.route('/patient/<int:patient_id>/delete', methods=['POST'])
@login_required
def delete_patient(patient_id):
    patient = Patient.query.get_or_404(patient_id)
    db.session.delete(patient)
    db.session.commit()
    flash('Patient deleted successfully!', 'success')
    return redirect(url_for('patients'))

@app.route('/import_symptoms', methods=['GET', 'POST'])
@login_required
def import_symptoms():
    if request.method == 'POST':
        file = request.files['file']
        if not file:
            flash('No file selected', 'danger')
            return redirect(request.url)

        filename = secure_filename(file.filename)
        if not filename.endswith('.csv'):
            flash('File is not CSV format', 'danger')
            return redirect(request.url)

        file_path = os.path.join('uploads', filename)
        file.save(file_path)

        with open(file_path, newline='', encoding='utf-8') as csvfile:
            csvreader = csv.reader(csvfile, delimiter=';')
            next(csvreader)  # Skip the header row
            for row in csvreader:
                if len(row) < 2:
                    continue  # Skip rows with insufficient data
                name, solution = row[0].strip(), row[1].strip()
                if name and solution:
                    symptom = Symptom(name=name, solution=solution)
                    db.session.add(symptom)
            db.session.commit()

        flash('Data imported successfully', 'success')
        return redirect(url_for('symptoms'))

    return render_template('import_symptoms.html')





@app.route('/symptoms')
@login_required
def symptoms():
    all_symptoms = Symptom.query.all()
    return render_template('symptoms.html', symptoms=all_symptoms)


@app.route('/health_check', methods=['GET', 'POST'])
@login_required
def health_check():
    symptoms = Symptom.query.all()
    if request.method == 'POST':
        answers = request.form.to_dict()
        solutions = []

        for symptom_id, answer in answers.items():
            if answer == 'yes':
                symptom = Symptom.query.get(symptom_id)
                if symptom and symptom.solution.strip():
                    solutions.append(symptom.solution)

        return render_template('health_result.html', solutions=solutions)

    return render_template('health_check.html', symptoms=symptoms)
