# Imports
from sklearn.preprocessing import StandardScaler, MinMaxScaler
from sklearn.decomposition import PCA
import pandas as pd
import os

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
csv_file = os.path.join(BASE_DIR, 'datasets', 'finalpt6.csv')
df = pd.read_csv(csv_file)

df = df.set_index('PROPERTYADDRESS')

# condition : rank (1, 7, 2, 3, 4, 5, 8, 6 is conditions from best to worst)
scale_mapping = {
    1: 1, 
    7: 2, 
    2: 3, 
    3: 4, 
    4: 5,
    5: 6, 
    8: 7, 
    6: 8
}

df['CONDITION'] = df['CONDITION'].map(scale_mapping)
df['CONDITION_FLIPPED'] = -df['CONDITION']
df['STORIES_FLIPPED'] = -df['STORIES']

X = df[['STORIES_FLIPPED', 'CONDITION_FLIPPED', 'TOTALROOMS', 'FINISHEDLIVINGAREA']]

def pca_scoring(df):# Load the dataset
    # Standardize features
    features = df.to_numpy()
    scaler = StandardScaler()
    scaled_features = scaler.fit_transform(features)

    # Apply PCA to the scaled data
    pca = PCA(n_components=1)
    principal_component = pca.fit_transform(scaled_features)

    # Add the score back to the original DataFrame
    df['livability_score'] = principal_component


    minmaxscaler = MinMaxScaler(feature_range=(0, 100))
    df['livability_score'] = minmaxscaler.fit_transform(df['livability_score'].values.reshape(-1, 1)).flatten()
    # Rank the data from best to worst
    return df.sort_values(by='livability_score', ascending=False)

print(pca_scoring(X))