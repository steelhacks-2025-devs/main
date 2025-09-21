import pandas as pd
import os
import matplotlib.pyplot as plt

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
csv_file = os.path.join(BASE_DIR, 'datasets', 'final_dataset.csv')
finalframe = pd.read_csv(csv_file)

# Create a distribution plot of the livability scores
plt.figure(figsize=(10, 6))
plt.hist(finalframe['livability_score'], bins=20, alpha=0.7, color='skyblue', edgecolor='black')
plt.title('Distribution of Livability Scores', fontsize=16, fontweight='bold')
plt.xlabel('Livability Score', fontsize=12)
plt.ylabel('Frequency', fontsize=12)
plt.grid(True, alpha=0.3)

# Add mean and median to the plot
mean_score = finalframe['livability_score'].mean()
median_score = finalframe['livability_score'].median()
plt.axvline(mean_score, color='red', linestyle='--', linewidth=2, label=f'Mean: {mean_score:.2f}')
plt.axvline(median_score, color='orange', linestyle='--', linewidth=2, label=f'Median: {median_score:.2f}')
plt.legend()

plt.tight_layout()
plt.savefig(os.path.join(BASE_DIR, 'datasets', 'livability_score_distribution.png'), dpi=300, bbox_inches='tight')
plt.show()

print(f"Distribution statistics:")
print(f"Mean: {mean_score:.2f}")
print(f"Median: {median_score:.2f}")
print(f"Standard Deviation: {finalframe['livability_score'].std():.2f}")
print(f"Min: {finalframe['livability_score'].min():.2f}")
print(f"Max: {finalframe['livability_score'].max():.2f}