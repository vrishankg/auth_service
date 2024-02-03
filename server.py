from models.Activities import Activities
from models.Restaurant import Restaurant
from flask import  Flask,redirect, request, url_for, render_template
import pymongo
from pymongo import MongoClient

app = Flask(__name__)

uri = "mongodb+srv://ayushlanka106:jQ380711mrAeupZg@cluster0.sxjgrop.mongodb.net/?retryWrites=true&w=majority"
client = MongoClient(uri,connectTimeoutMS=30000, socketTimeoutMS=None, connect=False, maxPoolsize=1)
Auth = client.Auth
users = Auth.Users
restraunts = client.Data.Restaurants
activities = client.Data.Activities

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

@app.route('/add_restraunt', methods=['POST'])
def add_restaurant():
    restraunt_data = request.json

    new_restaurant = Restaurant(
            name= restraunt_data.get('name'),
            location= restraunt_data.get('location'),
            price= restraunt_data.get('price'),
            cuisine= restraunt_data.get('cuisine'),
            timing= restraunt_data.get('timing')
        )

    result = restraunts.insert_one(new_restaurant.to_dict())
    return "200"

@app.route('/add_activities', methods=['POST'])
def add_activities():
    activities_data = request.json
    
    new_event = Activities(
            name=activities_data.get('name'),
            location=activities_data.get('location'),
            date=activities_data.get('date'),
            time=activities_data.get('time'),
            description=activities_data.get('description')
        )

    result = activities.insert_one(new_event.to_dict())
    return "200"

if __name__ == '__main__':
    app.run(debug=True)