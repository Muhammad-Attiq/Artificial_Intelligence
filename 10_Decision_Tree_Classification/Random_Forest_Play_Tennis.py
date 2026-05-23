import numpy as np
import pandas as pd
from sklearn import preprocessing
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import (
    accuracy_score,
    classification_report,
    confusion_matrix,
    ConfusionMatrixDisplay
)
import matplotlib.pyplot as plt

!wget -q "https://raw.githubusercontent.com/luelhagos/Play-Tennis-Implementation-Using-Sklearn-Decision-Tree-Algorithm/master/Play%20Tennis.csv" -O "Play Tennis.csv"

PLAY_TENNIS_DATASET = pd.read_csv("Play Tennis.csv")

pd.set_option('display.max_columns', None)
pd.set_option('display.width', 1000)

print("="*60)
print("PLAY TENNIS DATASET")
print("="*60)
display(PLAY_TENNIS_DATASET)

LABEL_ENCODER = preprocessing.LabelEncoder()

for COLUMN_NAME in PLAY_TENNIS_DATASET.columns:
    PLAY_TENNIS_DATASET[COLUMN_NAME] = LABEL_ENCODER.fit_transform(
        PLAY_TENNIS_DATASET[COLUMN_NAME]
    )

print("\n" + "="*60)
print("ENCODED DATASET")
print("="*60)
display(PLAY_TENNIS_DATASET)

FEATURE_COLUMNS = ['Outlook', 'Temprature', 'Humidity', 'Wind']

INPUT_FEATURES = PLAY_TENNIS_DATASET[FEATURE_COLUMNS]
TARGET_OUTPUT = PLAY_TENNIS_DATASET['Play_Tennis']

X_TRAIN, X_TEST, Y_TRAIN, Y_TEST = train_test_split(
    INPUT_FEATURES,
    TARGET_OUTPUT,
    test_size=0.30,
    random_state=42
)

RANDOM_FOREST_MODEL = RandomForestClassifier(
    n_estimators=100,
    random_state=42
)

RANDOM_FOREST_MODEL.fit(X_TRAIN, Y_TRAIN)

PREDICTED_OUTPUT = RANDOM_FOREST_MODEL.predict(X_TEST)

MODEL_ACCURACY = accuracy_score(Y_TEST, PREDICTED_OUTPUT)

print("\n" + "="*60)
print("MODEL ACCURACY")
print("="*60)
print(f"Accuracy = {MODEL_ACCURACY:.2f}")

RESULT_TABLE = pd.DataFrame({
    'Actual': Y_TEST.values,
    'Predicted': PREDICTED_OUTPUT
})

print("\n" + "="*60)
print("ACTUAL VS PREDICTED")
print("="*60)
display(RESULT_TABLE)

CONFUSION_MATRIX_RESULT = confusion_matrix(
    Y_TEST,
    PREDICTED_OUTPUT
)

print("\n" + "="*60)
print("CONFUSION MATRIX")
print("="*60)
print(CONFUSION_MATRIX_RESULT)

CONFUSION_MATRIX_DISPLAY = ConfusionMatrixDisplay(
    confusion_matrix=CONFUSION_MATRIX_RESULT,
    display_labels=['No', 'Yes']
)

CONFUSION_MATRIX_DISPLAY.plot(cmap='Blues')

plt.title("Confusion Matrix")
plt.show()

print("\n" + "="*60)
print("CLASSIFICATION REPORT")
print("="*60)
print(classification_report(Y_TEST, PREDICTED_OUTPUT))

FEATURE_IMPORTANCE_TABLE = pd.DataFrame({
    'Feature': FEATURE_COLUMNS,
    'Importance': RANDOM_FOREST_MODEL.feature_importances_
})

FEATURE_IMPORTANCE_TABLE = FEATURE_IMPORTANCE_TABLE.sort_values(
    by='Importance',
    ascending=False
)

print("\n" + "="*60)
print("FEATURE IMPORTANCE")
print("="*60)
display(FEATURE_IMPORTANCE_TABLE)

plt.figure(figsize=(8,5))

plt.bar(
    FEATURE_IMPORTANCE_TABLE['Feature'],
    FEATURE_IMPORTANCE_TABLE['Importance']
)

plt.xlabel("Features")
plt.ylabel("Importance")
plt.title("Feature Importance in Random Forest")

plt.show()
