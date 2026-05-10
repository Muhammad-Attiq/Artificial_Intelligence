import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
from sklearn import linear_model
from sklearn.model_selection import train_test_split
data_url = "http://lib.stat.cmu.edu/datasets/boston"
raw_df = pd.read_csv(data_url, sep=r"\s+", skiprows=22, header=None)
X = raw_df.values[::2, :]
y = raw_df.values[1::2, 0]
X_train, X_test, y_train, y_test = train_test_split
 (X, y, test_size=0.4, random_state=1)
reg = linear_model.LinearRegression()
reg.fit(X_train, y_train)
print('Coefficients: ', reg.coef_)
print('Variance score: {}'.format(reg.score(X_test, y_test)))
plt.style.use('ggplot')
plt.scatter(reg.predict(X_train), reg.predict(X_train) - y_train,
    color="green", s=10, label='Train data')
plt.scatter(reg.predict(X_test), reg.predict(X_test) - y_test,
    color="blue", s=10, label='Test data')
plt.hlines(y=0, xmin=0, xmax=50, linewidth=2)
plt.legend(loc='upper right')
plt.title("Residual errors")
plt.show()
