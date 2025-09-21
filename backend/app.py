# Import necessary modules from Flask
from flask import Flask, render_template, request, redirect, url_for, flash
import os
import pandas as pd
# from prox import count_amenities_by_distance
# from pca import pca_scoring

# init flask
app = Flask(__name__, template_folder='../frontend', static_folder='../frontend/static')

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/find')
def find():
    return render_template('find.html')

@app.route('/results', methods=['POST'])
def results():
    # Get price range selected by user on index page
    price_range = request.form.get('price-range')

    # Get csv file path
    BASE_DIR = os.path.dirname(os.path.abspath(__file__))
    property_csv = os.path.join(BASE_DIR, 'datasets', 'finalpt6.csv')

    # Read PGH properties into a DataFrame
    df = pd.read_csv(property_csv)

    # Price conditionals based on dropdown choice
    if (price_range == '0-100'):
        print(df[df['FAIRMARKETTOTAL'] < 100_000]['FAIRMARKETTOTAL'])
    elif (price_range == '100-250'):
        print(df[(df['FAIRMARKETTOTAL'] >= 100_000) & (df['FAIRMARKETTOTAL'] < 250_000)]['FAIRMARKETTOTAL'])
    elif (price_range == '250-500'):
        print(df[(df['FAIRMARKETTOTAL'] >= 250_000) & (df['FAIRMARKETTOTAL'] < 500_000)]['FAIRMARKETTOTAL'])
    elif (price_range == '500+'):
        print(df[df['FAIRMARKETTOTAL'] >= 500_000]['FAIRMARKETTOTAL'])
    
    return render_template('results.html', price_range_chosen=price_range)

# Run the Flask server
if __name__ == '__main__':
    app.run(host='127.0.0.1', port=5000, debug=True)
