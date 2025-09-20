import pandas as pd
import os


# Get csv file paths
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
csv_files = [os.path.join(BASE_DIR, 'datasets', f'property-assessments-{i}.csv') for i in range(1, 5)]

df1 = pd.read_csv(csv_files[0])
df2 = pd.read_csv(csv_files[1])
df3 = pd.read_csv(csv_files[2])
df4 = pd.read_csv(csv_files[3])

result = pd.concat([df1, df2, df3, df4], ignore_index=True)

# Get csv file path
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
output_csv = os.path.join(BASE_DIR, 'datasets', 'property-assessments-combined.csv')

result.to_csv(output_csv)