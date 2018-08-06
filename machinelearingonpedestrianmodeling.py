# -*- coding: utf-8 -*-
"""MachineLearingOnPedestrianModeling.ipynb

Automatically generated by Colaboratory.

Original file is located at
    https://colab.research.google.com/drive/1zL2dF795yuefSQVPvmWG1uti5K74uI-f

Import packages
"""

import pandas as pd
from google.colab import files
from sklearn import svm, linear_model, preprocessing
from sklearn.utils import shuffle
from sklearn.model_selection import cross_val_score
import io
import matplotlib.pyplot as plt
import numpy as np

"""Load and organize  the data"""

DataFile = files.upload()
Data_df = pd.read_csv(io.StringIO(DataFile['Data.csv'].decode('utf-8')))
Data_df = shuffle(Data_df)
Data_df = pd.read_csv(io.StringIO(DataFile['Data.csv'].decode('utf-8')))
Data_df = shuffle(Data_df)
X = preprocessing.scale(Data_df.loc[:,'R1D':'Money'])
Y = Data_df.loc[:,'Label']
X_train = X[0:1400]
X_test = X[1400: 1599]
Y_train = Y[0:1400]
Y_test = Y[1400: 1599]

"""# 1. Multi-class logistic regression:

*Use one-vs-rest strategy for multi-class classification.*

1.1 Use 5-fold cross validation to choose panelty parameter C
"""

LogRegAccuracies = []
different_Cs = np.arange(0.1,5,0.1)
for c in different_Cs:
  LogReg = linear_model.LogisticRegression(C=c, max_iter = 200)
  scores = cross_val_score(LogReg, X_train, Y_train, cv=5)
  accuracy = scores.mean()
  LogRegAccuracies.append(accuracy)

Best_C = different_Cs[np.argmax(LogRegAccuracies)]
print("Best C: " + str(Best_C) + ', ' + 'best accuracy: ' + str(max(LogRegAccuracies)))
plt.plot(different_Cs, LogRegAccuracies, 'r-')
plt.xlabel("C")
plt.ylabel("Accuracy")
plt.show()

"""1.2 Train on the whole training data set using best C, and then use the test set to evaluate"""

LogReg = linear_model.LogisticRegression(C=Best_C, max_iter=200)
LogReg.fit(X_train, Y_train)
LogReg_Accuracy = LogReg.score(X_test, Y_test)
print(LogReg_Accuracy)

"""# 2. Multi-class Support Vector Machine:

*Use one-vs-rest strategy for multi-class classification. Use radial basis function kernel (Gaussian kernel).*

2.1 Use 5-fold cross validation to choose panelty parameter C
"""

SVMAccuracies = []
different_Cs = np.arange(0.1,5,0.1)
for c in different_Cs:
  SVM = svm.SVC(C=c)
  scores = cross_val_score(SVM, X[0:1000], Y[0:1000], cv=5)
  accuracy = scores.mean()
  SVMAccuracies.append(accuracy)

Best_C = different_Cs[np.argmax(SVMAccuracies)]
print("Best C: " + str(Best_C) + ', ' + 'best accuracy: ' + str(max(SVMAccuracies)))
plt.plot(different_Cs, SVMAccuracies, 'r-')
plt.xlabel("C")
plt.ylabel("Accuracy")
plt.show()

"""2.2 Train on the whole training data set using best C, and then use the test set to evaluate"""

SVM = svm.SVC(C=Best_C)
SVM.fit(X_train, Y_train)
SVM_Accuracy = SVM.score(X_test, Y_test)
print(SVM_Accuracy)

"""# 3. Neural Network"""

import tensorflow as tf
from tensorflow import keras

NeuralNetwork = keras.Sequential([
    keras.layers.Dense(12, activation=tf.nn.relu),
    keras.layers.Dense(10, activation=tf.nn.relu),
    keras.layers.Dense(10, activation=tf.nn.softmax)
])

NeuralNetwork.compile(optimizer=tf.train.AdamOptimizer(), 
              loss='sparse_categorical_crossentropy',
              metrics=['accuracy'])

Y_train_modified = Y_train - 1
Y_test_modified = Y_test - 1
history = NeuralNetwork.fit(X_train, Y_train_modified.values, epochs=200, validation_data=(X_test, Y_test_modified), verbose=0)

plt.plot(history.history['acc'])
plt.plot(history.history['val_acc'])
plt.show()

test_loss, test_acc = NeuralNetwork.evaluate(X_test, Y_test_modified)
print('Test accuracy:', test_acc)