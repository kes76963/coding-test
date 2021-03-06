import seaborn as sns
import pandas as pd
import numpy as np

pd.set_option('display.max_columns', 15)
pd.set_option('display.max_row', 500)

raw_data = sns.load_dataset('titanic')
print(raw_data.head(50))

print(raw_data.info())

raw_data.isnull().sum()

clean_data = raw_data.dropna(axis=1, thresh=500)
print(clean_data.columns)

mean_age = clean_data['age'].mean()
print(mean_age)

print(clean_data.head(10))

df = clean_data['age'].fillna(mean_age, inplace=True)

print(clean_data.head(10))

clean_data.drop(['embark_town', 'alive'], axis=1, inplace=True)

print(clean_data.info())

print(clean_data['embarked'][825:835])

clean_data['embarked'].fillna(
    method='ffill', inplace=True)
print(clean_data['embarked'][825:830])

print(clean_data.isnull().sum())

print(clean_data.info())

clean_data['sex'].replace({'male':0, 'female':1}, inplace=True)
print(clean_data.info())

print(clean_data['sex'].unique())

print(clean_data['embarked'].unique())

from sklearn import preprocessing

label_encoder = preprocessing.LabelEncoder()
onehot_encoder = preprocessing.OneHotEncoder()

print(clean_data['embarked'].value_counts())

clean_data['embarked'] = label_encoder.fit_transform(
    clean_data['embarked'])
print(clean_data['embarked'].unique())

print(clean_data['embarked'].value_counts())

print(clean_data.info())

clean_data['class'] = label_encoder.fit_transform(
    clean_data['class'])
print(clean_data['class'].unique())

print(clean_data.info())

clean_data['who'] = label_encoder.fit_transform(
    clean_data['who'])
print(clean_data['who'].unique())

print(clean_data.info())

clean_data['adult_male'] = clean_data['adult_male'].astype(
    'int64')
print(clean_data.info())

print(clean_data['adult_male'])

clean_data['alone'] = clean_data['alone'].astype(
    'int64')
print(clean_data.info())

target = pd.DataFrame(clean_data.iloc[:, 0], columns=['survived'])
training_data = clean_data.drop('survived', axis=1)
print(training_data.head())
print(target.head())

value_data = training_data[['age', 'fare']]
print(value_data.head())

from sklearn.preprocessing import StandardScaler
scaler = StandardScaler()
scaled_data = scaler.fit_transform(value_data)
value_data = pd.DataFrame(scaled_data, columns= value_data.columns)
print(value_data.head())

print(value_data.describe())

training_data.drop(['age', 'fare'], axis=1, inplace=True)
print(training_data.head())

onehot_data = pd.get_dummies(training_data['pclass'])
print(onehot_data.head())

print(training_data.head())

onehot_data = pd.get_dummies(training_data, columns=training_data.columns)
print(onehot_data.head())

print(onehot_data.info())

training_data = pd.concat([value_data, onehot_data], axis=1)
print(training_data.info())

from sklearn.model_selection import train_test_split
X_train, X_test, Y_train, Y_test = train_test_split(
    training_data, target, test_size=0.20)

print(X_train.shape)
print(Y_train.shape)
print(X_test.shape)
print(Y_test.shape)

from tensorflow.keras.models import Sequential
from tensorflow.keras.layers import Dense, Dropout

model = Sequential()
model.add(Dense(128, input_dim=34, activation='relu'))
model.add(Dropout(0.02))
model.add(Dense(256, activation='relu'))
model.add(Dropout(0.2))
model.add(Dense(512, activation='relu'))
model.add(Dropout(0.2))
model.add(Dense(256, activation='relu'))
model.add(Dropout(0.2))
model.add(Dense(128, activation='relu'))
model.add(Dropout(0.02))
model.add(Dense(64, activation='relu'))
model.add(Dropout(0.02))
model.add(Dense(32, activation='relu'))
model.add(Dropout(0.02))
model.add(Dense(1, activation='sigmoid'))
print(model.summary())

model.compile(loss='mse', optimizer='adam',
              metrics=['binary_accuracy'])
fit_hist = model.fit(
    X_train, Y_train, batch_size=50, epochs=30,
    validation_split=0.2, verbose=1)

import matplotlib.pyplot as plt
plt.plot(fit_hist.history['binary_accuracy'])
plt.plot(fit_hist.history['val_binary_accuracy'])
plt.show()

score = model.evaluate(X_test, Y_test, verbose=0)
print('loss', score[0])
print('accuracy ', score[1])

