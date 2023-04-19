from flask import Flask, render_template,jsonify, request,url_for,redirect
from flask_admin import Admin
from flask_sqlalchemy import SQLAlchemy
from flask_admin.contrib.sqla import ModelView
from flask_login import LoginManager, login_required,login_user, current_user,logout_user
import json


app = Flask(__name__) 

app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///example.sqlite"
app.config["SECRET_KEY"] = "mykey"
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False

db = SQLAlchemy(app)

admin = Admin(app)

########################
class Users(db.Model):
    id = db.Column(db.Integer, primary_key=True)   
    username = db.Column(db.String, unique = True, nullable = False)
    password = db.Column(db.String, nullable = False)
    name = db.Column(db.String, nullable = False)
    isStudent = db.Column(db.Boolean)

    def __init__(self,username, password2, name2, rank2 ):
        self.username = username
        self.password = password2
        self.name = name2
        self.isStudent = rank2

class classes(db.Model):
    id = db.Column(db.Integer, primary_key=True)   
    classname = db.Column(db.String, unique = True, nullable = False)
    teacher = db.Column(db.String, nullable = False)
    time = db.Column(db.String, nullable = False)
    enrolled = db.Column(db.Integer, nullable = False)
    capcity = db.Column(db.Integer, nullable = False)

    def __init__(self,classname2, teacher2, time2, enrolled2, capcity2):
        self.classname = classname2        
        self.teacher = teacher2
        self.time = time2 
        self.enrolled = enrolled2
        self.capcity = capcity2

# class professors(db.Model):
#     id = db.Column(db.Integer, primary_key=True)   
#     classname = db.Column(db.String, unique = True, nullable = False)
#     teacher = db.Column(db.String, nullable = False)

#     def __init__(self,classname2, teacher2):
#         self.classname = classname2        
#         self.teacher = teacher2

class studentsinclasses(db.Model):
    id = db.Column(db.Integer, primary_key=True)   
    students = db.Column(db.String, nullable = False)
    classes = db.Column(db.String, nullable = False)
    teacher = db.Column(db.String, nullable = False)
    grade = db.Column(db.Integer, nullable = False)


    def __init__(self, Sname, Cname, Grade, Teacher):
        self.students= Sname        
        self.classes = Cname
        self.teacher = Teacher
        self.grade = Grade



student1 = Users("ant1","12345", "anthony",True )
student2 = Users("mat2","574839", "matthew",True )
student3 = Users("theo345","64936803", "theodore",True)
student4 = Users("jack64","theskiisblue", "jack",True)

prof1 = Users("anon","jetski", "santosh",False)
prof2 = Users("amhep","test", "ammon hepworth",False)

class1 = classes("CSE 106", prof1.name, "Thursday 5:00pm - 7:20pm", 0, 10)
class2 = classes("CSE 120", prof2.name, "Monday Wednesday 12:00pm - 1:20pm", 0, 10)



list1 = studentsinclasses(student1.name, class1.classname, class1.teacher, 100)
list2 = studentsinclasses(student2.name, class1.classname, class1.teacher, 87)
list3 = studentsinclasses(student4.name, class1.classname, class1.teacher, 98)
list4 = studentsinclasses(student3.name, class2.classname, class2.teacher, 77)
list5 = studentsinclasses(student4.name, class2.classname, class2.teacher, 76)

admin.add_view(ModelView(Users, db.session))
admin.add_view(ModelView(classes, db.session))
admin.add_view(ModelView(studentsinclasses,db.session))


UserName = ""
PassWord = ""
CurrentUser = ""
# HomePage
@app.route("/")
def home():
    return render_template("/login.html")

@app.route("/admin", methods = ['GET'])
def Admin():
    return {}

@app.route("/logout", methods = ['GET'])
def logout():
    return {}

@app.route("/login", methods = ['POST'])
def login():

    content = request.get_json()
    UserName = content['username']
    PassWord = content['password']
    print(UserName)
    print(PassWord)
    if(UserName == "Admin" and PassWord == "password"):
        CurrentUser = "Admin"
        soem = {"good": 1}
        rj = jsonify(soem)
        return rj

    else:
        data = Users.query.filter_by(username = UserName).first()
        CurrentUser = data
        if(data.password == PassWord):
            print(data.isStudent)
            if(data.isStudent == False):
                # redirect(url_for("teachercourses"))
                soem = {"good": 2}
                rj = jsonify(soem)
                return rj
            else:
                # redirect(url_for("studentcourses"))
                soem = {"good": 3}
                rj = jsonify(soem)
                return rj


#teachers
@app.route("/teacher/courses", methods = ['GET'])
def Tscreen():
    a = studentsinclasses.query.all()
    return render_template("teachercourses.html", a = a)


#students
@app.route("/student/courses", methods = ['GET'])
def Sscreen():
    b = classes.query.all()
    return render_template("studentcourse.html", b = b)



if __name__ == "__main__":
    
    with app.app_context():
        #db.drop_all()
        db.create_all()
        # db.session.commit()
        # db.session.add(student1)
        # db.session.add(student2)
        # db.session.add(student3)
        # db.session.add(student4)
        # db.session.add(prof1)
        # db.session.add(prof2)
        # db.session.add(class1)
        # db.session.add(class2)
        # db.session.add(list1)
        # db.session.add(list2)
        # db.session.add(list3)
        # db.session.add(list4)
        # db.session.add(list5)
        # db.session.commit()

        # admin.init_app(app)
    app.run(debug =True)