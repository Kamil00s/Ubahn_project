import pandas as pd

df = pd.read_csv("dataset.csv", sep=";", decimal=",")

print(df.head())
print(df.shape)
print(df.columns)
