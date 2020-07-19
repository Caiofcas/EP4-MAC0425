import numpy as np
from sklearn.metrics import confusion_matrix, classification_report
from sklearn.model_selection import KFold
import torch

class Train():
    def __init__(self, net, q, X, Y, epochs, df):

        self.net = net
        self.X = X
        self.Y = Y
        self.df = df
        self.epochs = epochs
        self.criterion = torch.nn.BCELoss()
        self.optimizer = torch.optim.Adam(net.parameters(), lr=lr)



    def calculate_accuracy(self, y_true, y_pred):
        predicted = y_pred.ge(.5).view(-1)
        return (y_true == predicted).sum().float() / len(y_true)

    def train(self):
        # Falta alguma implementação de k-fold
        device = torch.device("cuda:0" if torch.cuda.is_available() else "cpu")

        self.net = self.net.to(device)
        kf = KFold(n_splits=10, random_state=42, shuffle=True)
        for train_index, test_index in kf.split(self.df):
            x_train, x_test, y_train, y_test = self.X.iloc[train_index], self.X.iloc[test_index], \
                self.Y.iloc[train_index], self.Y.iloc[test_index]
            x_train = x_train.to(device)
            x_test = x_test.to(device)
            y_test = y_test.to(device)
            y_pred = self.net(x_train)
            for epoch in range(self.epochs):
                y_pred = torch.squeeze(y_pred)
                # Precisa disso?
                train_loss = self.criterion(y_pred, y_test)
                if epoch % 100 == 0:
                    train_acc = self.calculate_accuracy(y_test, y_pred)
                    y_test_pred = self.net(x_test)
                    y_test_pred = torch.squeeze(y_test_pred)
                    test_loss = self.criterion(y_test_pred, y_test)
                    test_acc = self.calculate_accuracy(y_test, y_test_pred)
                    print('EPOCH {0}:'.format(epoch))
                    print('Train Set --- loss:{0}; acc:{1}'.format(train_loss, train_acc))
                    print('Validation Set  --- loss:{0}; acc:{1}'.format(test_loss, test_acc))

                self.optimizer.zero_grad()
                train_loss.backward()
                self.optimizer.step()
