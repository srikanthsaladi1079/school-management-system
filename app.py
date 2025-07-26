#Importing required libraries
from flask import Flask, render_template, request, redirect, url_for, flash,session,get_flashed_messages
from flask_sqlalchemy import SQLAlchemy
from extensions import db
from models import Student,Teacher,Parent
import os
from werkzeug.security import generate_password_hash,check_password_hash

#Creating App
app = Flask(__name__)
app.secret_key = 'supersecretkey'

BASE_DIR = os.path.abspath(os.path.dirname(__file__))
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///' + os.path.join(BASE_DIR, 'instance/student_portal.db')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

#Initializing app
db.init_app(app)
from models import Student 

#Home page
@app.route("/")
def home():
    return render_template("home.html")

#Student Registration page
@app.route("/register/student",methods=['GET','POST'])
def register_student():
    if request.method == 'POST':
        first = request.form['first_name']
        middle = request.form['middle_name']
        last = request.form['last_name']
        gender = request.form['gender']
        username = request.form['username']
        password = request.form['password']
        
        existing_user = Student.query.filter_by(username=username).first()
        if existing_user:
            return redirect(url_for("register_student"))
        
        hashed_pw = generate_password_hash(password)
        
        new_student = Student (
            first_name = first,
            middle_name = middle,
            last_name = last,
            gender = gender,
            username = username,
            password = hashed_pw 
        )
        db.session.add(new_student)
        db.session.commit()
        return redirect(url_for('login_student'))
    
    return render_template("register_student.html")

#Student login page
@app.route("/login/student",methods=['GET','POST'])
def login_student():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        
        student = Student.query.filter_by(username=username).first()
        if student and check_password_hash(student.password, password):
            session['student_id'] = student.id
            return redirect(url_for('student_dashboard'))
        else:
            return redirect(url_for("login_student"))
    
    return render_template("login_student.html")

#Student dashboard
@app.route("/dashboard/student")
def student_dashboard():
    if 'student_id' not in session:
        return redirect(url_for("login_student"))
    
    student = Student.query.get(session['student_id'])
    return render_template("dashboard_students.html",student=student)

#Teacher Registration page
@app.route('/register/teacher',methods=['GET','POST'])
def register_teacher():
    if request.method == 'POST':
        first_name = request.form['first_name']
        middle_name = request.form['middle_name']
        last_name = request.form['last_name']
        gender = request.form['gender']
        subject = request.form['subject']
        username = request.form['username']
        password = request.form['password']
        confirm_password = request.form['confirm_password']
        
        if password != confirm_password:
            return redirect(url_for("register_teacher"))
        
        existing_username = Teacher.query.filter_by(username=username).first()
      
        if existing_username:
            return redirect(url_for("register_teacher"))

        hashed_pw = generate_password_hash(password)
        new_teacher = Teacher (
            first_name = first_name, 
            middle_name = middle_name, 
            last_name = last_name, 
            gender = gender, 
            subject = subject, 
            username = username, 
            password = hashed_pw
        )
        
        db.session.add(new_teacher)
        db.session.commit()
        return redirect(url_for('login_teacher'))
    
    return render_template('register_teacher.html')

#Teacher login page
@app.route('/login/teacher',methods=['GET','POST'])
def login_teacher():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        
    
        teacher = Teacher.query.filter_by(username=username).first()
        
        if teacher and check_password_hash(teacher.password, password):
            session['teacher_id'] = teacher.id
            return redirect(url_for('dashboard_teacher'))
        else:
            return redirect(url_for("login_teacher"))
    
    return render_template('login_teacher.html')

#Teacher Dashboard page
@app.route('/dashboard/teacher')
def dashboard_teacher():
    if 'teacher_id' not in session:
        return redirect(url_for('login_teacher'))
    
    teacher = Teacher.query.get(session['teacher_id'])
    return render_template('dashboard_teacher.html',teacher=teacher)
        
#Parent Login page
@app.route('/login/parent', methods=['GET','POST'])
def login_parent():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        
        parent = Parent.query.filter_by(username=username).first()
        if parent and check_password_hash(parent.password, password):
            session['parent_id'] = parent.id   
            return redirect(url_for('dashboard_parent'))
        else:
            return redirect(url_for("login_parent"))
    
    return render_template('login_parent.html')
    
#Parent registration page
@app.route('/register/parent',methods=['GET','POST'])
def register_parent():
    if request.method == 'POST':
        first_name = request.form['first_name']
        middle_name = request.form['middle_name']
        last_name = request.form['last_name']
        phone = request.form['phone']
        email = request.form['email']
        username = request.form['username']
        password = request.form['password']
        
        existing_parent = Parent.query.filter_by(username=username).first()
        existing_email = Parent.query.filter_by(email=email).first()
        
        if existing_parent:
            return redirect(url_for("register_parent"))
        
        if existing_email:
            return redirect(url_for("register_parent"))
        
        hashed_pw = generate_password_hash(password)
        
        new_parent = Parent (
            first_name = first_name,
            middle_name = middle_name,
            last_name = last_name,
            phone = phone,
            email = email,
            username = username,
            password = hashed_pw
        )
        
        db.session.add(new_parent)
        db.session.commit()
        return redirect(url_for('login_parent'))
    

    return render_template("register_parent.html")

