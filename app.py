import sqlite3

from flask import Flask, render_template, request, flash, redirect, url_for
from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()


class Student(db.Model):
    sno = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(80), unique=False, nullable=False)
    email = db.Column(db.String(120), nullable=False)
    rollno = db.Column(db.Integer, nullable=False)


app = Flask(__name__)
db.init_app(app)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///student.sqlite'
db.create_all(app=app)
app.secret_key = "Secret Key"
if __name__ == '__main__':
    app.run(debug=True)


@app.route('/')
def index():
    alldata = Student.query.all()
    return render_template('index.html', alldata=alldata)


@app.route('/delete/<sno>/', methods=['GET', 'POST'])
def delete(sno):
    alldata = Student.query.get(sno)
    db.session.delete(alldata)
    db.session.commit()
    flash("Deleted")
    return redirect(url_for('index'))


@app.route('/update', methods=['GET', 'POST'])
def update():
    if request.method == 'POST':
        mydata = Student.query.get(request.form.get('sno'))
        mydata.name = request.form['name']
        mydata.email = request.form['email']
        mydata.rollno = request.form['rollno']
        db.session.commit()
        flash("Updated Successfully")
        return redirect(url_for('index'))


@app.route('/insert', methods=['POST'])
def insert():
    if request.method == 'POST':
        name = request.form['name']
        email = request.form['email']
        rollno = request.form['rollno']
        mydata = Student(name=name, email=email, rollno=rollno)
        db.session.add(mydata)
        db.session.commit()
        flash("Added Successfully")
        return redirect(url_for('index'))
