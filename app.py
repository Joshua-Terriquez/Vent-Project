from flask import Flask, request, redirect, url_for, render_template, session
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime
import random
from flask_login import LoginManager, login_user, logout_user, UserMixin, login_required
import os

SECRET_KEY = os.urandom(32)
app = Flask(__name__, static_folder='./frontend/build/static', template_folder='./frontend/build')
app.secret_key = SECRET_KEY
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
    date = db.Column(db.Text, nullable=False, default=str(datetime.now))
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    post_str = db.Column(db.Text)
    post_like = db.Column(db.Integer, default = 0)
    post_dislike = db.Column(db.Integer, default = 0)

    def __init__(self,Date,Userid,Content,Likes,Dislikes):
        self.date = Date
        self.user_id = Userid
        self.post_str= Content
        self.post_like = Likes
        self.post_dislike = Dislikes

    
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
            session["user"] = {'id': user.id, 'name': user.name}
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

@app.route('/like', methods=['PUT'] )
@login_required
def like():

    if request.method == 'PUT':

        print(session.get("postNumber"))

        postid = session.get("postNumber")

        post = UserPost.query.filter_by(id = int(postid)).first()

        print(post)

        likeCount = post.post_like
        
        likeCount = likeCount + 1

        post.post_like = likeCount

        db.session.commit()

        return{"likeCount" : post.post_like}



@app.route('/dislike', methods=['PUT'] )
@login_required
def dislike():
    
    if request.method == 'PUT':

        print(session.get("postNumber"))

        postid = session.get("postNumber")

        post = UserPost.query.filter_by(id = int(postid)).first()
        
        print(post)


        dislikeCount = post.post_dislike
        
        dislikeCount = dislikeCount + 1

        post.post_dislike = dislikeCount

        db.session.commit()


        return{"setDislikeCount" : post.post_dislike}
    
    


@app.route('/Post', methods=['POST'] )
@login_required
def Post():
    if request.method == 'POST':
        post = request.get_json()
        userInfo = session.get("user")

        new_post = UserPost(str(datetime.now), userInfo["id"], post, 0, 0)
        db.session.add(new_post)
        db.session.commit()

        return {"empty" : 0}

@app.route('/profile/posts')
@login_required
def Profile():

    #     id = db.Column(db.Integer, primary_key=True)
    # date = db.Column(db.Text, nullable=False, default=str(datetime.now))
    # user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    # post_str = db.Column(db.Text)
    # post_like = db.Column(db.Integer, default = 0)
    # post_dislike = db.Column(db.Integer, default = 0)

    info = session.get("user")
    id = info["id"]
    posts = UserPost.query.filter(UserPost.user_id == id).all()

    allPost = {}
    listPost = []

    for post in posts:
        allPost.update({"postContent" : post.post_str, "likeCount" : post.post_like, "dislikeCount" : post.post_dislike})
        
    print(allPost)

    listPost = allPost

    return allPost


@app.route('/profile/post/<int:postId>', methods=['DELETE'])
@login_required
def Profile_delete(postId):
    query = UserPost.query.filter_by(id=postId).first()
    db.session.delete(query)
    db.session.commit()
    return {}

@app.route('/MyFeed')
@login_required
def MyFeed():
    info = session.get("user")
    id = info["id"]

    post = []
    post = UserPost.query.filter(UserPost.user_id != id).all()
    
    numberOfAccounts = len(post)
    postid = random.randrange(1, numberOfAccounts)

    chosenPost = post[postid]

    session["postNumber"] = chosenPost.id


    return{"postContent" : post[postid].post_str, "likeCount" : post[postid].post_like, "setDislikeCount" : post[postid].post_dislike}

if __name__ == "__main__":
    with app.app_context():
        # new_user = User(name="test2", email="test", password="1")
        # db.session.add(new_user)
        # db.session.commit()

        db.create_all()
        # new_user = User(name="test", email="test@gmail.com", password="12345")
        # db.session.add(new_user)
        # db.session.commit()
    app.run(debug =True)
