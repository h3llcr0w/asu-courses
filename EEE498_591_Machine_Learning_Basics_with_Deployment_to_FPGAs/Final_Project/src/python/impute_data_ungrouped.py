#!/usr/bin/env python
# coding: utf-8

## Python code to remove NA values form the dataset by imputing with mean values, grouped by potability


import pandas as pd

water_dataset= pd.read_csv("datasets/water_potability_orig.csv")

water_dataset["ph"].fillna(value = water_dataset["ph"].mean(), inplace = True)
water_dataset["Sulfate"].fillna(value = water_dataset["Sulfate"].mean(), inplace = True)
water_dataset["Trihalomethanes"].fillna(value = water_dataset["Trihalomethanes"].mean(), inplace = True)

water_dataset.to_csv('datasets/water_potability_cleaned_ungrouped.csv', index=False)
