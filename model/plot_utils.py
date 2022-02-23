import matplotlib.pyplot as plt
import numpy as np
import pandas as pd


def monte_carlo_plot(dfs, column):
  fig, ax = plt.subplots()
  i = 0
  for df in dfs:
    x = pd.Series(dfs[i]["timestep"]).values
    ax.plot(x, pd.Series(df[column]).values, label='Run '+ str(df['run'][0]) + "Parameter " + str(df['subset'][0])) 
    i += 1
  plt.xlabel('Timestep')
  plt.ylabel(column)
  ax.legend()
  plt.title(' ' + column)
  plt.show()