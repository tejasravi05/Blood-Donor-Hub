from flask import Flask, render_template, request, redirect, url_for, g
from blood_donor_system import BloodDonorSystem

app = Flask(__name__)
DATABASE = 'donors.db'

def get_db():
    if not hasattr(g, 'db'):
        g.db = BloodDonorSystem()
        g.db.ConnectDB()
        g.db.CreateTable()
    return g.db

@app.teardown_appcontext
def close_connection(exception):
    db = getattr(g, 'db', None)
    if db is not None:
        db.conn.close()

@app.route('/')
def base():
    return render_template('base.html')

@app.route('/about')
def about():
    return render_template('about.html')

@app.route('/services')
def services():
    return render_template('services.html')

@app.route('/testimonials')
def testimonials():
    return render_template('testimonials.html')

@app.route('/contact')
def contact():
    return render_template('contact.html')

@app.route('/eligibility')
def eligibility():
    return render_template('eligibility.html')

@app.route('/check_eligibility', methods=['POST'])
def check_eligibility():
    form_data = request.form
    eligible = check_eligibility_logic(form_data)
    if eligible:
        return render_template('eligibility_result.html', eligible=eligible, form_data=form_data, show_register_button=True)
    else:
        return render_template('eligibility_result.html', eligible=eligible)

@app.route('/register_donor', methods=['POST'])
def register_donor():
    form_data = request.form
    name = form_data['name']
    age = int(form_data['age'])
    blood_group = form_data['blood_group']
    address = form_data['address']
    phone_number = form_data['phone_number']
    eligibility = "Can Donate" if check_eligibility_logic(form_data) else "Cannot Donate"
    
    db = get_db()
    result = db.AddDonor(None, name, blood_group, phone_number)
    return redirect(url_for('base'))

@app.route('/find_donors', methods=['GET', 'POST'])
def find_donors():
    if request.method == 'POST':
        blood_group = request.form['blood_group']
        db = get_db()
        donors = db.SearchDonor(blood_group)
        return render_template('find_donors.html', donors=donors)
    return render_template('find_donors.html', donors=None)

def check_eligibility_logic(form):
    age = int(form['age'])
    haemoglobin = float(form['haemoglobin'])
    pulse = int(form['pulse'])
    systolic_bp = int(form['systolic_bp'])
    diastolic_bp = int(form['diastolic_bp'])
    temperature = float(form['temperature'])
    weight = float(form['weight'])
    
    if not (18 <= age <= 60):
        return False
    if haemoglobin < 12.5:
        return False
    if not (50 <= pulse <= 100):
        return False
    if not (100 <= systolic_bp <= 180):
        return False
    if not (50 <= diastolic_bp <= 100):
        return False
    if temperature > 37.5:
        return False
    if weight < 45:
        return False
    return True

if __name__ == '__main__':
    app.run(debug=True)