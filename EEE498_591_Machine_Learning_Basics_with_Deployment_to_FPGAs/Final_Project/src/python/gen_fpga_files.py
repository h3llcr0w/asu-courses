#!/usr/bin/env python
# coding: utf-8


max_depth = 22 # Use the same value on FPGA

import pandas as pd
from sklearn.tree import DecisionTreeClassifier
from sklearn.preprocessing import StandardScaler
from sklearn.model_selection import train_test_split

water_dataset= pd.read_csv("datasets/water_potability_balanced.csv")

X = water_dataset.drop("Potability", axis=1)
y = water_dataset["Potability"]

scaler = StandardScaler()
X = scaler.fit_transform(X)

X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=3)

## Run DecisionTreeClassifier to generate model

dtc = DecisionTreeClassifier(random_state=22, max_depth=max_depth-1)
dtc.fit(X_train, y_train)
tree = dtc.tree_

## Convert model details to string representations

padding = [-1]*(2**max_depth-tree.node_count)

thresholds = ' '.join([str(xx) for xx in list(tree.threshold)+padding])
indices = ' '.join([str(xx) for xx in list(tree.feature)+padding])
children_left = ' '.join([str(xx) for xx in list(tree.children_left)+padding])
children_right = ' '.join([str(xx) for xx in list(tree.children_right)+padding])
_pred = [list(val[0]).index(val[0].max()) for val in tree.value]
predictions = ' '.join([str(xx) for xx in _pred+padding])

sensor_train = ' '.join([str(yy) for xx in X_train for yy in xx])
sensor_test = ' '.join([str(yy) for xx in X_test for yy in xx])

potable_train = ' '.join(str(xx) for xx in y_train)
potable_test = ' '.join(str(xx) for xx in y_test)


print("Train dataset size: ", len(X_train))
print("Test dataset size: ", len(X_test))


## Generate output files

with open('fpga_data/model_thresholds.txt', 'w') as out_file:
    out_file.write(thresholds)

with open('fpga_data/children_left.txt', 'w') as out_file:
    out_file.write(children_left)

with open('fpga_data/children_right.txt', 'w') as out_file:
    out_file.write(children_right)

with open('fpga_data/model_sensor_index.txt', 'w') as out_file:
    out_file.write(indices)

with open('fpga_data/model_predictions.txt', 'w') as out_file:
    out_file.write(predictions)


with open("fpga_data/sensor_values_train.txt", 'w') as out_file:
    out_file.write(sensor_train)
with open("fpga_data/potable_ref_train.txt", 'w') as out_file:
    out_file.write(potable_train)


with open('fpga_data/sensor_values_test.txt', 'w') as out_file:
    out_file.write(sensor_test)
with open('fpga_data/potable_ref_test.txt', 'w') as out_file:
    out_file.write(potable_test)
