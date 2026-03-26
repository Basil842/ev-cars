import os
import glob

css_content = """@import url('https://fonts.googleapis.com/css2?family=Outfit:wght@300;400;500;600;700&display=swap');

:root {
    --primary: #f36a10;
    --secondary: #242d3d;
    --dark: #121212;
    --light: #ffffff;
    --glass: #ffffff;
    --glass-border: #e2e8f0;
    --accent: #10b981;
}

* {
    margin: 0;
    padding: 0;
    box-sizing: border-box;
    font-family: 'Outfit', sans-serif;
}

body {
    background: #f5f7f8;
    color: var(--dark);
    min-height: 100vh;
}

.container {
    max-width: 1200px;
    margin: 0 auto;
    padding: 0 20px;
}

/* Navbar */
nav {
    padding: 1.2rem 2rem;
    display: flex;
    justify-content: space-between;
    align-items: center;
    background: #ffffff;
    box-shadow: 0 2px 10px rgba(0,0,0,0.05);
    margin: 0 -20px 2rem;
    border-radius: 0 0 12px 12px;
}

.logo {
    font-size: 1.8rem;
    font-weight: 800;
    color: var(--primary);
    text-transform: uppercase;
    letter-spacing: -0.5px;
}

.nav-links a {
    color: var(--secondary);
    text-decoration: none;
    margin-left: 2rem;
    font-weight: 500;
    transition: color 0.3s;
}

.nav-links a:hover {
    color: var(--primary);
}

/* Hero Section */
.hero {
    padding: 4rem 0;
    text-align: center;
}

.hero h1 {
    font-size: 3.5rem;
    margin-bottom: 1rem;
    color: var(--secondary);
    letter-spacing: -1px;
}

.hero p {
    font-size: 1.2rem;
    color: #64748b;
    max-width: 600px;
    margin: 0 auto 2rem;
}

/* Card Grid */
.car-grid {
    display: grid;
    grid-template-columns: repeat(auto-fill, minmax(300px, 1fr));
    gap: 2rem;
    padding: 2rem 0;
}

.car-card {
    background: #ffffff;
    border: 1px solid var(--glass-border);
    border-radius: 12px;
    overflow: hidden;
    transition: transform 0.3s, box-shadow 0.3s;
    box-shadow: 0 4px 15px rgba(0,0,0,0.03);
}

.car-card:hover {
    transform: translateY(-5px);
    box-shadow: 0 12px 30px rgba(0, 0, 0, 0.08);
}

.car-image {
    width: 100%;
    height: 200px;
    background: #f8fafc;
    display: flex;
    align-items: center;
    justify-content: center;
    font-size: 0.9rem;
    color: #94a3b8;
}

.car-info {
    padding: 1.5rem;
}

.car-name {
    font-size: 1.4rem;
    font-weight: 600;
    margin-bottom: 0.5rem;
    color: var(--secondary);
}

.car-specs {
    display: flex;
    justify-content: space-between;
    color: #64748b;
    margin-bottom: 1rem;
    font-size: 0.95rem;
}

.price {
    font-size: 1.3rem;
    font-weight: 700;
    color: var(--secondary);
}

.btn {
    display: inline-block;
    padding: 0.8rem 1.5rem;
    border-radius: 8px;
    text-decoration: none;
    font-weight: 600;
    transition: all 0.3s;
    cursor: pointer;
    border: none;
    text-align: center;
}

.btn-primary {
    background: var(--primary);
    color: white;
}

.btn-primary:hover {
    background: #e05c08;
    box-shadow: 0 4px 12px rgba(243, 106, 16, 0.2);
}

/* Forms */
.auth-container {
    max-width: 450px;
    margin: 4rem auto;
    padding: 2.5rem;
    background: #ffffff;
    border: 1px solid var(--glass-border);
    border-radius: 16px;
    box-shadow: 0 8px 24px rgba(0,0,0,0.04);
}

.form-group {
    margin-bottom: 1.5rem;
}

label {
    display: block;
    margin-bottom: 0.5rem;
    font-size: 0.95rem;
    font-weight: 500;
    color: var(--secondary);
}

input {
    width: 100%;
    padding: 0.8rem 1rem;
    background: #ffffff;
    border: 1px solid #cbd5e1;
    border-radius: 8px;
    color: var(--dark);
    font-size: 1rem;
    transition: border-color 0.3s, box-shadow 0.3s;
}

input:focus {
    outline: none;
    border-color: var(--primary);
    box-shadow: 0 0 0 3px rgba(243, 106, 16, 0.1);
}

/* Admin Dashboard Table */
.dashboard-table {
    width: 100%;
    border-collapse: separate;
    border-spacing: 0;
    margin-top: 1.5rem;
    background: #ffffff;
    border-radius: 12px;
    overflow: hidden;
    box-shadow: 0 2px 10px rgba(0,0,0,0.03);
    border: 1px solid var(--glass-border);
}

.dashboard-table th,
.dashboard-table td {
    padding: 1rem 1.5rem;
    text-align: left;
    border-bottom: 1px solid var(--glass-border);
}

.dashboard-table th {
    background: #f8fafc;
    color: var(--secondary);
    font-weight: 600;
    text-transform: uppercase;
    font-size: 0.85rem;
    letter-spacing: 0.5px;
}

.dashboard-table tr:last-child td {
    border-bottom: none;
}

.status-badge {
    padding: 0.4rem 0.8rem;
    border-radius: 20px;
    font-size: 0.8rem;
    font-weight: 600;
}

.status-pending {
    background: #fff8e1;
    color: #f59e0b;
}

.status-confirmed {
    background: #dcfce7;
    color: #16a34a;
}

.status-cancelled {
    background: #ffe4e6;
    color: #e11d48;
}

/* Responsive */
@media (max-width: 768px) {
    .hero h1 {
        font-size: 2.5rem;
    }
}
"""

with open('c:/Users/ASUS/OneDrive/Desktop/ev_cars/static/css/style.css', 'w') as f:
    f.write(css_content)

for filepath in glob.glob('c:/Users/ASUS/OneDrive/Desktop/ev_cars/templates/*.html'):
    with open(filepath, 'r', encoding='utf-8') as f:
        content = f.read()
    
    # Inline style fixups
    content = content.replace('#94a3b8', '#64748b') 
    content = content.replace('rgba(0,0,0,0.2)', '#f1f5f9') 
    content = content.replace('rgba(255, 255, 255, 0.1)', '#f8fafc')
    content = content.replace('border: 1px dashed var(--glass-border);', 'border: 2px dashed #cbd5e1;')
    content = content.replace('background: rgba(15, 23, 42, 0.6);', 'background: #ffffff;') 
    content = content.replace('color: #fff;', 'color: var(--secondary);') 
    content = content.replace('color: white;', 'color: var(--secondary);') 
    content = content.replace('color: var(--light);', 'color: var(--dark);')
    content = content.replace('color:var(--light);', 'color:var(--dark);')
    
    with open(filepath, 'w', encoding='utf-8') as f:
        f.write(content)

print("Theme updated successfully.")
