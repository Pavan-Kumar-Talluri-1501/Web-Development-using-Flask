from flask import Flask, render_template

app = Flask(__name__)

@app.route('/<value>')
def index(value):
    name = "tommy"
    letters = list(name)
    pup_dict = {"pup_name": "Max"}
    user_login = value
    pup_names = ["Max", "Snoopy", "Tommy"]
    return  render_template('basic.html', dog_name = name, letters_count = letters, dog_dict = pup_dict, user_login = user_login, dog_names = pup_names)

if __name__ == "__main__":
    app.run(debug=True)