import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
import seaborn as sns
from sklearn.linear_model import LogisticRegression
from sklearn.model_selection import train_test_split
from sklearn import preprocessing
plt.rc("font", size=14)
sns.set(style="white")
sns.set(style="whitegrid", color_codes=True)
url = "https://raw.githubusercontent.com/madhashup/targeted-marketing-predictive-engine/master/banking.csv"
data = pd.read_csv(url, header=0)
data = data.dropna()
print("Initial Dataset Shape:", data.shape)
print("Columns in dataset:", list(data.columns))
print("Unique education categories before grouping:", data["education"].unique())
data["education"] = np.where(data["education"] == "basic.9y", "Basic", data["education"])
data["education"] = np.where(data["education"] == "basic.6y", "Basic", data["education"])
data["education"] = np.where(data["education"].str.contains("basic.4y", case=False) | data["education"].str.contains("basic.5y", case=False), "Basic", data["education"])
print("Unique education categories after grouping:", data["education"].unique())
print(data.head())
