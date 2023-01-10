#!/usr/bin/env python
# coding: utf-8


import pandas as pd
import numpy as np
import seaborn as sns
import matplotlib.pyplot as plt
import plotly.express as px

water_dataset= pd.read_csv("datasets/water_potability_balanced.csv")

sns.heatmap(water_dataset.corr(), annot=True, cmap="Blues")
plt.title("Correlations Between Variables", size=16)
plt.show()

d = pd.DataFrame(water_dataset["Potability"].value_counts())
fig = px.pie(d,
             values = "Potability",
             names = ["Not Potable", "Potable"],
             hole = 0.4,
             opacity = 0.8,
             labels = {"label" : "Potability", "Potability" : "Number of Samples"})
fig.update_layout(title = dict(text = "Pie Chart of Potability"))
fig.update_traces(textposition = "outside", textinfo = "percent+label")
fig.show()


