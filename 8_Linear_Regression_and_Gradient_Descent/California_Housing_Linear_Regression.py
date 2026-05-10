import pandas as pd
import matplotlib.pyplot as plt
from sklearn.datasets import fetch_california_housing
from sklearn.linear_model import LinearRegression
from sklearn.model_selection import train_test_split
from sklearn.metrics import mean_squared_error
housing = fetch_california_housing(as_frame=True)
df = housing.frame
X = df[['AveRooms']]
y = df['MedHouseVal']
X_train, X_test, y_train, y_test = train_test_split(
    X, y, test_size=0.2, random_state=42)
model = LinearRegression()
model.fit(X_train, y_train)
y_pred = model.predict(X_test)
print("Coefficient:", model.coef_[0])
print("Mean Squared Error:", mean_squared_error(y_test, y_pred))
plt.scatter(X_test, y_test)
plt.plot(X_test, y_pred)
plt.xlabel("Average Rooms")
plt.ylabel("House Price")
plt.title("Feature Impact Analysis")
plt.show()
