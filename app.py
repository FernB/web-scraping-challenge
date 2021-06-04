# Dependencies
from flask import Flask, render_template, redirect
from flask_pymongo import PyMongo
import scrape_mars

# Create instance of Flask
app = Flask(__name__)

# PyMongo to establish Mongo connection
mongo = PyMongo(app, uri="mongodb://localhost:27017/mars_app")


# Route to render index.html template using data from Mongo
@app.route("/")
def home():

    # Find one record of data from the mongo database
    
    mars_data = mongo.db.mars_data.find_one()

    # Return template and data
    return render_template("index.html", app_data=mars_data)


# Route that will trigger the scrape function
@app.route("/scrape")
def scrape():

    # call scrape and save the results to mongo
    mars_data = mongo.db.mars_data
    new_data = scrape_mars.scrape()
    mars_data.update({}, new_data, upsert=True)



    # Redirect back to home page
    return redirect("/")


if __name__ == "__main__":
    app.run(debug=True)