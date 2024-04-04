# %% -----------------------------------------------------------------------------------------------------------------------------------------
# Imports
'''
The purpose of this file is to build and save a version of the DL ML model that can be imported from joblib in the actual main file
'''
import tensorflow as tf
from tensorflow.keras.layers import Dense, Dropout
from tensorflow.keras.callbacks import TensorBoard
from sklearn.model_selection import train_test_split

import pandas as pd
import numpy as np


# %%
X = pd.read_csv('xdata.txt', delimiter=' ',header=None)
y = pd.read_csv('ydata.txt', delimiter=' ',header=None)
# %%
X = X.dropna(axis=1)
# %%
rng = np.random.RandomState(123)
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.05, random_state= rng)

n = 69
# Define the input shape
input_shape = (n,)

# define the model
model = tf.keras.Sequential([
    Dense(n, activation='relu', input_shape=(n,)), 
    Dropout(0.2),

    Dense(8*n, activation='relu'),
    Dropout(0.2),

    Dense(4*n, activation='relu'),
    Dropout(0.2),

    Dense(2*n, activation='relu'),

    Dense(1)
])


# Use the Adam optimizer with a learning rate of 0.001 and mean squared error loss function
optimizer = tf.keras.optimizers.Adam(learning_rate=0.001)
model.compile(loss='mse', optimizer=optimizer,  metrics=['mae'])

# Print the model summary
model.summary()

#tensorboard definition, available via tensorboard --logdir=./logs          localhost:6006
tensorboard_callback = TensorBoard(log_dir='./logs', histogram_freq=1)

history = model.fit(X_train, y_train, epochs=10, batch_size=32, 
                    validation_data=(X_test, y_test), 
                    callbacks=[tensorboard_callback])

# %%
#loss, mae = model.evaluate(X_test, y_test)

model.save('dropout_model.h5')


# %%
#How to make predicitons from the model:


# Load the model from the file
from keras.models import load_model
loaded_model = load_model('dropout_model.h5')

# Use the loaded model to make predictions
y_pred = loaded_model.predict(X_test)


# %%
