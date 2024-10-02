from flask import Blueprint, render_template, request, session

# Use of blue print to group routes, 
# name - first argument is the blue print name 
# import name - second argument - helps identify the root url for it 
mainbp = Blueprint('main', __name__)

@mainbp.route('/')
def index():
    if 'email' in session:
        str = f"Welcome to the Travel App, {session['email']}"
    else: 
        str = "<h1>Hello World</h1>"
    return render_template('index.html')
