from flask import Flask, render_template, redirect
from flask_pymongo import PyMongo
import scrape_mars

# Create an instance of our Flask app.
app = Flask(__name__)

# Create connection variable
mongo = PyMongo(app, uri="mongodb://localhost:27017/mars_app")

# Set route
@app.route('/')
def index():
    mars_data = mongo.db.mars_data.find_one()
    # Store the entire team collection in a list
    # Return the template with the teams list passed in
    return render_template('index.html', mars_data=mars_data)

@app.route('/scrape')
def scrape():
    mars_data = mongo.db.mars_data
    mars_info = scrape_mars.scrape()
    mars_data.update({},mars_info,upsert = True)
    return redirect("/", code=302)



if __name__ == "__main__":
    app.run(debug=True)
