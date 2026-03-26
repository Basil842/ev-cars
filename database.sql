-- Database script for EV Recommendation and Booking System

CREATE DATABASE IF NOT EXISTS ev_booking;
USE ev_booking;

-- Users table
CREATE TABLE IF NOT EXISTS users (
    user_id INT AUTO_INCREMENT PRIMARY KEY,
    name VARCHAR(100) NOT NULL,
    email VARCHAR(100) NOT NULL UNIQUE,
    password VARCHAR(255) NOT NULL,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Admin table
CREATE TABLE IF NOT EXISTS admin (
    admin_id INT AUTO_INCREMENT PRIMARY KEY,
    username VARCHAR(100) NOT NULL UNIQUE,
    password VARCHAR(255) NOT NULL
);

-- Cars table
CREATE TABLE IF NOT EXISTS cars (
    car_id INT AUTO_INCREMENT PRIMARY KEY,
    name VARCHAR(100) NOT NULL,
    brand VARCHAR(100) NOT NULL,
    price DECIMAL(10, 2) NOT NULL,
    range_km INT NOT NULL,
    image_url VARCHAR(255),
    description TEXT,
    CONSTRAINT chk_price CHECK (price > 0),
    CONSTRAINT chk_range CHECK (range_km > 0)
);

-- Bookings table
CREATE TABLE IF NOT EXISTS bookings (
    booking_id INT AUTO_INCREMENT PRIMARY KEY,
    user_id INT NOT NULL,
    car_id INT NOT NULL,
    customer_name VARCHAR(100),
    customer_address TEXT,
    customer_phone VARCHAR(20),
    customer_email VARCHAR(100),
    booking_date DATETIME DEFAULT CURRENT_TIMESTAMP,
    status ENUM('Pending', 'Confirmed', 'Cancelled') DEFAULT 'Pending',
    FOREIGN KEY (user_id) REFERENCES users(user_id) ON DELETE CASCADE,
    FOREIGN KEY (car_id) REFERENCES cars(car_id) ON DELETE CASCADE
);

-- VIEW: show booked cars and total users summary
CREATE OR REPLACE VIEW booking_summary AS
SELECT 
    b.booking_id,
    u.name AS user_account,
    b.customer_name,
    b.customer_email,
    b.customer_phone,
    b.customer_address,
    c.name AS car_name,
    c.brand,
    b.booking_date,
    b.status
FROM bookings b
JOIN users u ON b.user_id = u.user_id
JOIN cars c ON b.car_id = c.car_id;

-- TRIGGER: Auto-update booking status when a car is booked (Dummy example for status flow)
DELIMITER //
CREATE TRIGGER trg_after_booking_insert
AFTER INSERT ON bookings
FOR EACH ROW
BEGIN
    -- In a real scenario, you might update car availability
    -- Here we just ensure the status is logged or potentially update a log table
END; //
DELIMITER ;

-- Insert some sample data
INSERT INTO admin (username, password) VALUES ('admin', 'admin123');

INSERT INTO cars (name, brand, price, range_km, image_url, description) VALUES
('Model 3', 'Tesla', 10000000.00, 500, 'https://images.unsplash.com/photo-1560958089-b8a1929cea89?auto=format&fit=crop&q=80&w=800', 'Modern and sleek electric sedan.'),
('Ioniq 5', 'Hyundai', 5000000.00, 480, 'https://cdni.autocarindia.com/ExtraImages/20230207113158_Hyundai_Ioniq_5_front.jpeg', 'Next-gen electric SUV with retro styling.'),
('EV6', 'Kia', 4000000.00, 510, 'https://www.kia.com/content/dam/kwcms/kme/global/en/assets/vehicles/ev6-gt/discover/kia-ev6-gt-my23-discover-keyvisual-w.jpg', 'High-performance electric crossover.'),
('Leaf', 'Nissan', 28000.00, 240, 'https://www-asia.nissan-cdn.net/content/dam/Nissan/AU/Images/about-nissan/news/2025/june/All-new_Nissan_LEAF_Dynamic_Pictures_01.jpg.ximg.l_12_m.smart.jpg', 'Reliable and affordable electric hatch.');

-- AGGREGATE FUNCTION example usage (can be used in queries):
-- SELECT COUNT(*) as total_bookings FROM bookings;
-- SELECT AVG(price) as average_price FROM cars;
