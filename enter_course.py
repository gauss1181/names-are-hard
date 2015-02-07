from flask import Flask
from flask import request
from flask import render_template

#from flask.ext.pymongo import PyMongo
import pymongo
from pymongo import MongoClient

app = Flask(__name__)
mongo = MongoClient()

db = mongo.course_database
courses = db.courses

@app.route('/')
def my_form():
    return render_template("enter_courses.html")

@app.route('/', methods=['POST'])
def my_form_post():
    course_number = request.form['course_number']
    course_name = request.form['course_name']
    processed_text = course_number + ": " + course_name
    course_id = courses.insert({"name" : course_name, "number" : course_number})

    return render_template('added_course.html', name=course_name, number=course_number)

if __name__ == '__main__':
    app.run()
