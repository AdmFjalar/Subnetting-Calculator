from flask import Flask, render_template
from Subnetter import *
app = Flask(__name__)

@app.route('/subnet-explanations')
def HomeFunc():
    return render_template("subnet-explanations.html", network_address = "192.168.0.0", cidr=24)
@app.route('/about')
def AboutFunc():
    return "About"

if __name__ == "__main__":
    app.run(debug=True)