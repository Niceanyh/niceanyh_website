from flask import Flask,render_template
import requests
import json

app = Flask( # Create a flask app
__name__,
template_folder='templates', # Name of html file folder
static_folder='static' # Name of directory for static files
)

@app.route("/")
def index():
    return render_template('index.html')

@app.route('/hello')
def hello():
    return "hello"

#app.run(host='127.0.0.1',port=0)
if __name__ == "__main__": # Makes sure this is the main process
    # Starts the site
    app.run(host='127.0.0.1',port=5000)