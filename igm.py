import torch
import my_nn
import train
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt


debug = True

input_df = pd.read_csv('dados/input.csv')

cols = ['Sexo', 'COVID19 IgM BOOL', 'COVID19 IgM NUM', 'Monócitos NUM', 'Neutrófilos NUM', 'Eosinófilos NUM', 'Basófilos NUM']
igm_df = input_df[cols]
igm_df = igm_df.dropna(how='any')
igm_df = igm_df.reset_index(drop=True)
igm_df['Sexo'].replace({'F': 1, 'M': 0}, inplace=True)

if debug:
    sns.set(style="darkgrid")
    sns.countplot(x = 'COVID19 IgM BOOL', data=igm_df)
    plt.show()

X  = ['Sexo', 'COVID19 IgM NUM', 'Monócitos NUM', 'Neutrófilos NUM', 'Eosinófilos NUM', 'Basófilos NUM']

Y = ['COVID19 IgM BOOL']

input_size = len(X)

igg_net = my_nn.Net_2hl(input_size, 128, 128)
treinamento = train.Train(igg_net, lr=0.01, X=X, Y=Y, epochs=1000, df=igm_df)
treinamento.train()
