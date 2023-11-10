import matplotlib.pyplot as plt
from pandas.plotting import scatter_matrix

def plot_bar(df):
    df.plot.bar(x='roastName', y=["preheatTemperature","beanDropTemperature"])
    plt.show()

def plot_box(df):
    df['ibtsTurningPointTemp'].plot(kind='box', subplots=True, layout=(2,2), sharex=False, sharey=False)
    plt.show()

def plot_scatter(df):
    df.plot.scatter(x='yellowPointTime', y='drumChargeTemperature')
    df.plot.scatter(x='beanChargeTemperature', y='preheatTemperature')
    plt.show()

def plot_scatter_matrix(df):
    features = ['drumChargeTemperature', 'ibtsTurningPointTemp', 'turningPointTime', 'yellowPointTime',
                'indexFirstCrackStart', 'beanDropTemperature', 'totalRoastTime', 'weightLostPercent',
                'Drop-ChargeDeltaTemp', 'ambient', 'temp/time']
    sm = scatter_matrix(df[features], range_padding=0.5, alpha=0.9, figsize=(15, 15))
    [s.xaxis.label.set_rotation(45) for s in sm.reshape(-1)]
    [s.yaxis.label.set_rotation(0) for s in sm.reshape(-1)]
    [s.get_yaxis().set_label_coords(-1, 0.5) for s in sm.reshape(-1)]
    plt.show()