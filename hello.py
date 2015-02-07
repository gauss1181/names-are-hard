from flask import Flask
from flask import request
from flask import render_template
import json
#from flask.ext.pymongo import PyMongo
import pymongo
from pymongo import MongoClient
from bson.objectid import ObjectId


app = Flask(__name__)
MONGODB_URI = 'mongodb://vincom2:joelisreallycool@ds041821.mongolab.com:41821/db'
mongo = MongoClient(MONGODB_URI)

db = mongo.course_database6
courses = db.courses

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/', methods=['POST'])
def my_form_post():
    course_list = request.form['course_list']
    schedule_hash = hash(frozenset(course_list))
    entry = courses.find_one({"schedule_hash": str(schedule_hash)})
    if entry == None:
        courses.insert({"schedule_hash": str(schedule_hash) ,"course_list" : str(course_list)})
    return (str(schedule_hash),200)

@app.route('/get_schedule')
def my_form_get():
    ans = ".<br>\n".join([str(c) for c in courses.find()])
    return (ans, 200)

@app.route('/schedule')
def show_sch():
    schedule_hash = request.args['entry_id']
    entry = courses.find_one({"schedule_hash": str(schedule_hash)})
    course_stuff = entry['course_list']
    return render_template('schedule_page.html', course_list=course_stuff)

def score(l1, l2):
    return 100 - 3 * len((set(l1)).symmetric_difference(set(l2))) + 5 * len((set(l1)).intersection(set(l2)))

@app.route('/schedule_search_data', methods=['POST'])
def search_data():
    course_list = map(unicode,json.loads(request.form['course_list']))
    schedules_set = set([])
    for c in courses.find():
        curr_list = map(unicode,json.loads(c['course_list']))
        schedule_score = score(course_list, curr_list)
        if set(course_list) != set(curr_list):
            schedules_set.add((schedule_score,c["schedule_hash"]))
    schedules = sorted(list(schedules_set), reverse=True)
    return json.dumps([(s[0],str(s[1])) for s in schedules[:5]])

if __name__ == '__main__':
    app.run(debug=True)
