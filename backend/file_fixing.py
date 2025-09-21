import pandas as pd
import os


# Get csv file paths
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
# csv_files = [os.path.join(BASE_DIR, 'datasets', f'property-assessments-{i}.csv') for i in range(1, 5)]
csv_file = os.path.join(BASE_DIR, 'datasets', 'finalpt6.csv')
zipcode_centroids_file = os.path.join(BASE_DIR, 'datasets', 'zipcode_centroid_proximity_scores.csv')
# Load the CSV file into a pandas DataFrame
print(f"Loading CSV file: {csv_file}")

global df
df = pd.read_csv(csv_file)
zipcode_centroids = pd.read_csv(zipcode_centroids_file)

# Merge df with zipcode_centroids based on matching LAT and LON coordinates
df = df.merge(zipcode_centroids[['LAT', 'LON', 'medical_prox_score', 
                                'grocery_prox_score', 'recreation_prox_score', 'entertainment_prox_score']], 
              on=['LAT', 'LON'], 
              how='left')

# Check if all zipcode_centroids STD_ZIP5 are contained in df PROPERTYZIP
# zipcode_centroids_set = set(zipcode_centroids['STD_ZIP5'])
# df_propertyzip_set = set(df['PROPERTYZIP'])
# missing_in_centroids = df_propertyzip_set - zipcode_centroids_set

# print(f"Original shape: {df.shape}")

# # Drop rows where PROPERTYZIP is in missing_in_centroids
# df = df[~df['PROPERTYZIP'].isin(missing_in_centroids)]
# print(f"Shape after dropping missing zipcodes: {df.shape}")

# # Merge df with zipcode_centroids to add LAT and LON columns
# df = df.merge(zipcode_centroids[['STD_ZIP5', 'LAT', 'LON']], 
#             left_on='PROPERTYZIP', 
#             right_on='STD_ZIP5', 
#             how='left')

# # Drop the redundant STD_ZIP5 column
# df = df.drop('STD_ZIP5', axis=1)

print(f"New shape: {df.shape}")
print(f"head: {df.head()}")

df.to_csv(os.path.join(BASE_DIR, 'datasets', 'finalpt7.csv'), index=False)