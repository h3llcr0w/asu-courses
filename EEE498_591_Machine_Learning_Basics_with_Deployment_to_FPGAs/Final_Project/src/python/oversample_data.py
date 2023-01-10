#!/usr/bin/env python
# coding: utf-8

# In[1]:


import pandas as pd
from collections import Counter
from sklearn.preprocessing import StandardScaler
from imblearn.over_sampling import RandomOverSampler

water_dataset= pd.read_csv("datasets/water_potability_cleaned.csv")

X = water_dataset.drop("Potability", axis=1)
y = water_dataset["Potability"]

scaler = StandardScaler()
X = scaler.fit_transform(X)


over_sampler = RandomOverSampler(random_state=33)
X_res, y_res = over_sampler.fit_resample(X,y)
water_dataset_balanced = pd.DataFrame(X_res, columns = water_dataset.columns[:-1])
water_dataset_balanced['Potability'] = y_res
water_dataset_balanced.to_csv("datasets/water_potability_balanced.csv", index=False)
