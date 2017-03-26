from flask import Flask, render_template, request, session, redirect, url_for, flash
from models import db, User, Post
from forms import SignupForm, LoginForm




app = Flask(__name__)

app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://localhost/globalconcepts'
db.init_app(app)

app.secret_key = "development-key"

#index page
@app.route("/",)
def index():
    post = Post.query.all()  #something not right here
    return render_template("index.html" , post=post)

#about page
@app.route("/about")
def about():
    return render_template("about.html")

#signup page
@app.route("/signup", methods=['GET', 'POST'])
def signup():
    form = SignupForm()

    if request.method == 'POST':
        if form.validate() == False:
            return render_template("signup.html", form=form)
        else:
            newuser =  User(form.first_name.data, form.last_name.data, form.email.data, form.password.data)
            db.session.add(newuser)
            db.session.commit()

            session['email'] = newuser.email
            return redirect(url_for('home'))

    elif request.method == 'GET':
        return render_template("signup.html", form=form)

#login page
@app.route("/login", methods=['GET', 'POST'])
def login():
    form = LoginForm()

    if request.method == 'POST':
        if form.validate() == False:
            return render_template("login.html", form=form)
        else:
            email = form.email.data
            password = form.password.data

            user = User.query.filter_by(email=email).first()
            if user is not None and user.check_password(password):
                session['email'] = form.email.data
                return redirect(url_for('home'))
            else:
                return redirect(url_for('login'))

    elif request.method == 'GET':
            return render_template('login.html', form=form)

#logout for session
@app.route("/logout")
def logoout():
    session.pop('email', None)
    return redirect(url_for('index'))

#home page
@app.route("/home")
def home():
    return render_template('home.html')

#add post page
@app.route("/add", methods=['POST', 'GET'])
def add():
    if request.method == 'POST':
        post = Post(request.form['title'], request.form['body'], request.form['ddate'])   # something not right here
        db.session.add(post)
        db.session.commit()
        flash("New Entry Posted Succesfully")

    return render_template("add.html")

#edit/update
@app.route("/edit/<uid>", methods=['POST', 'GET'])
def edit(uid):
    post=Post.query.get(uid)
    if request.method == 'post':
        post.title = request.form['title']
        post.text = request.form['body']
        post.date = request.form['ddate', get_credentials()]
        db.session.commit()
        return redirect(url_for("index"))
    return render_template("edit.html", post=post, main=main)

#delete
@app.route("/delete/<uid>" ,methods=['POST', 'GET'])
def delete(uid):
    post = Post.query.get(uid)
    db.session.delete(post)
    db.session.commit()
    flash('post deleted')

    return redirect(url_for("index"))


if __name__ == "__main__":
    app.run(debug=True)