#!/usr/bin/env python
# coding: utf-8


import pandas as pd
import numpy as np
import plotly.express as px
import seaborn as sns
import matplotlib.pyplot as plt
from sklearn.model_selection import train_test_split, GridSearchCV
from sklearn.preprocessing import StandardScaler
from sklearn.metrics import accuracy_score, confusion_matrix, roc_curve, roc_auc_score
from sklearn.tree import plot_tree
from sklearn.tree import export_text

from sklearn.linear_model import LogisticRegression
from sklearn.tree import DecisionTreeClassifier
from sklearn.ensemble import RandomForestClassifier
from sklearn.svm import SVC
from xgboost import XGBClassifier
from lightgbm import LGBMClassifier
from sklearn.naive_bayes import GaussianNB
from sklearn.neighbors import KNeighborsClassifier


water_dataset= pd.read_csv("datasets/water_potability_balanced.csv")
water_dataset = water_dataset.dropna()

X = water_dataset.drop("Potability", axis=1)
y = water_dataset["Potability"]

scaler = StandardScaler()
X = scaler.fit_transform(X)


model_data = pd.DataFrame(columns=["Model", "Train Accuracy Score","Test Accuracy Score","Misclassified Train",'Misclassified Test'])


model_list = [("Logistic Regression", LogisticRegression(random_state=5)),
              ("Random Forest", RandomForestClassifier(random_state=5)),
              ("LightGBM", LGBMClassifier(random_state=5)),
              ("Support Vector Machines", SVC(random_state=5)),
              ("XGBoost", XGBClassifier(random_state=5)),
              ("Gaussian Naive Bayes", GaussianNB()),
              ("KNN", KNeighborsClassifier(n_neighbors=2)),
              ("Decision Tree", DecisionTreeClassifier(random_state=5))]


X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=3)


for model, classifier in model_list:
    classifier.fit(X_train, y_train)
    y_pred_train= classifier.predict(X_train)
    y_pred_test= classifier.predict(X_test)
    score_train = accuracy_score(y_train, y_pred_train)
    misclassified_train =(y_train != y_pred_train).sum()
    score_test =accuracy_score(y_test, y_pred_test)
    misclassified_test =(y_test != y_pred_test).sum()
   
    new_row = {"Model": model, "Train Accuracy Score": score_train, "Test Accuracy Score":score_test , "Misclassified Train": misclassified_train,  'Misclassified Test':misclassified_test}
    model_data = pd.concat([model_data, pd.DataFrame(new_row, index=[0])], ignore_index=True)



model_data = model_data.sort_values(by="Test Accuracy Score", ascending=False)
print(model_data)


dtc = model_list[1][1]
y_pred_test = dtc.predict(X_test)
plt.figure(figsize=(8,6))
sns.heatmap(confusion_matrix(y_test, y_pred_test), annot=True, cmap="Blues", fmt="d")
plt.title("Confusion Matrix of Random Forest", size=15)
plt.show()

