from extensions import db

class Student(db.Model):
    id = db.Column(db.Integer,primary_key=True)
    first_name = db.Column(db.String(50),nullable=False)
    middle_name = db.Column(db.String(50))
    last_name = db.Column(db.String(100),nullable=False)
    gender = db.Column(db.String(10),nullable=False)
    username = db.Column(db.String(25),unique=True,nullable=False)
    password = db.Column(db.String(50),nullable=False)
    
    def __repr__(self):
        return f"<Student {self.username}>"
    
class Teacher(db.Model):
    id = db.Column(db.Integer,primary_key=True)
    first_name = db.Column(db.String(50),nullable=False)
    middle_name = db.Column(db.String(50))
    last_name = db.Column(db.String(50),nullable=False)
    gender = db.Column(db.String(10),nullable=False)
    subject = db.Column(db.String(50),nullable=False)
    username = db.Column(db.String(50),unique=True,nullable=False)
    password = db.Column(db.String(24),nullable=False)
    
    def __repr__(self):
        return f"<Teacher {self.username}>"
    

class Parent(db.Model):
    id = db.Column(db.Integer,primary_key=True)
    first_name = db.Column(db.String(100),nullable=False)
    middle_name = db.Column(db.String(100))
    last_name = db.Column(db.String(100),nullable=False)
    phone = db.Column(db.String(15),nullable=False)           
    email = db.Column(db.String(30),nullable=False,unique=True) 
    username = db.Column(db.String(30),nullable=False,unique=True)
    password = db.Column(db.String(50),nullable=False)
    
    def __repr__(self):
        return f"<Parent {self.username}>"

  