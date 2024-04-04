# %% -----------------------------------------------------------------------------------------------------------------------------------------
# Imports
'''
The purpose of this file is to build and save a version of the DL ML model that can be imported from joblib in the actual main file
'''
import pandas as pd
import numpy as np
from sklearn.model_selection import train_test_split 
from sklearn.neural_network import MLPRegressor
from joblib import dump,load

# %%
X = pd.read_csv('xdata.txt', delimiter=' ',header=None)
y = pd.read_csv('ydata.txt',delimiter=' ',header=None)

# %%
X = X.dropna(axis=1)
# %%
rng = np.random.RandomState(123)
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.05, random_state= rng)

n = 100
model = MLPRegressor(hidden_layer_sizes=[n])

model.fit(X_train,y_train)

model.predict(X_test)

# %% -----------------------------------------------------------------------------------------------------------------------------------------
model.score(X_test,y_test)
# %%
dump(model, 'chessengine2.joblib')
# Load with model = load('chessengine.joblib') 

# %% -----------------------------------------------------------------------------------------------------------------------------------------
'''
HOW TO PREDICT WITH THE MODEL
-------------------------------

model = load('chessengine.joblib') 

pred = '-0.4 -0.5 -0.6 -0.8 -1.0 -0.6 -0.5 -0.4 -0.2 -0.2 -0.2 -0.2 -0.2 -0.2 -0.2 -0.2 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0.2 0 0 0 0 0 0 0 0 0 0 0 0 0.2 0.2 0.2 0 0.2 0.2 0.2 0.2 0.4 0.5 0.6 0.8 1.0 0.6 0.5 0.4 -1 1 1 1 1'
pred = pred.split()

df = pd.DataFrame(pred).T

model.predict(df)
'''

