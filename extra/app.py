from flask import Flask, render_template, jsonify, redirect
from flask_pymongo import PyMongo
import time

# Import my mars web scraping python script
import scrape_mars

# Create application with Flask
app = Flask(__name__)

# Set up mongo connection with PyMongo
app.config["MONGO_URI"] = "mongodb://localhost:27017/mars_db"
mongo = PyMongo(app)


### Main - Landing Page - index.html
@app.route("/")
def index():
    
    # Get mars_news_data documents from database mars_db, collection mars_data
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
