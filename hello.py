from flask import Flask
from flask import request
from flask import render_template

#from flask.ext.pymongo import PyMongo
import pymongo
from pymongo import MongoClient

app = Flask(__name__)
mongo = MongoClient()

db = mongo.course_database2
courses = db.courses

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/', methods=['POST'])
def my_form_post():
    course_list = str(request.form['course_list'])
    course_id = courses.insert({"course_list" : course_list})
    return ('',200)

@app.route('/get_schedule')
def my_form_get():
    ans = ".<br>\n".join([c["course_list"] for c in courses.find()])
    return (ans, 200)

if __name__ == '__main__':
    app.run(debug=True)
