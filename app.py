from flask import Flask, render_template, request, redirect, url_for, session, jsonify, flash
import os
import json
from datetime import datetime
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

app = Flask(__name__)
app.secret_key = os.getenv('SECRET_KEY', 'default_secret_key')

DB_FILE = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'database.json')

def load_db() -> dict:
    if not os.path.exists(DB_FILE):
        return {"users": [], "admin": [], "cars": [], "bookings": []}
    with open(DB_FILE, 'r') as f:
        return dict(json.load(f))

def save_db(data: dict) -> None:
    with open(DB_FILE, 'w') as f:
        json.dump(data, f, indent=4)

@app.template_filter('formatdatetime')
def format_datetime(value, format="%B %d, %Y"):
    if isinstance(value, str):
        try:
            date_obj = datetime.strptime(value, "%Y-%m-%d %H:%M:%S")
            return date_obj.strftime(format)
        except ValueError:
            return value
    if hasattr(value, 'strftime'):
        return value.strftime(format)
    return value

# ----------------- ROUTES -----------------

@app.route('/')
def index():
    db = load_db()
    return render_template('index.html', cars=db.get('cars', []), upcoming_cars=db.get('upcoming_cars', []))

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        email = request.form['email']
        password = request.form['password']
        db = load_db()
        user = next((u for u in db.get('users', []) if u['email'] == email and u['password'] == password), None)
        
        if user:
            session['loggedin'] = True
            session['id'] = user['user_id']
            session['name'] = user['name']
            session['role'] = 'user'
            return redirect(url_for('index'))
        else:
            flash('Incorrect email/password!', 'danger')
    return render_template('login.html')

@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        name = request.form['name']
        email = request.form['email']
        password = request.form['password']
        
        db = load_db()
        users = db.get('users', [])
        
        # Check if email exists
        if any(u['email'] == email for u in users):
            flash('Account with this email already exists!', 'danger')
            return redirect(url_for('register'))
            
        new_id = max([u['user_id'] for u in users] + [0]) + 1
        
        new_user = {
            'user_id': new_id,
            'name': name,
            'email': email,
            'password': password,
            'created_at': datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        }
        
        db['users'].append(new_user)
        save_db(db)
        
        flash('You have successfully registered!', 'success')
        return redirect(url_for('login'))
    return render_template('register.html')

@app.route('/admin/login', methods=['GET', 'POST'])
def admin_login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        db = load_db()
        
        admin = next((a for a in db.get('admin', []) if a['username'] == username and a['password'] == password), None)
        
        if admin:
            session['loggedin'] = True
            session['id'] = admin['admin_id']
            session['username'] = admin['username']
            session['role'] = 'admin'
            return redirect(url_for('admin_dashboard'))
        else:
            flash('Incorrect username/password!', 'danger')
    return render_template('admin_login.html')

@app.route('/dashboard')
def dashboard():
    if 'loggedin' in session and session['role'] == 'user':
        db = load_db()
        user_bookings = [b for b in db.get('bookings', []) if b['user_id'] == session['id']]
        
        # Join with cars to get car name and brand
        for b in user_bookings:
            car = next((c for c in db.get('cars', []) if c['car_id'] == b['car_id']), None)
            if car:
                b['name'] = car['name']
                b['brand'] = car['brand']
                
        return render_template('user_dashboard.html', bookings=user_bookings)
    return redirect(url_for('login'))

@app.route('/car/<int:car_id>')
def car_details(car_id):
    db = load_db()
    car = next((c for c in db.get('cars', []) if c['car_id'] == car_id), None)
    if car:
        return render_template('car_details.html', car=car)
    return redirect(url_for('index'))

@app.route('/admin/dashboard')
def admin_dashboard():
    if 'loggedin' in session and session['role'] == 'admin':
        db = load_db()
        users = db.get('users', [])
        cars = db.get('cars', [])
        bookings = db.get('bookings', [])
        
        # Build booking summary
        # Contains booking_id, user_account, customer_name, customer_email, customer_phone, customer_address, car_name, brand, booking_date, status
        booking_summary = []
        for b in bookings:
            u = next((u for u in users if u['user_id'] == b['user_id']), None)
            c = next((c for c in cars if c['car_id'] == b['car_id']), None)
            
            s = b.copy()
            if u:
                s['user_account'] = u['name']
            if c:
                s['car_name'] = c['name']
                s['brand'] = c['brand']
            booking_summary.append(s)
            
        return render_template('admin_dashboard.html', 
                             bookings=booking_summary, 
                             total_bookings=len(bookings), 
                             total_users=len(users),
                             cars=cars,
                             users=users)
    return redirect(url_for('admin_login'))

