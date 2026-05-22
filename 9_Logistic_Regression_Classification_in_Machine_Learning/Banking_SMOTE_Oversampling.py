import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
import seaborn as sns
from sklearn.linear_model import LogisticRegression
from sklearn.model_selection import train_test_split
from sklearn import preprocessing
from imblearn.over_sampling import SMOTE
plt.rc("font", size=14)
sns.set(style="white")
sns.set(style="whitegrid", color_codes=True)
url = "https://raw.githubusercontent.com/madmashup/targeted-marketing-predictive-engine/master/banking.csv"
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
X = data_final.loc[:, data_final.columns != "y"]
y = data_final.loc[:, data_final.columns == "y"].values.ravel()
os = SMOTE(random_state=0)
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.3, random_state=0)
columns = X_train.columns
os_data_X, os_data_y = os.fit_resample(X_train, y_train)
os_data_X = pd.DataFrame(os_data_X, columns=columns)
os_data_y = pd.DataFrame(os_data_y, columns=["y"])
print("length of oversampled data is ", len(os_data_X))
print("Number of no subscription in oversampled data", len(os_data_y[os_data_y["y"] == 0]))
print("Number of subscription", len(os_data_y[os_data_y["y"] == 1]))
print("Proportion of no subscription data in oversampled data is ", len(os_data_y[os_data_y["y"] == 0]) / len(os_data_X))
print("Proportion of subscription data in oversampled data is ", len(os_data_y[os_data_y["y"] == 1]) / len(os_data_X))
