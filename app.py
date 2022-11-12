from flask import Flask, render_template, request, url_for, redirect, session
from flask_session import Session
import pymongo
import bcrypt
from flask import flash
from forms import RegistrationForm, LoginForm
from chat import CService
from tkinter import *
from client import Client
app= Flask(__name__)
app.config['SECRET_KEY']="chatApplication"
app.config["SESSION_PERMANENT"] = False
app.config["SESSION_TYPE"] = "filesystem"
Session(app)
client = pymongo.MongoClient("127.0.0.1", 27017)
db= client['ChatApplication']
coll= db['UserDetails']


@app.route("/")
@app.route('/login', methods=['GET', 'POST'])
def login():
    message = 'Please login to your account'
    if 'email' in session:
        return redirect(url_for("logged_in"))
    form = LoginForm(request.form)
    if request.method == 'POST' and form.validate():
        email= form.email.data
        password= form.password.data
        email_found = coll.find_one({"email": email})
        if email_found:
            email_val = email_found['email']
            passwordcheck = email_found['password']
            if bcrypt.checkpw(password.encode('utf-8'), passwordcheck):
                session["email"] = email_val
                return redirect(url_for('logged_in'))
            else:
                if 'email' in session:
                    return redirect(url_for("logged_in"))
                message = 'Wrong password'
                return render_template('login.html', form=form, message=message)
        else:
            message = 'Email not found'
            return render_template('login.html', form=form, message=message)
    return render_template('login.html', form= form, message= message)

@app.route("/logout", methods=["POST", "GET"])
def logout():
    if "email" in session:
        session.pop("email", None)
        message="you have sighout"
        return render_template("logout.html", message= message)
    else:
        return redirect(url_for("login"))

@app.route('/logged_in')
def logged_in():
    if "email" in session:
        email = session["email"]
        chatser= CService()
        user_list= chatser.getUserslist(email)
        return render_template('logged_in.html', email=email, user_list=user_list)
    else:
        return redirect(url_for("login"))

@app.route('/chat')
def chat():
    receiver_email= request.args.get('email')
    sender_email= session['email']
    chatser= CService()
    chat_id= chatser.getChatId(sender_email, receiver_email)
    #root = Tk()
    #frame = Frame(root, width=300, height=300)
    #frame.pack()
    Client(sender_email, chat_id)
    return redirect(url_for("logged_in"))



@app.route('/register', methods=['GET', 'POST'])
def register():
    form = RegistrationForm(request.form)
    if request.method == 'POST' and form.validate():
        email = form.email.data
        username =form.username.data
        password = form.password.data
        user_found = coll.find_one({"username": username})
        email_found = coll.find_one({"email": email})
        if user_found:
            message = 'There already is a user by that name'
            return render_template('register.html', form=form, message= message)
        if email_found:
            message = 'This email already exists in database'
            return render_template('register.html', form=form, message= message)

        hashed = bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt())
        user_input = {'username': username, 'email': email, 'password': hashed}
        coll.insert_one(user_input)
                
        flash('Thanks for registering')
        return redirect(url_for('login'))
    return render_template('register.html', form=form)


if __name__== "__main__":
    app.run()

