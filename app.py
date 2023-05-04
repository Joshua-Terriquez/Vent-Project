from flask import Flask, request, redirect, url_for, render_template, session
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime
from flask_login import LoginManager, login_user, logout_user, UserMixin, login_required
import os

SECRET_KEY = os.urandom(32)
app = Flask(__name__, static_folder='./frontend/build/static', template_folder='./frontend/build')
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///mydatabase.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SECRET_KEY'] = SECRET_KEY

app.debug=True

db = SQLAlchemy(app)

class User(UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50))
    email = db.Column(db.String(50), unique=True)
    password = db.Column(db.String(255))
    posts = db.relationship('UserPost', backref='author', lazy=True)

class UserPost(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    date = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    post_str = db.Column(db.Text)
    post_like = db.Column(db.Integer, default = 0)
    post_dislike = db.Column(db.Integer, default = 0)

    
################################
login_manager = LoginManager()
login_manager.init_app(app)

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))

@login_manager.request_loader
def load_user_from_request(request):
    email = request.form.get('email')
    if email:
        return User.query.filter_by(email=email).first()
    return None
################################


#calls
@app.route('/protected')
@login_required
def protected():
    return 'Logged in as: ' + flask_login.current_user.id

#login logout Sign up
@app.route('/')
def index():
    return render_template("index.html")
#-------------------------------------------------

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        auth = request.get_json()
        email = auth["username"]
        password = auth["password"]

        user = User.query.filter_by(email=email).first()

        if user is not None and user.password == password:
            login_user(user)
            session['email'] = user.email
            session["loggedin"] = True
            session["user"] = user
            return {"code": "12345"}
            # return flask.redirect(flask.url_for('home'))
        print("yea this didnt work")
        return 'Bad login'

@app.route('/logout')
@login_required
def logout():
    logout_user()
    del session['email']
    return {"success" : True} 
    #return redirect(url_for('/')) ################################## need to change

@app.route('/signup', methods=['GET', 'POST'])
def signup():
    name = request.form['name']
    email = request.form['email']
    password = request.form['password']

    # create a new user and add to database
    new_user = User(name=name, email=email, password=password)
    db.session.add(new_user)
    db.session.commit()

    return redirect(url_for('login'))
#-----------------------------------------------------


@app.route('/home')
@login_required
def home():
    return 'Welcome to your home page, ' + flask_login.current_user.name + '!'

#: Login, logout, session token(maybe),
# new post upload, like/dislike (onclick return a new post to populate the <h2>, GET all post from self.

@app.route('/like')
@login_required
def like():
    return 

@app.route('/dislike')
@login_required
def dislike():
    return 

@app.route('/Post', methods=['POST'] )
@login_required
def Post():
    # id = db.Column(db.Integer, primary_key=True)
    # date = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)
    # user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    # post_str = db.Column(db.Text)
    # post_like = db.Column(db.int)
    # post_dislike = db.Column(db.int)

    user = session['user']

    post = request.get_json()
    retrieveContent = post["content"]

    new_post = Post(datetime.utcnow, user.id, retrieveContent,)
    db.session.add(new_post)
    db.session.commit()

    return

@app.route('/Profile')
@login_required
def Profile():
    return 

@app.route('/MyFeed')
@login_required
def MyFeed():
    return 

if __name__ == "__main__":
    with app.app_context():
        # new_user = User(name="test", email="test@gmail.com", password="12345")
        # db.session.add(new_user)
        # db.session.commit()
        db.create_all()
    app.run(debug =True)
