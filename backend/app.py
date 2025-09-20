# Import necessary modules from Flask
from flask import Flask, render_template, request, redirect, url_for, flash
import os

# init flask
app = Flask(__name__, template_folder='../frontend')

@app.route('/')
def home():
    return render_template('index.html')

# Run the Flask server
if __name__ == '__main__':
    app.run(host='127.0.0.1', port=5000)
