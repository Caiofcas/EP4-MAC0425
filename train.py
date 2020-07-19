import numpy as np
from sklearn.metrics import confusion_matrix, classification_report
from sklearn.model_selection import KFold
import torch

class Train():
    def __init__(self, net, lr, X, Y, epochs, df):

        self.net = net
        self.X = X
        self.Y = Y
        self.df = df
        self.epochs = epochs
        self.lr = lr


    def _normalize_tensor(self, target):
        max_val = torch.max(target).item()
        min_val = torch.min(target).item()
        normalized = (target - min_val)/(max_val - min_val)

        return target



    def calculate_accuracy(self, y_true, y_pred):
        predicted = y_pred.ge(.5).view(-1)
        y_size = torch.numel(predicted)
        ones = torch.ones(y_size)
        zeros = torch.zeros(y_size)
        out = torch.where(predicted == True, ones, zeros)
        return out.sum().float().item() / torch.numel(y_true)

    def train(self):

        x = self.df[self.X]
        y = self.df[self.Y]


        criterion = torch.nn.BCELoss()
        optimizer = torch.optim.SGD(self.net.parameters(), lr=self.lr)
        device = torch.device("cuda:0" if torch.cuda.is_available() else "cpu")

        self.net = self.net.to(device)
        kf = KFold(n_splits=10, random_state=42, shuffle=True)
        for train_index, test_index in kf.split(self.df):
            # os valores train são usados para de fato treinar a rede neural.
            # Os valores de test são usados depois para alimentar a rede neural e ver 
            # se ela está prevendo bem os valores.
            x_train, x_test, y_train, y_test = x.iloc[train_index], x.iloc[test_index], \
                y.iloc[train_index], y.iloc[test_index]
            x_train = self._normalize_tensor(torch.from_numpy(x_train.to_numpy()).float())
            y_train = torch.from_numpy(y_train.to_numpy()).float()
            x_test = self._normalize_tensor(torch.from_numpy(x_test.to_numpy()).float())
            y_test = torch.from_numpy(y_test.to_numpy()).float()
            
            x_train = x_train.to(device)
            x_test = x_test.to(device)
            y_test = y_test.to(device)

            for epoch in range(self.epochs):
                y_pred = self.net(x_train)
                train_loss = criterion(y_pred, y_train)
                if epoch % 10 == 0:
                    print('EPOCH {0}:'.format(epoch))
                    train_acc = self.calculate_accuracy(y_train, y_pred)
                    y_test_pred = self.net(x_test)
                    test_loss = criterion(y_test_pred, y_test)
                    test_acc = self.calculate_accuracy(y_test, y_test_pred)
                    print('Train Set --- loss:{0}; acc:{1}'.format(train_loss, train_acc))
                    print('Validation Set  --- loss:{0}; acc:{1}'.format(test_loss, test_acc))
                #print('y_pred.shape:', y_pred.shape)
                optimizer.zero_grad()
                train_loss.backward()
                optimizer.step()

    