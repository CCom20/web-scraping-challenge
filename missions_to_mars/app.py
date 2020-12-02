from flask import Flask, render_template, redirect
from flask_pymongo import PyMongo
from selenium import webdriver
import scrape_mars
import pymongo

# Create an instance of our Flask app.
app = Flask(__name__)

# Create connection variable
app.config["MONGO_URI"] = "mongodb://localhost:27017/mars_db"
mongo = PyMongo(app)

@app.route('/')
def index():
    mars_db = mongo.db.mars_db.find_one()
    print(mars_db)

    # Return the template with the teams list passed in
    return render_template('index.html', mars=mars_db)

# Set route
@app.route('/scrape')
def scraper():
    mars_db = mongo.db.mars_db
    mars_data = scrape_mars.scrape()
    mars_db.update({}, mars_data, upsert=True)
    return redirect("/", code=302)


if __name__ == "__main__":
    app.run(debug=True)