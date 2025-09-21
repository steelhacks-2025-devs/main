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

# Bell curve score for price, median homes are ranked higher as a sweet spot for affordability and quality
target_price = df['FAIRMARKETTOTAL'].median()
print(f"median FMV price: {target_price}")
price_distance = abs(df['FAIRMARKETTOTAL'] - target_price)
max_distance = price_distance.max()

# Convert to score where closer to median = higher score
df['price_bell_score'] = 1 - (price_distance / max_distance)

# # Bell curve score for home size, seniors want a comfortable but not overly large home
# target_price = df['FINISHEDLIVINGAREA'].median()
# print(f"median FMV price: {target_price}")
# price_distance = abs(df['FINISHEDLIVINGAREA'] - target_price)
# max_distance = price_distance.max()

# # Convert to score where closer to median = higher score
# df['house_size_bell_score'] = 1 - (price_distance / max_distance)


X = df[['STORIES_FLIPPED', 'CONDITION_FLIPPED', 'price_bell_score', "FINISHEDLIVINGAREA"]]

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
pd.set_option('display.max_columns', None)
print(pca_scoring(X))