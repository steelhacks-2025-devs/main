# Import necessary modules from Flask
from flask import Flask, render_template, request, redirect, url_for, flash
import os
import pandas as pd

# init flask
app = Flask(__name__, template_folder='../frontend')

@app.route('/')
def home():
    # Get csv file path
    BASE_DIR = os.path.dirname(os.path.abspath(__file__))
    neighborhoods_csv = os.path.join(BASE_DIR, 'datasets', 'Pittsburgh_Neighborhoods.csv')

    # Read PGH neighborhoods into a DataFrame
    df = pd.read_csv(neighborhoods_csv)

    # Get all neighborhoods
    neighborhoods = df['hood']

    return render_template('index.html', neighborhood_options=neighborhoods)

# Run the Flask server
if __name__ == '__main__':
    app.run(host='127.0.0.1', port=5000, debug=True)
