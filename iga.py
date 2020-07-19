import torch
import my_nn
import train
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt


debug = True

input_df = pd.read_csv('dados/input.csv')

cols = ['Sexo', 'COVID19 IgA BOOL', 'COVID19 IgA NUM', 'Monócitos NUM', 'Neutrófilos NUM', 'Eosinófilos NUM', 'Basófilos NUM']
iga_df = input_df[cols]
iga_df = iga_df.dropna(how='any')
iga_df = iga_df.reset_index(drop=True)
iga_df['Sexo'].replace({'F': 1, 'M': 0}, inplace=True)

if debug:
    sns.set(style="darkgrid")
    sns.countplot(x = 'COVID19 IgA BOOL', data=iga_df)
    plt.show()

X  = ['Sexo', 'COVID19 IgA NUM', 'Monócitos NUM', 'Neutrófilos NUM', 'Eosinófilos NUM', 'Basófilos NUM']

Y = ['COVID19 IgA BOOL']

input_size = len(X)

igg_net = my_nn.Net_2hl(input_size, 128, 128)
treinamento = train.Train(igg_net, lr=0.01, X=X, Y=Y, epochs=1000, df=iga_df)
treinamento.train()
