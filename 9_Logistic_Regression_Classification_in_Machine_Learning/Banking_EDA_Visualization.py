import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
import seaborn as sns
from sklearn.linear_model import LogisticRegression
from sklearn.model_selection import train_test_split
from sklearn import preprocessing

url = "https://raw.githubusercontent.com/madmashup/targeted-marketing-predictive-engine/master/banking.csv"
data = pd.read_csv(url, header=0)
data = data.dropna()

data["education"] = np.where(data["education"] == "basic.9y", "Basic", data["education"])
data["education"] = np.where(data["education"] == "basic.6y", "Basic", data["education"])
data["education"] = np.where(data["education"] == "basic.4y", "Basic", data["education"])

pd.crosstab(data.day_of_week, data.y).plot(kind="bar")
plt.title("Purchase Frequency for Day of Week")
plt.xlabel("Day of Week")
plt.ylabel("Frequency of Purchase")
plt.show()

pd.crosstab(data.month, data.y).plot(kind="bar")
plt.title("Purchase Frequency for Month")
plt.xlabel("Month")
plt.ylabel("Frequency of Purchase")
plt.show()

pd.crosstab(data.job, data.y).plot(kind="bar")
plt.title("Purchase Frequency for Job Title")
plt.xlabel("Job")
plt.ylabel("Frequency of Purchase")
plt.savefig("purchase_fre_job")
plt.show()

data.age.hist()
plt.title("Histogram of Age")
plt.xlabel("Age")
plt.ylabel("Frequency")
plt.savefig("hist_age")
plt.show()

table = pd.crosstab(data.marital, data.y)
table.div(table.sum(1).astype(float), axis=0).plot(kind="bar", stacked=True)
plt.title("Stacked Bar Chart of Marital Status vs Purchase")
plt.xlabel("Marital Status")
plt.ylabel("Proportion of Customers")
plt.savefig("marital_vs_pur_stack")
plt.show()

pd.crosstab(data.poutcome, data.y).plot(kind="bar")
plt.title("Purchase Frequency for Poutcome")
plt.xlabel("Poutcome")
plt.ylabel("Frequency of Purchase")
plt.show()

table = pd.crosstab(data.education, data.y)
table.div(table.sum(1).astype(float), axis=0).plot(kind="bar", stacked=True)
plt.title("Stacked Bar Chart of Education vs Purchase")
plt.xlabel("Education")
plt.ylabel("Proportion of Customers")
plt.show()
