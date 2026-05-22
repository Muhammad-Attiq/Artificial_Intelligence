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
url = "https://raw.githubusercontent.com/madmashipu/targeted-marketing-predictive-engine/master/banking.csv"
data = pd.read_csv(url, header=0)
data = data.dropna()
data["education"] = np.where(data["education"] == "basic.9y", "Basic", data["education"])
data["education"] = np.where(data["education"] == "basic.6y", "Basic", data["education"])
data["education"] = np.where(data["education"].isnull(), "Basic", data["education"])
cat_vars = ["job", "marital", "education", "default", "housing", "loan", "contact", "month", "day_of_week", "poutcome"]
for var in cat_vars:
    cat_list = pd.get_dummies(data[var], prefix=var)
    data = data.join(cat_list)
data_vars = data.columns.values.tolist()
to_keep = [i for i in data_vars if i not in cat_vars]
data_final = data[to_keep]
print(data_final.columns.values)
