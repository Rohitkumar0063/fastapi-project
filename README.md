# 🚀 FastAPI Task Management API

A production-ready backend API built using FastAPI with authentication, role-based access control, and MongoDB integration.

---

## 🔗 Live Demo
👉 https://fastapi-project-u1dm.onrender.com/docs

---

## 📌 Features

- User Registration & Login
- JWT Authentication
- Role-Based Authorization (Admin/User)
- CRUD Operations for Tasks
- Secure Password Hashing (bcrypt)
- MongoDB Atlas Integration
- API Documentation using Swagger
- Deployed on Render

---

## 🛠️ Tech Stack

- **Backend:** FastAPI
- **Database:** MongoDB Atlas
- **Authentication:** JWT (python-jose)
- **Password Hashing:** Passlib (bcrypt)
- **Deployment:** Render
- **Async DB Driver:** Motor

---

## 📂 Project Structure
project/
│── main.py
│── routes/
│── models/
│── schemas/
│── database/
│── utils/
│── requirements.txt
│── .env


---

## ⚙️ Installation & Setup

### 1. Clone the repository
```bash
git clone https://github.com/your-username/your-repo-name.git
cd your-repo-name


2. Create virtual environment
python -m venv myenv
myenv\Scripts\activate
3. Install dependencies
pip install -r requirements.txt
4. Setup environment variables

Create a .env file:

MONGO_URI=your_mongodb_connection_string
SECRET_KEY=your_secret_key
ALGORITHM=HS256
5. Run the server
uvicorn main:app --reload
🔐 Authentication Flow
User registers with email & password
Password is hashed using bcrypt
JWT token is generated on login
Protected routes require Bearer token
Role-based access control enforced
📖 API Documentation

Swagger UI available at:

/docs
🚧 Future Improvements
Add Redis caching
Implement rate limiting
Add background job queue
Dockerize application

👨‍💻 Author
Rohit Kumar




