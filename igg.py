import torch
import my_nn
import train
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt


debug = False

input_size = 10
input_df = pd.read_csv('dados/input.csv')

cols = ['Sexo', 'COVID19 IgG BOOL', 'COVID19 IgG NUM']
igg_df = input_df[cols]
igg_df = igg_df.dropna(how='any')
igg_df = igg_df.reset_index(drop=True)
igg_df['Sexo'].replace({'F': 1, 'M': 0}, inplace=True)

if debug:
    sns.set(style="darkgrid")
    sns.countplot(x = 'COVID19 IgG BOOL', data=igg_df) # HAHHAHHAHAHAAHA
    plt.show()

X  = ['Sexo', 'COVID19 IgG NUM', 'Monócitos NUM', 'Neutrófilos NUM', 'Eosinófilos NUM', 'Basófilos NUM']

Y = ['COVID19 IgG BOOL']

input_size = len(X)

igg_net = my_nn.Net_2hl(input_size, 128, 128)
treinamento = train.Train(igg_net, lr=0.01, X=X, Y=Y, epochs=1000, df=igg_df)
treinamento.train()
