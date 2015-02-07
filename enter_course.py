from flask import Flask
from flask.ext.pymongo import PyMongo
from flask import request
from flask import render_template

app = Flask(__name__)
mongo = PyMongo(app)

@app.route('/')
def my_form():
    return render_template("enter_courses.html")

@app.route('/', methods=['POST'])
def my_form_post():
    course_number = request.form['course_number']
    course_name = request.form['course_name']
    processed_text = course_number + ": " + course_name

    return processed_text

if __name__ == '__main__':
    app.run()
