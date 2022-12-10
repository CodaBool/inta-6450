import os
import json
import pandas as pd
from pathlib import Path
import seaborn as sns
import matplotlib.pyplot as plt

df = pd.read_json('./results/main.json')

# correlation
print("correlation between urls & security", df['score'].corr(df['urls']))
print("correlation between permissions & security", df['score'].corr(df['permissions']))
print("correlation between being a game & security", df['score'].corr(df['game']))

# positive means when one goes up the other does too
# negative means when one goes down the other goes up
#  0 - .2 very weak
# .2 - .4 weak

# scatter graph
plt.rcParams.update({'figure.figsize':(10,8), 'figure.dpi':100})
sns.lmplot(x='game', y='score', data=df)
plt.title("Scatter Plot with Linear fit");
plt.show()