from flask import Flask, render_template, jsonify, redirect
from flask_pymongo import PyMongo
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
app.config["MONGO_URI"] = "mongodb://heroku_8mh5bx8l:Francis99$@ds155616.mlab.com:55616/heroku_8mh5bx8l"

#___________________________________________________________________________________
# connMLAB = "mongodb://jonathan:Biomed#101@ds137003.mlab.com:37003/project3"

# # Pass connection to the pymongo instance.
# client = pymongo.MongoClient(connMLAB)

# # Connect to a database. Will create one if not already available.
# db = client.project3
#___________________________________________________________________________________

# app.config["MONGO_URI"] = 'mongodb://localhost:27017/Apple_y_y' or "mongodb://heroku_8nx1c4b9:gebgv4dmtcjvsgpgq8kbdd76g3@ds117623.mlab.com:17623/heroku_8nx1c4b9"
### app.config["MONGO_URI"] = "mongodb://heroku_8nx1c4b9:gebgv4dmtcjvsgpgq8kbdd76g3@ds117623.mlab.com:17623/heroku_8nx1c4b9"

mongo = PyMongo(app)

### Main - Landing Page - index.html
@app.route("/")
def index():
    
    # Get mars_news_data documents from database mars_db ( or heroku_8mh5bx8l ), collection mars_data
    mars_news_data = mongo.db.mars_data.find_one()
    
    return render_template("index.html", mars_news_data=mars_news_data)

### Scrape route that will execute mars_scrape functions
@app.route("/scrape")
def scrape_all_sites():

    #####mars_news_data = mongo.db.mars_data
    mars_news_data = scrape_mars.scrape_all_sites()

    # Insert mars_news_data into database collection mars_data
    mongo.db.mars_data.update({}, mars_news_data, upsert=True)
    
    # Redirect back to Landing Page
    ###return redirect("http://localhost:5000/", code=302)
    return redirect("/", code=302)
    
    ###return "Scraping was successful."

if __name__ == "__main__":
    ##print (scrape_mars.scrape_all_sites())
    # time.sleep(4)
    app.run(debug=True)    
