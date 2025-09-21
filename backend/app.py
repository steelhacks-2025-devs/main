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
    # Get criteria selected by user on index page
    min_price = int(request.form.get('min_price'))
    max_price = int(request.form.get('max_price'))
    

    # Get csv file path
    BASE_DIR = os.path.dirname(os.path.abspath(__file__))
    property_csv = os.path.join(BASE_DIR, 'datasets', 'finalpt6.csv')

    # Read PGH properties into a DataFrame
    df = pd.read_csv(property_csv)

    # Get data within price range
    print(df[(df['FAIRMARKETTOTAL'] >= min_price) & (df['FAIRMARKETTOTAL'] < max_price)]['FAIRMARKETTOTAL'])
    
    return render_template('results.html', price_range_chosen=f'${min_price:,} - ${max_price:,}')

# Run the Flask server
if __name__ == '__main__':
    app.run(host='127.0.0.1', port=5000, debug=True)