@app.route('/recommend', methods=['GET', 'POST'])
def recommend():
    if 'loggedin' in session and session['role'] == 'user':
        db = load_db()
        cars = db.get('cars', [])
        recommendations = []
        if request.method == 'POST':
            max_price = request.form.get('max_price', type=float)
            min_range = request.form.get('min_range', type=int)
            
            for c in cars:
                # Need to handle missing data gracefully just in case
                if float(c['price']) <= max_price and int(c['range_km']) >= min_range:
                    recommendations.append(c)
                    
            return render_template('recommend.html', cars=recommendations, searched=True)
        return render_template('recommend.html', cars=[], searched=False)
    return redirect(url_for('login'))

@app.route('/admin/add_car', methods=['GET', 'POST'])
def add_car():
    if 'loggedin' in session and session['role'] == 'admin':
        if request.method == 'POST':
            name = request.form['name']
            brand = request.form['brand']
            price = request.form['price']
            range_km = request.form['range_km']
            image_url = request.form['image_url']
            description = request.form['description']
            
            db = load_db()
            cars = db.get('cars', [])
            new_id = max([c['car_id'] for c in cars] + [0]) + 1
            
            new_car = {
                'car_id': new_id,
                'name': name,
                'brand': brand,
                'price': float(price),
                'range_km': int(range_km),
                'image_url': image_url,
                'description': description,
                'battery_capacity': request.form.get('battery_capacity', ''),
                'power_bhp': request.form.get('power_bhp', ''),
                'charging_dc': request.form.get('charging_dc', ''),
                'charging_ac': request.form.get('charging_ac', ''),
                'boot_space': request.form.get('boot_space', ''),
                'safety_rating': request.form.get('safety_rating', ''),
                'extra_images': request.form.get('extra_images', ''),
                'variants_text': request.form.get('variants_text', '')
            }
            db['cars'].append(new_car)
            save_db(db)
            
            flash('New EV added successfully!', 'success')
            return redirect(url_for('admin_dashboard'))
        return render_template('add_car.html')
    return redirect(url_for('admin_login'))

@app.route('/admin/update_booking/<int:booking_id>/<string:status>')
def update_booking(booking_id, status):
    if 'loggedin' in session and session['role'] == 'admin':
        if status in ['Confirmed', 'Cancelled']:
            db = load_db()
            booking = next((b for b in db.get('bookings', []) if b['booking_id'] == booking_id), None)
            
            if booking:
                current_status = booking['status']
                if status == 'Confirmed' and current_status != 'Pending':
                    flash(f'Cannot confirm booking #{booking_id}. It is currently {current_status}.', 'danger')
                else:
                    booking['status'] = status
                    save_db(db)
                    flash(f'Booking #{booking_id} updated to {status}!', 'success')
        return redirect(url_for('admin_dashboard'))
    return redirect(url_for('admin_login'))

@app.route('/admin/edit_car/<int:car_id>', methods=['GET', 'POST'])
def edit_car(car_id):
    if 'loggedin' in session and session['role'] == 'admin':
        db = load_db()
        car = next((c for c in db.get('cars', []) if c['car_id'] == car_id), None)
        
        if request.method == 'POST':
            if car:
                car['name'] = request.form['name']
                car['brand'] = request.form['brand']
                car['price'] = float(request.form['price'])
                car['range_km'] = int(request.form['range_km'])
                car['image_url'] = request.form['image_url']
                car['description'] = request.form['description']
                car['battery_capacity'] = request.form.get('battery_capacity', '')
                car['power_bhp'] = request.form.get('power_bhp', '')
                car['charging_dc'] = request.form.get('charging_dc', '')
                car['charging_ac'] = request.form.get('charging_ac', '')
                car['boot_space'] = request.form.get('boot_space', '')
                car['safety_rating'] = request.form.get('safety_rating', '')
                car['extra_images'] = request.form.get('extra_images', '')
                car['variants_text'] = request.form.get('variants_text', '')
                save_db(db)
                flash('Car details updated successfully!', 'success')
            return redirect(url_for('admin_dashboard'))
            
        if car:
            return render_template('edit_car.html', car=car)
    return redirect(url_for('admin_login'))

