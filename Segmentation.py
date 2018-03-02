import os
import pandas as pd
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D
%matplotlib inline


DATA_PATH = './data'
Filename = 'angleScan_layer2.csv'

csv_path = os.path.join(DATA_PATH, Filename)
dataset = pd.read_csv(csv_path)

dataset.head()
dataset.info()
dataset.describe()
dataset.hist(bins=50, figsize=(20, 15))

dataset['cellId'].value_counts()
dataset.sort_values(by='cellId', ascending=True)

fig = plt.figure()
ax = Axes3D(fig)

group = dataset.groupby('cellId')
for cellid in group.groups.keys():
    df = group.get_group(cellid)
    ax.scatter(df['x'], df['z'], df['y'])  # Detector axis placed correctly

ax.set_xlabel('x')
ax.set_ylabel('z')
ax.set_zlabel('y')


fig.savefig('./plots/allHits_2.pdf')
