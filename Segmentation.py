import os
import pandas as pd
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D
#%matplotlib inline

DATA_PATH = './data'
Filename = 'angleScan_layer1.csv'

csv_path = os.path.join(DATA_PATH, Filename)
dataset = pd.read_csv(csv_path)

dataset.head()
dataset.info()
dataset.describe()
dataset.hist(bins=50, figsize=(20, 15))

dataset['cellId'].value_counts()
dataset.sort_values(by='cellId', ascending=True)


group = dataset.groupby('cellId')

for cellid in group.groups.keys():
    df = group.get_group(cellid)
    fig = plt.figure()
    ax = Axes3D(fig)
    ax.scatter(df['x'], df['y'], df['z'])
    fig.savefig('./plots/cellid'+str(cellid)+'.pdf')
