import numpy as np
import pandas as pd
from sklearn import preprocessing
from sklearn.model_selection import train_test_split
from sklearn.tree import DecisionTreeClassifier, export_graphviz
from sklearn.metrics import accuracy_score, classification_report, confusion_matrix
from sklearn import tree
from six import StringIO
from IPython.display import Image, display
import pydotplus
import matplotlib.pyplot as plt

!pip install pydotplus -q
!apt-get install graphviz -y -q

!wget -q "https://raw.githubusercontent.com/luelhagos/Play-Tennis-Implementation-Using-Sklearn-Decision-Tree-Algorithm/master/Play%20Tennis.csv" -O "Play Tennis.csv"

PLAY_TENNIS_DATASET = pd.read_csv("Play Tennis.csv")

pd.set_option('display.max_columns', None)
pd.set_option('display.width', 1000)

print("="*60)
print("ORIGINAL COLUMN NAMES")
print("="*60)
print(PLAY_TENNIS_DATASET.columns.tolist())

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

DECISION_TREE_MODEL = DecisionTreeClassifier(
    criterion="entropy",
    random_state=100
)

DECISION_TREE_MODEL.fit(X_TRAIN, Y_TRAIN)

PREDICTED_OUTPUT = DECISION_TREE_MODEL.predict(X_TEST)

print("\n" + "="*60)
print("MODEL ACCURACY")
print("="*60)
print(f"Accuracy : {accuracy_score(Y_TEST, PREDICTED_OUTPUT):.2f}")

RESULT_TABLE = pd.DataFrame({
    'Actual': Y_TEST.values,
    'Predicted': PREDICTED_OUTPUT
})

print("\n" + "="*60)
print("ACTUAL VS PREDICTED")
print("="*60)
display(RESULT_TABLE)

print("\n" + "="*60)
print("CONFUSION MATRIX")
print("="*60)
print(confusion_matrix(Y_TEST, PREDICTED_OUTPUT))

print("\n" + "="*60)
print("CLASSIFICATION REPORT")
print("="*60)
print(classification_report(Y_TEST, PREDICTED_OUTPUT))

plt.figure(figsize=(20,10))

tree.plot_tree(
    DECISION_TREE_MODEL,
    feature_names=FEATURE_COLUMNS,
    class_names=['No', 'Yes'],
    filled=True,
    rounded=True,
    fontsize=10
)

plt.title("Decision Tree - Play Tennis Dataset", fontsize=16)
plt.show()

DOT_DATA = StringIO()

export_graphviz(
    DECISION_TREE_MODEL,
    out_file=DOT_DATA,
    filled=True,
    rounded=True,
    special_characters=True,
    feature_names=FEATURE_COLUMNS,
    class_names=['No', 'Yes']
)

GRAPH_OBJECT = pydotplus.graph_from_dot_data(DOT_DATA.getvalue())

GRAPH_OBJECT.write_png("PLAY_TENNIS_TREE.png")

display(Image(GRAPH_OBJECT.create_png()))
