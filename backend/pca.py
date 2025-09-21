# Imports
from sklearn.preprocessing import StandardScaler, MinMaxScaler
from sklearn.decomposition import PCA
import pandas as pd
import os
import matplotlib.pyplot as plt

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
csv_file = os.path.join(BASE_DIR, 'datasets', 'finalpt7.csv')
df = pd.read_csv(csv_file)

df = df.set_index('PROPERTYADDRESS')

# condition : rank (1, 7, 2, 3, 4, 5, 8, 6 is conditions from best to worst)
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

df['CONDITION'] = df['CONDITION'].map(condition_scale_mapping)
df['CONDITION_FLIPPED'] = -df['CONDITION']
df['STORIES_FLIPPED'] = -df['STORIES']

# Bell curve score for price, median homes are ranked higher as a sweet spot for affordability and quality
target_price = df['FAIRMARKETTOTAL'].median()
print(f"median FMV price: {target_price}")
price_distance = abs(df['FAIRMARKETTOTAL'] - target_price)
max_distance = price_distance.max()
# Convert to score where closer to median = higher score
df['price_bell_score'] = 1 - (price_distance / max_distance)

# Bell curve score towards 75th percentile for home size, seniors want a comfortable but not overly large home
target_price = df['FINISHEDLIVINGAREA'].median()
print(f"median FMV price: {target_price}")
price_distance = abs(df['FINISHEDLIVINGAREA'] - target_price)
max_distance = price_distance.max()
# Convert to score where closer to median = higher score
df['house_size_bell_score'] = 1 - (price_distance / max_distance)

X = df[['STORIES_FLIPPED', 'CONDITION_FLIPPED', 'price_bell_score', "house_size_bell_score", "medical_prox_score", "grocery_prox_score", "recreation_prox_score", "entertainment_prox_score"]]

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
# pd.set_option('display.max_columns', None)
finalframe = pca_scoring(X)
print(finalframe)
# Merge finalframe with the original df to get all columns
# Reset index to ensure proper merging
finalframe_reset = finalframe.reset_index(drop=True)
df_reset = df.reset_index(drop=False)

# Merge the dataframes
merged_df = pd.concat([df_reset, finalframe_reset], axis=1)

# Remove duplicate columns (keep the first occurrence)
merged_df = merged_df.loc[:, ~merged_df.columns.duplicated()]
print(merged_df.columns)
# Set PROPERTYADDRESS as the index and save to CSV
merged_df.set_index('PROPERTYADDRESS').to_csv(os.path.join(BASE_DIR, 'datasets', 'final_dataset.csv'))




# finalframe = pd.read_csv(os.path.join(BASE_DIR, 'datasets', 'finalfinalpt2.csv'))
# # Create a distribution plot of the livability scores
# plt.figure(figsize=(10, 6))
# plt.hist(finalframe['livability_score'], bins=20, alpha=0.7, color='skyblue', edgecolor='black')
# plt.title('Distribution of Livability Scores', fontsize=16, fontweight='bold')
# plt.xlabel('Livability Score', fontsize=12)
# plt.ylabel('Frequency', fontsize=12)
# plt.grid(True, alpha=0.3)

# # Add some statistics to the plot
# mean_score = finalframe['livability_score'].mean()
# median_score = finalframe['livability_score'].median()
# plt.axvline(mean_score, color='red', linestyle='--', linewidth=2, label=f'Mean: {mean_score:.2f}')
# plt.axvline(median_score, color='orange', linestyle='--', linewidth=2, label=f'Median: {median_score:.2f}')
# plt.legend()

# plt.tight_layout()
# plt.savefig(os.path.join(BASE_DIR, 'datasets', 'livability_score_distribution.png'), dpi=300, bbox_inches='tight')
# plt.show()

# print(f"Distribution statistics:")
# print(f"Mean: {mean_score:.2f}")
# print(f"Median: {median_score:.2f}")
# print(f"Standard Deviation: {finalframe['livability_score'].std():.2f}")
# print(f"Min: {finalframe['livability_score'].min():.2f}")
# print(f"Max: {finalframe['livability_score'].max():.2f}")
