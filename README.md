
# Mobile Accessories E-Commerce Store 🛍️  

Django-powered online shop for mobile accessories with JWT authentication, product search, cart management, and admin dashboard.  

---

## ✨ Features  

### 🔐 Authentication & User Management  
- JWT Authentication using Django SimpleJWT  
- User registration, login, logout, and profile management  
- Protected routes for authenticated users  

### 📱 Product Management  
- Product Listing with search by name & category filters  
- Product Detail Page with high-quality images, pricing, and descriptions  
- Modern UI with responsive design (CSS Grid/Flexbox)  

### 🛒 Cart & Checkout  
- Add/remove items from cart  
- Adjust quantities before checkout  
- Save orders to database  

### 👨‍💻 Admin Dashboard  
- Full Django Admin integration  
- Manage products, categories, users, and orders  
- Inventory & stock control  

### ⚡ Performance & Security  
- MySQL for fast & reliable database operations  
- Django REST Framework (DRF) for API endpoints  
- Secure payment handling *(if applicable)*  

---

## 🛠️ Tech Stack  

| Category       | Technologies Used |  
|---------------|------------------|  
| Backend   | Django, Django REST Framework (DRF) |  
| Database  | MySQL |  
| Auth      | SimpleJWT (Token-based) |  
| Frontend  | Django Templates, Bootstrap, Custom CSS/JS |  
| APIs      | DRF for RESTful endpoints |  
| Deployment| *(Optional: Docker, Nginx, Gunicorn)* |  

---

## 🚀 Installation Guide  

### Prerequisites  
- Python 3.9+  
- MySQL Server  
- pip (Python package manager)  

### Setup Steps  

1. Clone the repository  
  
   git clone https://github.com/c1montazerian/mobile-accessories-shop.git
   cd mobile-accessories-shop
   
2. Create & activate a virtual environment  
  
   python -m venv venv
   source venv/bin/activate  # Linux/Mac
   venv\Scripts\activate    # Windows
   
3. Install dependencies  
  
   pip install -r requirements.txt
   
4. Configure MySQL Database  
   - Create a database (e.g., mobile_shop_db)  
   - Update .env file (copy from .env.example):  
    
     SECRET_KEY=your_django_secret_key
     DB_NAME=mobile_shop_db
     DB_USER=your_mysql_user
     DB_PASSWORD=your_mysql_password
     DB_HOST=localhost
     DB_PORT=3306
     
5. Run migrations  
  
   python manage.py migrate
   
6. Create a superuser (Admin Access)  
  
   python manage.py createsuperuser
   
7. Start the development server  
  
   python manage.py runserver
   
8. Access the app  
   - Website: http://localhost:8000/  
   - Admin Panel: http://localhost:8000/admin/  

---

## 📌 Usage Guide  

### For Users  
✅ Browse products with search & category filters  
✅ Add to cart and adjust quantities  
✅ Place orders securely  

### For Admins  
⚙️ Manage products, categories, and inventory via Django Admin  
📊 View & process orders from the dashboard  

---

## 🔌 API Endpoints (DRF)  

| Endpoint | Method | Description |  
|----------|--------|-------------|  
| /api/auth/ | POST | JWT Login/Register |  
| /api/products/ | GET | List all products (search/filter) |  
| /api/cart/ | GET/POST | View/Modify cart |  
| /api/orders/ | POST | Create new order |  

Example API Request (Login):  
curl -X POST http://localhost:8000/api/auth/login/ \
  -H "Content-Type: application/json" \
  -d '{"username": "user", "password": "pass"}'
 


---

## 🤝 Contributing

1. Fork the repository  
2. Create a new branch (git checkout -b feature/new-feature)  
3. Commit changes (git commit -m "Add new feature")  
4. Push to branch (git push origin feature/new-feature)  
5. Open a Pull Request  

---


## 📩 Contact  

- GitHub: [@c1montazerian](https://github.com/c1montazerian)  
- Email: [amirali.mokri@gmail.com] 

---

🌟 Happy Coding! 🚀
