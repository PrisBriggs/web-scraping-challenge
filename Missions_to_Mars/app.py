from flask import Flask, render_template, redirect
from flask_pymongo import PyMongo
import flask_pymongo as fp
import scrape_mars

app = Flask(__name__)

# Use flask_pymongo to set up mongo connection
app.config["MONGO_URI"] = "mongodb://localhost:27017/mars_app"
mongo = PyMongo(app)

@app.route("/")
def index():
    # find the documents from our mongo db and return it.
    listings = mongo.db.listings.find()
    # pass that listing to render_template
    return render_template("index.html", listings=listings)


# set our path to /scrape
@app.route("/scrape")
def scraper():
    print("scraping results: ")
    # create a listings database
    listings = mongo.db.listings
    # call the scrape function in our scrape_mars file. This will scrape and save to mongo.
    listings_data = scrape_mars.scrape()
    # update our listings with the data that is being scraped.
    listings.insert_one(listings_data)
    # return a message to our page so we know it was successful.
    return redirect("/", code=302)


if __name__ == "__main__":
    app.run(debug=True)
