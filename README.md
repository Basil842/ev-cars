# Electric Vehicle Recommendation and Booking System

A full-stack web application designed for the KTU 2024 Scheme DBMS mini-project. This system allows users to browse, search, and book electric vehicles, while providing an administrative interface for fleet and booking management.

## Technology Stack
- **Frontend**: HTML5, CSS3 (Custom Glassmorphism Design), JavaScript
- **Backend**: Python Flask
- **Database**: MySQL (XAMPP compatibility)
- **Design**: Modern Dark UI with Responsive Layout

## Features
### User Side
- Register and Login.
- Browse available EVs with images and specifications.
- Filter cars by brand/name.
- Book an EV and view booking history.
- Recommendation section based on top-tier specifications.

### Admin Side
- Secure separate login.
- View all user bookings using a SQL **View**.
- Statistical overview using **Aggregate Functions**.
- Manage fleet (Add/Update/Delete cars).

## DBMS Concepts Used

### 1. Multiple Tables & Relationships
- `users`: Stores user identity. 
- `admin`: Stores administrative credentials.
- `cars`: Stores vehicle specifications.
- `bookings`: Maps users to cars (Many-to-Many resolved into 1-M with pivot).

### 2. SQL Views
- **View Name**: `booking_summary`
- **Purpose**: Combines data from `bookings`, `users`, and `cars` to provide a human-readable list for the admin, without exposing sensitive user data in raw queries.

### 3. Triggers
- **Trigger**: `trg_after_booking_insert`
- **Purpose**: Automatically executes logic after a booking is recorded. In this system, it can be extended to log status changes or verify availability.

### 4. Aggregate Functions
- `COUNT(*)`: Used to calculate Total Bookings and Total Registered Users on the Admin Dashboard.
- `AVG(price)`: (Available for reports) calculates average EV price in the fleet.

### 5. Constraints & Assertions
- `CHECK (price > 0)`: Ensures no car is listed with a negative or zero price.
- `CHECK (range_km > 0)`: Ensures valid battery range data.
- `UNIQUE`: Used for emails and usernames to prevent duplicate accounts.
- `FOREIGN KEY`: Ensures referential integrity between users, cars, and bookings.

## How to Run
1. **Database Setup**:
   - Ensure you have **MySQL Server** installed and running.
   - Open your MySQL terminal or **MySQL Workbench**.
   - Create a database: `CREATE DATABASE ev_booking;`
   - Run the contents of `database.sql` to set up tables and sample data.

2. **Configuration**:
   - Open the `.env` file.
   - Update `DB_USER` and `DB_PASSWORD` with your MySQL credentials.
   - Update `DB_HOST` if your database is not local.

3. **Backend Setup**:
   - Install dependencies: `pip install -r requirements.txt`
   - Run the app: `python app.py`
   - Visit `http://127.0.0.1:5000` in your browser.

3. **Admin Credentials**:
   - **Username**: `admin`
   - **Password**: `admin123`
