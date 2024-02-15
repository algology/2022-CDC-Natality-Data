import sqlite3
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

# Connect to the SQLite database
conn = sqlite3.connect('natality_data.db')

# Query to extract mothers' and fathers' ages
query = "SELECT mothers_age, fathers_age FROM natality_data;"
df = pd.read_sql_query(query, conn)
conn.close()

# Convert age fields from string to numeric (integers)
df['mothers_age'] = pd.to_numeric(df['mothers_age'], errors='coerce')
df['fathers_age'] = pd.to_numeric(df['fathers_age'], errors='coerce')

# Drop rows with NaN values and where father's age is 99 (unknown)
df.dropna(subset=['mothers_age', 'fathers_age'], inplace=True)
df = df[df['fathers_age'] != 99]

# Determine a common bin size based on the range of ages
bins = range(int(df[['mothers_age', 'fathers_age']].min().min()), 
             int(df[['mothers_age', 'fathers_age']].max().max()) + 1, 
             1)  # Bin width of 1 year

# Seaborn styling
sns.set(style="whitegrid")

# Create plot
plt.figure(figsize=(12, 8))

# Histogram for mothers' ages with KDE
sns.histplot(df['mothers_age'], bins=bins, kde=True, color='skyblue', label='Mothers Age', alpha=0.6, kde_kws={'bw_adjust': 2})

# Histogram for fathers' ages with KDE
sns.histplot(df['fathers_age'], bins=bins, kde=True, color='salmon', label='Fathers Age', alpha=0.6, kde_kws={'bw_adjust': 2})

# Mean ages
mean_mothers_age = df['mothers_age'].mean()
mean_fathers_age = df['fathers_age'].mean()

# Add vertical lines for mean ages
plt.axvline(mean_mothers_age, color='blue', linestyle='dashed', linewidth=1.5, label=f'Mean Mothers Age: {mean_mothers_age:.2f}')
plt.axvline(mean_fathers_age, color='red', linestyle='dashed', linewidth=1.5, label=f'Mean Fathers Age: {mean_fathers_age:.2f}')

# Customizing the plot
plt.title('Distribution of Mothers\' and Fathers\' Ages', fontsize=16)
plt.xlabel('Age', fontsize=14)
plt.ylabel('Frequency', fontsize=14)
plt.legend()

plt.tight_layout()
plt.show()
