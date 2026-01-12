import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
from sklearn.datasets import fetch_california_housing
import warnings
warnings.filterwarnings('ignore')

def run_eda():
    print("=" * 70)
    print("LOADING CALIFORNIA HOUSING DATASET")
    print("=" * 70)
    
    # Load dataset
    housing = fetch_california_housing()
    df = pd.DataFrame(housing.data, columns=housing.feature_names)
    df['Price'] = housing.target
    
    # Save dataset
    df.to_csv('data/housing.csv', index=False)
    print(f"✅ Dataset saved: data/housing.csv")
    print(f"✅ Shape: {df.shape}")
    print(f"✅ Rows: {df.shape[0]:,}")
    print(f"✅ Columns: {df.shape[1]}")
    
    # Display basic info
    print("\n" + "=" * 70)
    print("FIRST 5 ROWS")
    print("=" * 70)
    print(df.head())
    
    print("\n" + "=" * 70)
    print("DATASET INFO")
    print("=" * 70)
    print(df.info())
    
    print("\n" + "=" * 70)
    print("STATISTICAL SUMMARY")
    print("=" * 70)
    print(df.describe())
    
    print("\n" + "=" * 70)
    print("MISSING VALUES")
    print("=" * 70)
    print(df.isnull().sum())
    
    print("\n" + "=" * 70)
    print("CORRELATION WITH PRICE")
    print("=" * 70)
    correlations = df.corr()['Price'].sort_values(ascending=False)
    print(correlations)
    
    # Create visualizations
    print("\n" + "=" * 70)
    print("CREATING VISUALIZATIONS")
    print("=" * 70)
    
    plt.style.use('seaborn-v0_8-darkgrid')
    
    # 1. Price distribution
    plt.figure(figsize=(10, 6))
    plt.hist(df['Price'], bins=50, edgecolor='black', color='skyblue')
    plt.xlabel('Price (in $100,000)', fontsize=12)
    plt.ylabel('Frequency', fontsize=12)
    plt.title('Distribution of House Prices', fontweight='bold', fontsize=14)
    plt.grid(axis='y', alpha=0.3)
    plt.tight_layout()
    plt.savefig('data/price_distribution.png', dpi=300)
    print("✅ Saved: data/price_distribution.png")
    plt.close()
    
    # 2. Correlation heatmap
    plt.figure(figsize=(12, 8))
    sns.heatmap(df.corr(), annot=True, fmt='.2f', cmap='coolwarm', center=0, square=True)
    plt.title('Feature Correlation Matrix', fontweight='bold', fontsize=14)
    plt.tight_layout()
    plt.savefig('data/correlation_heatmap.png', dpi=300)
    print("✅ Saved: data/correlation_heatmap.png")
    plt.close()
    
    # 3. Pairplot
    print("⏳ Creating pairplot (this may take a minute)...")
    key_features = ['MedInc', 'HouseAge', 'AveRooms', 'Price']
    pairplot = sns.pairplot(df[key_features], diag_kind='kde', height=2.5)
    pairplot.fig.suptitle('Key Features Relationship', y=1.02, fontweight='bold', fontsize=14)
    plt.tight_layout()
    plt.savefig('data/pairplot.png', dpi=300)
    print("✅ Saved: data/pairplot.png")
    plt.close()
    
    # 4. Boxplots (FIXED)
    print("⏳ Creating boxplots...")
    num_cols = len(df.columns)
    num_rows = (num_cols + 3) // 4  # Calculate rows needed
    
    fig, axes = plt.subplots(num_rows, 4, figsize=(16, num_rows * 4))
    fig.suptitle('Feature Distributions and Outliers', fontweight='bold', fontsize=16)
    
    # Flatten axes array for easier indexing
    axes = axes.flatten()
    
    for idx, col in enumerate(df.columns):
        axes[idx].boxplot(df[col], vert=True)
        axes[idx].set_title(col, fontweight='bold')
        axes[idx].grid(axis='y', alpha=0.3)
    
    # Hide empty subplots
    for idx in range(num_cols, len(axes)):
        axes[idx].axis('off')
    
    plt.tight_layout()
    plt.savefig('data/boxplots.png', dpi=300)
    print("✅ Saved: data/boxplots.png")
    plt.close()
    
    print("\n" + "=" * 70)
    print("✅ EDA COMPLETE!")
    print("=" * 70)
    print("\n💡 Next: python src/data_preprocessing.py")

if __name__ == "__main__":
    run_eda()