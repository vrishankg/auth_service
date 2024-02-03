from flask import  Flask,redirect, request, url_for, render_template
import pymongo
from pymongo import MongoClient

app = Flask(__name__)

uri = "mongodb+srv://ayushlanka106:jQ380711mrAeupZg@cluster0.sxjgrop.mongodb.net/?retryWrites=true&w=majority"
client = MongoClient(uri,connectTimeoutMS=30000, socketTimeoutMS=None, connect=False, maxPoolsize=1)
db = client.Auth
users = db.Users

@app.route('/')
def index():
    return 'hi'

@app.route('/authenticate', methods=['GET', 'POST'])
def authenticate():
     if request.method == 'POST':

        username = request.form["username"]
        password = request.form["password"]
        user = users.find_one({"username": username, "password": password})

        if user:
            return "user found"
        else:
            return "user not found"



@app.route('/signup', methods=['POST'])
def signup():
   
    user_data = request.json
    name = user_data.get('name')
    location = user_data.get('location')
    budget = user_data.get('budget')
    top_cuisines = user_data.get('top_cuisines')
    fav_activities = user_data.get('fav_activities')

    
    user = {
        'name': name,
        'location': location,
        'budget': budget,
        'top_cuisines': top_cuisines,
        'fav_activities': fav_activities
    }

  
    
    result = users.insert_one(user)

    print(result)
    return "200"



if __name__ == '__main__':
    app.run(debug=True)
