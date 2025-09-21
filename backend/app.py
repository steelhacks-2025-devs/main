# Import necessary modules from Flask
from flask import Flask, render_template, request, redirect, url_for, flash
import os
import pandas as pd
# from prox import count_amenities_by_distance
from pca import pca_scoring

# init flask
app = Flask(__name__, template_folder='../frontend', static_folder='../frontend/static')

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

@app.route('/find')
def find():
    # Get csv file path
    BASE_DIR = os.path.dirname(os.path.abspath(__file__))
    property_csv = os.path.join(BASE_DIR, 'datasets', 'finalpt5.csv')

    # Read PGH property into a DataFrame
    df = pd.read_csv(property_csv)

    neighborhood = request.form.get('neighborhood-list')
    print(pca_scoring(df[df['NEIGHBORHOOD'] == neighborhood]))
    
    return render_template('find.html')

@app.route('/results', methods=['POST'])
def results():
    print(request.form)
    # Get neighborhood selected by user on index page
    selected_neighborhood = request.form.get('neighborhood-list')
    print(selected_neighborhood)

    # Get csv file path
    BASE_DIR = os.path.dirname(os.path.abspath(__file__))
    property_csv = os.path.join(BASE_DIR, 'datasets', 'finalpt5.csv')

    # Read PGH property into a DataFrame
    df = pd.read_csv(property_csv)

    print(df['NEIGHDESC'])
    print(df[df['NEIGHDESC'] == selected_neighborhood.upper()].head())
    
    # # Example count_amenities_by_distance call
    # test_row = df[0]
    # for amenity in ['hospital', 'transportation']:
    #     print(count_amenities_by_distance(f'{test_row['PROPERTYHOUSENUM']} {test_row['PROPERTYADDRESS']}, Pittsburgh, PA {test_row['PROPERTYZIP']}', amenity, [1, 3, 5]))

    return render_template('results.html', neighborhood=selected_neighborhood)

# Run the Flask server
if __name__ == '__main__':
    app.run(host='127.0.0.1', port=5000, debug=True)
