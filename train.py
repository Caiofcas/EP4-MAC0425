import numpy as np
from sklearn.metrics import confusion_matrix, classification_report
import torch

class Train():
    def __init__(self, net, lr, x_train, x_test, y_test, epochs):

        self.net = net
        self.x_train = x_train
        self.x_test = x_test
        self.y_test = y_test
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
        self.x_train = self.x_train.to(device)
        self.x_test = self.x_test.to(device)
        self.y_test = self.y_test.to(device)
        for epoch in range(self.epochs):
            y_pred = self.net(self.x_train)
            y_pred = torch.squeeze(y_pred)
            # Precisa disso?
            train_loss = self.criterion(y_pred, self.y_test)
            if epoch % 100 == 0:
                train_acc = self.calculate_accuracy(self.y_test, y_pred)
                y_test_pred = self.net(self.x_test)
                y_test_pred = torch.squeeze(y_test_pred)
                test_loss = self.criterion(y_test_pred, self.y_test)
                test_acc = self.calculate_accuracy(self.y_test, y_test_pred)
                print('EPOCH {0}:'.format(epoch))
                print('Train Set --- loss:{0}; acc:{1}'.format(train_loss, train_acc))
                print('Validation Set  --- loss:{0}; acc:{1}'.format(test_loss, test_acc))
            
            self.optimizer.zero_grad()
            train_loss.backward()
            self.optimizer.step()
