import pandas as pd
import numpy as np
from sklearn.model_selection import train_test_split
from keras.models import Sequential
from keras.optimizers import Adam
from keras.callbacks import ModelCheckpoint
from keras.layers import Lambda, Conv2D, MaxPooling2D, Dropout, Dense, Flatten
from utils import INPUT_SHAPE, batch_generator
import argparse
import os

data_dir = 'data'
test_size = 0.2
keep_prob = 0.5
nb_epoch = 10
samples_per_epoch = 1000
batch_size = 20
save_best_only = 'true'
learning_rate = 1.0e-4

def load_data():
    data = pd.read_csv(os.path.join(os.getcwd(), data_dir, 'driving_log.csv'), names=['center', 'left', 'right', 'steering', 'throttle', 'reverse', 'speed'])
    X = data[['center', 'left', 'right']].values
    y = data['steering'].values
    X_train, X_valid, y_train, y_valid = train_test_split(X, y, test_size=test_size, random_state=1)
    return X_train, X_valid, y_train, y_valid


def build_model():
    model = Sequential()
    model.add(Lambda(lambda x: x/127.5-1.0, input_shape=INPUT_SHAPE))
    model.add(Conv2D(24, kernel_size=(5, 5), activation='elu', strides=(2, 2)))
    model.add(Conv2D(36, kernel_size=(5, 5), activation='elu', strides=(2, 2)))
    model.add(Conv2D(48, kernel_size=(5, 5), activation='elu', strides=(2, 2)))
    model.add(Conv2D(64, kernel_size=(3, 3), activation='elu'))
    model.add(Conv2D(64, kernel_size=(3, 3), activation='elu'))
    model.add(Dropout(keep_prob))
    model.add(Flatten())
    model.add(Dense(100, activation='elu'))
    model.add(Dense(50, activation='elu'))
    model.add(Dense(10, activation='elu'))
    model.add(Dense(1))
    model.summary()

    return model


def train_model(model, X_train, X_valid, y_train, y_valid):
    checkpoint = ModelCheckpoint('model-{epoch:03d}.h5',
                                 monitor='val_loss',
                                 verbose=0,
                                 save_best_only=save_best_only,
                                 mode='auto')
    model.compile(loss='mean_squared_error', optimizer=Adam(lr=learning_rate),metrics=['accuracy',])
    model.fit_generator(batch_generator(data_dir, X_train, y_train, batch_size, True),
                        samples_per_epoch,
                        nb_epoch,
                        max_q_size=1,
                        validation_data=batch_generator(data_dir, X_valid, y_valid, batch_size, False),
                        validation_steps=len(X_valid),
                        callbacks=[checkpoint],
                        verbose=1)


def main():
    data = load_data()
    model = build_model()
    train_model(model, *data)


if __name__ == '__main__':
    main()
