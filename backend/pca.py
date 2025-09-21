from sklearn.preprocessing import StandardScaler, MinMaxScaler
from sklearn.decomposition import PCA
import pandas as pd
import os

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
csv_file = os.path.join(BASE_DIR, 'datasets', 'finalpt7.csv')
df = pd.read_csv(csv_file)

df = df.set_index('PROPERTYADDRESS') # index by address

# condition : the dataset we used ranks house conditions from best to worst as: (1, 7, 2, 3, 4, 5, 8, 6)
condition_scale_mapping = {
    1: 1, 
    7: 2, 
    2: 3, 
    3: 4, 
    4: 5,
    5: 6, 
    8: 7, 
    6: 8
}

df['CONDITION'] = df['CONDITION'].map(condition_scale_mapping) # map conditions to actual ranking from best to worst
df['CONDITION_FLIPPED'] = -df['CONDITION'] # flip the condition so that lower ranked scores are better (closer to #1)
df['STORIES_FLIPPED'] = -df['STORIES'] # flip the stories so that lower ranked scores are better (closer to 1 story, the best option for seniors)

# Bell curve score for price, homes closer to median price are ranked higher as a sweet spot for affordability and quality
target_price = df['FAIRMARKETTOTAL'].median()
print(f"median FMV price: {target_price}")
price_distance = abs(df['FAIRMARKETTOTAL'] - target_price)
max_distance = price_distance.max()
# Convert to score where closer to median = higher score
df['price_bell_score'] = 1 - (price_distance / max_distance)

# Bell curve score for home size, homes closer to median size are ranked higher as seniors want a comfortable but not overly large home
target_sqft = df['FINISHEDLIVINGAREA'].median()
print(f"median size: {target_sqft}")
price_distance = abs(df['FINISHEDLIVINGAREA'] - target_sqft)
max_distance = price_distance.max()
# Convert to score where closer to median = higher score
df['house_size_bell_score'] = 1 - (price_distance / max_distance)

# ---------------------------------- PCA Calculation ----------------------------------
# Principal Component Analysis will be used to create a "livability score" of the properties.
# The features that will be used are:
# - Stories Flipped: lower ranked stories are better
# - Condition Flipped: lower ranked conditions are better
# - Price Bell Score: homes closer to median price are ranked higher
# - House Size Bell Score: homes closer to median size are ranked higher
# - Medical Proximity: homes closer to medical amenities are ranked higher
# - Grocery Proximity: homes closer to grocery amenities are ranked higher
# - Recreation Proximity: homes closer to recreation amenities are ranked higher
# - Entertainment Proximity: homes closer to entertainment amenities are ranked higher
#
X = df[['STORIES_FLIPPED', 'CONDITION_FLIPPED', 'price_bell_score', "house_size_bell_score", "medical_prox_score", "grocery_prox_score", "recreation_prox_score", "entertainment_prox_score"]]

# Calculate the livability score with PCA
def pca_scoring(df):
    # Standardize features with StandardScaler
    features = df.to_numpy()
    scaler = StandardScaler()
    scaled_features = scaler.fit_transform(features)

    # Apply PCA to the scaled data - 1 component creates a "composite score" of the features, our livability score
    pca = PCA(n_components=1)
    principal_component = pca.fit_transform(scaled_features)

    # Add the score back to the original DataFrame
    df['livability_score'] = principal_component

    # MinMaxScaler to scale the score to a range of 0-100
    minmaxscaler = MinMaxScaler(feature_range=(0, 100))
    df['livability_score'] = minmaxscaler.fit_transform(df['livability_score'].values.reshape(-1, 1)).flatten()

    # Rank the data from best to worst
    return df.sort_values(by='livability_score', ascending=False)
# pd.set_option('display.max_columns', None)
finalframe = pca_scoring(X)
print(finalframe)
# Merge finalframe with the original df to get all columns
# Reset index to ensure proper merging
finalframe_reset = finalframe.reset_index(drop=True)
df_reset = df.reset_index(drop=False) #keep address index

# Merge the dataframes
merged_df = pd.concat([df_reset, finalframe_reset], axis=1)
# Remove duplicate columns (keep the first occurrence)
merged_df = merged_df.loc[:, ~merged_df.columns.duplicated()]
print(merged_df.columns)
# Set PROPERTYADDRESS as the index and save to CSV
merged_df.set_index('PROPERTYADDRESS').to_csv(os.path.join(BASE_DIR, 'datasets', 'final_dataset.csv'))