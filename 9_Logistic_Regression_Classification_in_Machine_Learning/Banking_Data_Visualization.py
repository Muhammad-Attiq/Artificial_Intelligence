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
url = "https://raw.githubusercontent.com/madmashup/targeted-marketing-predictive-engine/master/banking.csv"
data = pd.read_csv(url, header=0)
data = data.dropna()
data["education"] = np.where(data["education"] == "basic.9y", "Basic", data["education"])
data["education"] = np.where(data["education"] == "basic.6y", "Basic", data["education"])
data["education"] = np.where(data["education"].isnull(), 0, data["education"])
print(data["education"].value_counts())
sns.countplot(x="y", data=data, palette="hls")
plt.savefig("count_plot")
plt.show()
count_no_sub = len(data["education"] == 0)
count_sub = len(data["education"] == 1)
pct_of_no_sub = count_no_sub / (count_no_sub + count_sub)
print("percentage of no subscription is", pct_of_no_sub * 100)
pct_of_sub = count_sub / (count_no_sub + count_sub)
print("percentage of subscription", pct_of_sub * 100)
print(data.groupby("y").mean(numeric_only=True))
print(data.groupby("job").mean(numeric_only=True))
print(data.groupby("marital").mean(numeric_only=True))
print(data.groupby("education").mean(numeric_only=True))
