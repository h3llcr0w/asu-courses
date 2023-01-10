#!/usr/bin/env python
# coding: utf-8

## Python code to remove NA values form the dataset by imputing with mean values, grouped by potability


import pandas as pd
import missingno as msno
import matplotlib.pyplot as plt

water_dataset= pd.read_csv("datasets/water_potability_orig.csv")

msno.matrix(water_dataset)
plt.show()

water_dataset['ph'] = water_dataset['ph'].fillna(water_dataset.groupby(['Potability'])['ph'].transform('mean'))
water_dataset['Sulfate'] = water_dataset['Sulfate'].fillna(water_dataset.groupby(['Potability'])['Sulfate'].transform('mean'))
water_dataset['Trihalomethanes'] = water_dataset['Trihalomethanes'].fillna(water_dataset.groupby(['Potability'])['Trihalomethanes'].transform('mean'))

water_dataset.to_csv('datasets/water_potability_cleaned.csv', index=False)
