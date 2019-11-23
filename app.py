from flask import Flask, render_template, jsonify, redirect
from flask_pymongo import PyMongo
import pymongo
from pymongo import MongoClient # Database connector
import time


# Import my mars web scraping python script
import scrape_mars

# # to overrun heroku problems
from flask_cors import CORS, cross_origin

# Create application with Flask
app = Flask(__name__)

# to overrun heroku problems
cors = CORS(app)
app.config['CORS_HEADERS'] = 'Content-Type'

# Set up mongo connection with PyMongo
###app.config["MONGO_URI"] = "mongodb://localhost:27017/mars_db"
app.config["MONGO_URI"] = "mongodb://ibaloyan:Francis99$@ds155616.mlab.com:55616/heroku_8mh5bx8l"

mongo = PyMongo(app)
# print(mongo)

### Main - Landing Page - index.html
@app.route("/")
def index():
    
    # Get mars_news_data documents from database mars_db ( or heroku_8mh5bx8l ), collection mars_data
    mars_news_data = mongo.db.mars_data.find_one()
    #for MongoClient# mars_news_data = db.mars_data.find_one()
    
    return render_template("index.html", mars_news_data=mars_news_data)

### Scrape route that will execute mars_scrape functions
@app.route("/scrape")
def scrape_all_sites():

    print("We are in scrape")

    #####mars_news_data = mongo.db.mars_data
    mars_news_data = scrape_mars.scrape_all_sites()

    # Insert mars_news_data into database collection mars_data
    mongo.db.mars_data.update({}, mars_news_data, upsert=True)
    #for MongoClient # db.mars_data.update({}, mars_news_data, upsert=True)
    
    # Redirect back to Landing Page
    return redirect("/", code=302)
    
    ###return "Scraping was successful."

if __name__ == "__main__":
    ##print (scrape_mars.scrape_all_sites())
    time.sleep(10)
    app.run(debug=True)    