#Parent Dashboard page  
@app.route('/dashboard/parent')
def dashboard_parent():
    if 'parent_id' not in session:
        return redirect(url_for('login_parent'))
    
    parent = Parent.query.get(session['parent_id'])
    return render_template('dashboard_parent.html',parent=parent)

#Contact us Page
@app.route('/contact')
def contact():
    return render_template('contact.html')

#Gallery page  
@app.route('/gallery')
def gallery():
    return render_template('gallery.html')

#Logout route
@app.route('/logout')
def logout():
    session.clear()
    return redirect(url_for('home'))
 
#Student account deletion page  
@app.route('/delete/student', methods=['POST'])
def delete_student():
      if 'student_id' not in session:
          return redirect(url_for('login_student'))
      
      student = Student.query.get(session['student_id'])
      password = request.form['password']
      confirm_password = request.form['confirm_password']
      
      if password != confirm_password:
          return redirect(url_for("dashboard_student"))
      
      if not check_password_hash(student.password, password):
          return redirect(url_for("dashboard_student"))
      
      db.session.delete(student)
      db.session.commit()
      session.clear()

      return redirect(url_for("register_student"))
  
#Teacher account deletion page
@app.route('/delete/teacher', methods=['POST'])
def delete_teacher():
      if 'teacher_id' not in session:
          return redirect(url_for('login_teacher'))
      
      teacher = Teacher.query.get(session['teacher_id'])
      password = request.form['password']
      confirm_password = request.form['confirm_password']
      
      if password != confirm_password:
          return redirect(url_for("dashboard_teacher"))
      
      if not check_password_hash(teacher.password, password):
          return redirect(url_for("dashboard_teacher"))
      
      db.session.delete(teacher)
      db.session.commit()
      session.clear()

      return redirect(url_for("register_teacher"))

#Parent account deletion page 
@app.route('/delete/parent', methods=['POST'])
def delete_parent():
      if 'parent_id' not in session:
          return redirect(url_for('login_parent'))
      
      parent = Parent.query.get(session['parent_id'])
      password = request.form['password']
      confirm_password = request.form['confirm_password']
      
      if password != confirm_password:

          return redirect(url_for("dashboard_parent"))
      
      if not check_password_hash(parent.password, password):
          return redirect(url_for("dashboard_parent"))
      
      db.session.delete(parent)
      db.session.commit()
      session.clear()

      return redirect(url_for("register_parent"))
  
#Forgot password page for teacher 
@app.route('/forgot/teacher',methods=['GET','POST'])
def forgot_teacher():
    if request.method == 'POST':
        username = request.form['username']
        new_password = request.form['new_password']
        confirm_password = request.form['confirm_password']
        
        teacher = Teacher.query.filter_by(username=username).first()
        if not teacher:
            return redirect(url_for("forgot_teacher"))
        
        if new_password != confirm_password:
            return redirect(url_for("forgot_teacher"))
        
        teacher.password = generate_password_hash(new_password)
        db.session.commit()

        return redirect(url_for("login_teacher"))

    return render_template("forgot_teacher.html")

#Forgot password page for parent
@app.route('/forgot/parent',methods=['GET','POST'])
def forgot_parent():
    if request.method == 'POST':
        username = request.form['username']
        phone = request.form['phone']
        new_password = request.form['new_password']
        confirm_password = request.form['confirm_password']
        
        parent = Parent.query.filter_by(username=username).first()
        if not parent:
            return redirect(url_for("forgot_parent"))
        
        if parent.phone != phone:
            return redirect(url_for("forgot_parent"))
        
        if new_password != confirm_password:
            return redirect(url_for("forgot_parent"))
        
        parent.password = generate_password_hash(new_password)
        db.session.commit()

        return redirect(url_for("login_parent"))
 
    return render_template("forgot_parent.html")

#Forgot password page for student
@app.route('/forgot/student',methods=['GET','POST'])
def forgot_student():
    if request.method == 'POST':
        username = request.form['username']
        new_password = request.form['new_password']
        confirm_password = request.form['confirm_password']
        
        student = Student.query.filter_by(username=username).first()
        if not student:
            return redirect(url_for("forgot_student"))
        if new_password != confirm_password:
            return redirect(url_for("forgot_student"))
        
        student.password = generate_password_hash(new_password)
        db.session.commit()
        
        return redirect(url_for("login_student"))
    
    return render_template("forgot_student.html")

#Admin login page
@app.route("/login/admin",methods=['GET','POST'])
def login_admin():
    if request.method == 'POST':
        username = request.form["username"]
        password = request.form["password"]
        
        if username == "admin" and password == "vviprincipal":
            session["admin"] = True
            return redirect(url_for("admin_dashboard"))
        else:
            return render_template("login_admin.html")
        
    return render_template("login_admin.html")

#Admin dashboard page with hashed passwords in table and just user tables
@app.route("/admin/dashboard")
def admin_dashboard():
    if "admin" not in session:
        return redirect(url_for("login_admin"))
    
    students = Student.query.all()
    teachers = Teacher.query.all()
    parents = Parent.query.all()
    return render_template("dashboard_admin.html",students=students,teachers=teachers,parents=parents)

#Logout page for admin
@app.route("/logout/admin")
def logout_admin():
    session.pop("admin", None)
    return redirect(url_for("home"))

#Run the Flask app (remove (debug=True) when deploying online)                      
if __name__ == '__main__':
    with app.app_context():
        from models import Student 
        db.create_all()
    app.run(debug=True)