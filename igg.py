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

X  = igg_df[['Sexo', 'COVID19 IgG NUM']]
X = torch.from_numpy(X.values).float()

Y = igg_df[['COVID19 IgG BOOL']]
Y = torch.from_numpy(Y.values)

input_size = X.shape[1]

igg_net = my_nn.Net_2hl(input_size, 128, 128)
output = igg_net(X)
print(output)


