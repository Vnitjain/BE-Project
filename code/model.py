from keras.models import Sequential
from keras.layers import Dense,Conv2D,MaxPooling2D,Flatten,Dropout,Lambda
from keras.callbacks import  TensorBoard

from utils import IMAGE_DIM, batch_processing

import pandas as pd

def load_dataset():

    dataframe = pd.read_csv('data/driving_log.csv',names=['center','left','right','steering', 'throttle', 'reverse', 'speed'])
    images = dataframe[['left','center','right']].values
    steering_angles = dataframe['steering'].values

    from sklearn.model_selection import train_test_split

    x_train, x_test, y_train, y_test = train_test_split(images,steering_angles,random_state=1,test_size=0.3)

    return  x_train, y_train, x_test, y_test

def create_model():

    model = Sequential()

    model.add(Lambda(lambda x : x/127.5 -1, input_shape=IMAGE_DIM))
    model.add(Conv2D(32,5))
    model.add(MaxPooling2D(2, 2))
    model.add(Conv2D(64,5,activation='relu'))
    model.add(MaxPooling2D(2, 2))
    model.add(Conv2D(128,3,activation='relu'))
    model.add(MaxPooling2D(2,2))
    model.add(Flatten())
    model.add(Dense(50,activation='relu'))
    model.add(Dense(25,activation='relu'))
    model.add(Dense(1))

    model.summary()

    return model

def train_model(model,x_train,y_train,x_test,y_test):

    CallBack = TensorBoard(log_dir='./Graph', histogram_freq=0, write_graph=True, write_images=True)
    model.compile(optimizer='adam',loss='mean_squared_error',metrics=['accuracy',])
    model.fit_generator(batch_processing(x_train,y_train,32),
                        steps_per_epoch=25,
                        validation_data=batch_processing(x_test,y_test,16),
                        validation_steps=20,
                        epochs=100,
                        verbose=1,
                        callbacks=[CallBack])

if __name__=="__main__":
    model = create_model()

    dataset = load_dataset()

    train_model(model,*dataset)