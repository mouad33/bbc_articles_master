from flask import Flask, render_template,request,redirect,url_for # For flask implementation


from flask import Flask
from flask_pymongo import PyMongo
from pymongo import MongoClient




app = Flask(__name__ , template_folder='templates')
app.config["MONGO_URI"] = "mongodb://localhost:27017/bbc_articles"
mongo = PyMongo(app)

	   

@app.route("/")
def home_page():
    res= mongo.db.articles.find()
    return render_template("index.html",
        res=res)
		   
		   
		   

if __name__ == "__main__":

    app.run()