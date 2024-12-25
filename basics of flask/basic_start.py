from flask import Flask
from flask_cors import CORS

app = Flask(__name__)
CORS(app)

@app.route("/")
def index():
    return "<h1> Hello Puppy! </h1>"

@app.route("/information")
def info():
    return "<h1> The puppies are cute </h1>"

@app.route("/puppy/<name>")
def puppy(name):
    return "<h1>The puppy name is {}".format(name.upper())

if __name__== "__main__":
    app.run(debug=True)