@app.route('/admin/delete_car/<int:car_id>')
def delete_car(car_id):
    if 'loggedin' in session and session['role'] == 'admin':
        db = load_db()
        cars = db.get('cars', [])
        # Also need to cascade to deleting bookings for this car? The original SQL had ON DELETE CASCADE
        db['cars'] = [c for c in cars if c['car_id'] != car_id]
        db['bookings'] = [b for b in db.get('bookings', []) if b['car_id'] != car_id]
        save_db(db)
        flash('Car record deleted successfully.', 'success')
        return redirect(url_for('admin_dashboard'))
    return redirect(url_for('admin_login'))

@app.route('/admin/delete_user/<int:user_id>')
def delete_user(user_id):
    if 'loggedin' in session and session['role'] == 'admin':
        db = load_db()
        db['users'] = [u for u in db.get('users', []) if u['user_id'] != user_id]
        # ON DELETE CASCADE for bookings related to this user
        db['bookings'] = [b for b in db.get('bookings', []) if b['user_id'] != user_id]
        save_db(db)
        flash('User record and associated bookings deleted successfully.', 'success')
        return redirect(url_for('admin_dashboard'))
    return redirect(url_for('admin_login'))

@app.route('/book/<int:car_id>')
def book_car(car_id):
    if 'loggedin' in session and session['role'] == 'user':
        db = load_db()
        car = next((c for c in db.get('cars', []) if c['car_id'] == car_id), None)
        if car:
            return render_template('booking_form.html', car=car)
    return redirect(url_for('login'))

@app.route('/confirm_booking', methods=['POST'])
def confirm_booking():
    if 'loggedin' in session and session['role'] == 'user':
        car_id = int(request.form['car_id'])
        customer_name = request.form['customer_name']
        customer_email = request.form['customer_email']
        customer_phone = request.form['customer_phone']
        customer_address = request.form['customer_address']
        
        db = load_db()
        bookings = db.get('bookings', [])
        new_id = max([b['booking_id'] for b in bookings] + [0]) + 1
        
        new_booking = {
            'booking_id': new_id,
            'user_id': session['id'],
            'car_id': car_id,
            'customer_name': customer_name,
            'customer_email': customer_email,
            'customer_phone': customer_phone,
            'customer_address': customer_address,
            'booking_date': datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
            'status': 'Pending'
        }
        
        db['bookings'].append(new_booking)
        save_db(db)
        
        flash('Car booked successfully!', 'success')
        return redirect(url_for('invoice', booking_id=new_id))
    return redirect(url_for('login'))

@app.route('/invoice/<int:booking_id>')
def invoice(booking_id):
    if 'loggedin' in session:
        db = load_db()
        
        if session['role'] == 'admin':
            booking = next((b for b in db.get('bookings', []) if b['booking_id'] == booking_id), None)
        else:
            booking = next((b for b in db.get('bookings', []) if b['booking_id'] == booking_id and b['user_id'] == session['id']), None)
        
        if booking:
            car = next((c for c in db.get('cars', []) if c['car_id'] == booking['car_id']), None)
            return render_template('invoice.html', booking=booking, car=car)
            
    return redirect(url_for('index'))

@app.route('/cancel_booking/<int:booking_id>')
def cancel_booking(booking_id):
    if 'loggedin' in session and session['role'] == 'user':
        db = load_db()
        
        booking = next((b for b in db.get('bookings', []) if b['booking_id'] == booking_id and b['user_id'] == session['id'] and b['status'] == 'Pending'), None)
        
        if booking:
            booking['status'] = 'Cancelled'
            save_db(db)
            flash('Booking successfully cancelled.', 'success')
        else:
            flash('Cannot cancel this booking. It may already be confirmed or does not exist.', 'danger')
            
        return redirect(url_for('dashboard'))
    return redirect(url_for('login'))

@app.route('/logout')
def logout():
    session.clear()
    return redirect(url_for('index'))

@app.route('/about')
def about():
    return render_template('about.html')

if __name__ == '__main__':
    app.run(debug=True)
