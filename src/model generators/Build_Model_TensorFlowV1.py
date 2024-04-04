# %% -----------------------------------------------------------------------------------------------------------------------------------------
# Imports
'''
The purpose of this file is to build and save a version of the DL ML model that can be imported from joblib in the actual main file
'''
import tensorflow as tf
from tensorflow import keras
from tensorflow.keras import layers
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

n= 69
# Define the input shape
input_shape = (n,)

# Define the model architecture
model = keras.Sequential([
    layers.Dense(((n**2)/2), activation='relu', input_shape=input_shape),
    layers.Dense(2*n, activation='relu'),
    layers.Dense(1, activation='linear')
])

# Compile the model
model.compile(optimizer='adam', loss='mse', metrics=['mae'])

# Print the model summary
model.summary()

training_history = model.fit(X_train, y_train, epochs=10, batch_size=32, validation_split=0.1)
# %%
loss, mae = model.evaluate(X_test, y_test)

model.save('my_model3.h5')


# %%
#How to make predicitons from the model:


# Load the model from the file
from keras.models import load_model
loaded_model = load_model('my_model3.h5')

# Use the loaded model to make predictions
y_pred = loaded_model.predict(X_test)


# %%
