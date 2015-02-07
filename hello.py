from flask import Flask
from flask import request
from flask import render_template

import pymongo
from pymongo import MongoClient
from bson.objectid import ObjectId

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
    entry_id = courses.insert({"course_list" : course_list})
    return (str(entry_id),200)

@app.route('/get_schedule')
def my_form_get():
    ans = ".<br>\n".join([str(c) for c in courses.find()])
    return (ans, 200)

@app.route('/schedule')
def show_sch():
    entry_id = request.args['entry_id']
    entry = courses.find_one({"_id": ObjectId(entry_id)})
    course_stuff = entry['course_list']
    return render_template('schedule_page.html', course_list=course_stuff)


if __name__ == '__main__':
    app.run(debug=True)
