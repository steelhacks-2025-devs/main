# Imports
from sklearn.preprocessing import StandardScaler
from sklearn.decomposition import PCA
import pandas as pd

def pca_scoring(df):
    # Standardize features
    features = df.to_numpy()
    scaler = StandardScaler()
    scaled_features = scaler.fit_transform(features)

    # Apply PCA to the scaled data
    pca = PCA(n_components=1)
    principal_component = pca.fit_transform(scaled_features)

    # Add the score back to the original DataFrame
    df['livability_score'] = principal_component

    # Rank the data from best to worst
    return df.sort_values(by='livability_score', ascending=False)