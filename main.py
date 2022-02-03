'''
HOBNOB BY ARYAN BHAJANKA
REFER THE 'README.MD' FILE FOR DETAILS
''' 

#main.py, HobNob

from re import template
from flask import Flask,render_template, request,redirect
from flask_login import login_required, current_user, login_user, logout_user
from models import UserModel,PostModel, ProfileModel, FollowModel, db, login
from random import sample
 
app = Flask(__name__)
app.secret_key = 'hobnob_aryanbhajanka'
 
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///data.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
 
 
db.init_app(app)
login.init_app(app)
login.login_view = 'login'
 
@app.before_first_request
def create_all():
    db.create_all()
     
@app.route('/', methods=['POST', 'GET'])
@login_required
def blog():
    username = request.form.get('text')
    if request.method == 'POST':


        print("liked")
        '''post_id = request.form.get('id')
        account = PostModel.query.get(post_id)
        print(PostModel.account(id=post_id))
        like = PostModel(id=post_id)
        db.session.add(like)
        db.session.commit()'''

    post = PostModel.query.all()
    post_list = sample(post, 5)
    return render_template('index.html',posts=post_list)
 
@app.route('/login', methods = ['POST', 'GET'])
def login():
    if current_user.is_authenticated:
        return redirect('/')
     
    if request.method == 'POST':
        email = request.form['email']
        user = UserModel.query.filter_by(email = email).first()
        if user is not None and user.check_password(request.form['password']):
            login_user(user)
            return redirect('/')
     
    return render_template('login.html')
 

@app.route('/register', methods=['POST', 'GET'])
def register():
    if current_user.is_authenticated:
        return redirect('/')
     
    if request.method == 'POST':
        email = request.form['email']
        username = request.form['username']
        password = request.form['password']
 
        if UserModel.query.filter_by(email=email).first():
            return ('Email already exists')
             
        user = UserModel(email=email, username=username)
        user.set_password(password)
        db.session.add(user)
        db.session.commit()
        bio = ProfileModel(bio_account=username,bio="Hello I am on HobNob!")
        db.session.add(bio)
        db.session.commit()
        return redirect('/login')
    return render_template('register.html')
 
 
@app.route('/logout')
def logout():
    logout_user()
    return redirect('/')

@app.route('/<username>',methods=['POST', 'GET'])
@login_required
def profile(username):
    try:
        if request.method == 'POST':
            follow = FollowModel(follow_account=username,follower_account=current_user.username)
            followers = FollowModel.query.filter_by(follow_account=username).all()
            if current_user.username in followers:
                print("pass")
            else:
                db.session.add(follow)
                db.session.commit()
        
        bio = ProfileModel.query.filter_by(bio_account=username).all()
        print_post = PostModel.query.filter_by(account=username).all()
        length = len(bio)-1
        bio_main = bio[length]
        return render_template('profile.html',user=username,posts=print_post,bio=bio_main)

    except IndexError or TypeError:
        pass

@app.route('/newpost', methods=['POST', 'GET'])
@login_required
def post():
    if request.method == 'POST':
        text = request.form['text']
        post = PostModel(text=text,account=current_user.username)
        db.session.add(post)
        db.session.commit()
    return render_template('newpost.html')

@app.route('/myprofile',methods=['POST', 'GET'])
@login_required
def myprofile():
    if request.method == 'POST':
        bio = request.form['bio']
        name = request.form['name']
        post_bio = ProfileModel(bio=bio,bio_account=current_user.username, name=name)
        db.session.add(post_bio)
        db.session.commit()
    return render_template("myprofile.html")

@app.route('/viewmyprofile')
def viewmyprofile():
    user = current_user.username
    return redirect('/'+user)

@app.route('/feed')
def feed():
    return render_template('feed.html')

@app.route('/<username>/followers')
def followers(username):
    followers = FollowModel.query.filter_by(follow_account=username).all()
    return render_template("followers.html",followers=followers,username=username)

@app.route('/delete_post',methods=['POST', 'GET'])
@login_required
def delete_post():
    if request.method == 'POST':
        post = request.form['delete']
        post_id = PostModel.query.filter_by(account=current_user.username).all()
        for i in post_id:
            if i.text == post:
                PostModel.query.filter_by(id=i.id).delete()
                db.session.commit()
            else:
                pass
    print_post = PostModel.query.filter_by(account=current_user.username).all()
    return render_template('delete_post.html',posts=print_post)


if __name__ == "__main__":
    app.run (debug=True)