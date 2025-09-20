import pandas as pd
import os


# Get csv file paths
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
# csv_files = [os.path.join(BASE_DIR, 'datasets', f'property-assessments-{i}.csv') for i in range(1, 5)]
csv_file = os.path.join(BASE_DIR, 'datasets', 'finalpt1.csv')
# Load the CSV file into a pandas DataFrame
print(f"Loading CSV file: {csv_file}")
global df
df = pd.read_csv(csv_file)

print(f"Original shape: {df.shape}")

def fix():
    df.drop('PROPERTYHOUSENUM', axis=1, inplace=True)

fix()

print(f"New shape: {df.shape}")

df.to_csv(os.path.join(BASE_DIR, 'datasets', 'finalpt2.csv'), index=False)