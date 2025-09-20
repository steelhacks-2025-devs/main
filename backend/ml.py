import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from sklearn.cluster import KMeans

metrics = [
    'walk_score',
    'price',
    'medical_proximity',
    'grocery_proximity',
    'park_proximity',
    'entertainment_proximity',
    'is_senior_living'
]

kmeans = KMeans(n_clusters=4).fit(data) #TODO: Choose n_clusters and collect data to cluster!

#TODO: Have DataFrame of predictive features, add cluster labels
df['cluster'] = kmeans.labels_

# Find averages of each feature that falls under each cluster to understand categories
cluster_summary = df.groupby('cluster').mean()
print(cluster_summary)

# Mapping dict
# Example:
category_mapping = {
    0: 'Walkable & Affordable',
    1: 'Access to Medical Care' # ... etc
}

# Assign categoires based on determined cluster categories
df['category'] = df['cluster'].map(category_mapping)

