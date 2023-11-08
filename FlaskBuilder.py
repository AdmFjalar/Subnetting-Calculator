from flask import Flask, render_template, url_for
from Subnetter import *

app = Flask(__name__)

@app.route('/subnet-explanations')
def HomeFunc():
    # Define the data you want to pass to the template
    network_address = "192.168.0.0"
    cidr = 24

    # Pass the data to the template
    return render_template("subnet-explanations.html", network_address=network_address, cidr=cidr)

@app.route('/about')
def AboutFunc():
    return "About"

if __name__ == "__main__":
    app.run(debug=True)
