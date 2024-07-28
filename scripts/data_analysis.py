import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

# Plot style settings
sns.set(style='whitegrid')
plt.rcParams['figure.figsize'] = (12, 6)
plt.rcParams['font.size'] = 12

# Load data
df = pd.read_csv('Walmart_cleaned.csv')

# Remove textual columns not used in the model
df.drop(columns=['User_ID', 'Product_ID'], inplace=True)

# Check and clean the data
df.dropna(inplace=True)

# Convert columns to appropriate types
numeric_cols = ['Purchase', 'Occupation', 'Product_Category']
df[numeric_cols] = df[numeric_cols].apply(pd.to_numeric, errors='coerce')
df.dropna(inplace=True)

# Function to add labels to bars
def add_labels(ax):
    for p in ax.patches:
        ax.annotate(f'{p.get_height():,.0f}', (p.get_x() + p.get_width() / 2, p.get_height()),
                    ha='center', va='bottom', fontsize=8)

# Function to plot categorical variable distribution
def plot_categorical_distribution(df, var):
    plt.figure()
    ax = sns.countplot(data=df, x=var, palette='muted', hue=var)
    add_labels(ax)
    plt.title(f'{var} Distribution', fontsize=14)
    plt.xlabel(var, fontsize=12)
    plt.ylabel('Count', fontsize=12)
    plt.xticks(rotation=45)
    if var == 'City_Category':
        legend_labels = ['A - Large metropolitan cities', 'B - Smaller cities', 'C - Rural areas']
    elif var == 'Gender':
        legend_labels = ['Female', 'Male']
    elif var == 'Marital_Status':
        legend_labels = ['Single', 'Married']
    else:
        legend_labels = df[var].unique()
    plt.legend(title=var, labels=legend_labels)
    plt.tight_layout()
    plt.show()

# Exploratory Data Analysis (EDA)

# Descriptive statistics
print("Descriptive Statistics:")
print(df.describe())

# Distribution of categorical variables
categorical_vars = ['Gender', 'Age', 'City_Category', 'Stay_In_Current_City_Years', 'Marital_Status']

for var in categorical_vars:
    plot_categorical_distribution(df, var)

# Correlation matrix for numeric columns
plt.figure()
sns.heatmap(df[numeric_cols].corr(), annot=True, cmap='coolwarm', linewidths=0.5)
plt.title('Correlation Matrix', fontsize=14)
plt.tight_layout()
plt.show()

# Customer segmentation based on product category
plt.figure()
ax = sns.countplot(x='Product_Category', hue='Gender', data=df, palette='muted')
add_labels(ax)
plt.title('Customer Segmentation Based on Product Category', fontsize=14)
plt.xlabel('Product Category', fontsize=12)
plt.ylabel('Number of Purchases', fontsize=12)
plt.xticks(rotation=45)
plt.legend(title='Gender', bbox_to_anchor=(1.05, 1), loc='upper left', labels=['Female', 'Male'])
plt.tight_layout()
plt.show()

print('Data analysis completed.')
