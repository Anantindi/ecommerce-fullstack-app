# 📱 PhoneVerse — E-Commerce Application for Smartphones

A responsive e-commerce web application to browse and purchase smartphones. Built with **Python**, **Flask**, and **HTML/CSS**. Users can register, log in, add items to the cart, check stock, and receive email confirmations after placing an order.

---

## 🚀 Features

- 🔍 Browse smartphones with filters (brand, price)
- 🛒 Add to cart or buy now
- 🔐 User authentication (register/login/logout)
- 📦 Stock management (no over-purchase)
- 📧 Email confirmation on order placement
- 📉 Cannot purchase if item is out of stock

---

## 💻 Tech Stack

- **Backend**: Python, Flask, Flask-SQLAlchemy, Flask-Mail, Flask-Login, Flask-WTF
- **Database**: SQLAlchemy (SQLite)
- **Frontend**: HTML5, CSS3
- **API Testing**: Postman

---

---

## ⚙️ Setup Instructions

1. **Clone the repository**
   ```bash
   git clone https://github.com/yourusername/phoneverse-ecommerce.git
   cd phoneverse-ecommerce
   ```

2. **Create and activate virtual environment**
   ```bash
   python -m venv .venv
   .venv\Scripts\activate   # On Windows
   ```

3. **Install dependencies**
   ```bash
   pip install -r requirements.txt
   ```

4. **Set environment variables**  
   Create a `.env` file in the root directory with:
   ```
   SECRET_KEY=your-secret-key
   MAIL_USERNAME=your email address
   MAIL_PASSWORD=your app password
   ```

5. **Initialize the database**
   ```bash
   python
   >>> from app import create_app, db
   >>> app = create_app()
   >>> app.app_context().push()
   >>> db.create_all()
   >>> exit()
   ```

6. **Seed the product data**
   ```bash
   python seed_data.py
   ```

7. **Run the application**
   ```bash
   python run.py
   ```

8. Visit `http://127.0.0.1:5000/` in your browser.

---

## 📁 Project Structure

```
📁 app/
│   ├── templates/
│   ├── static/
│   ├── __init__.py
│   ├── routes.py
│   ├── models.py
│   └── forms.py
├── seed_data.py
├── run.py
├── requirements.txt
└── README.md
```

---

## 👨‍💻 Developed By

**Anant Jagadish Indi**  


## 📬 License

This project is for educational purposes only.
