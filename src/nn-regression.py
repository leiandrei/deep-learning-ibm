from sklearn.datasets import fetch_california_housing
from sklearn.metrics import mean_squared_error
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler
from sklearn.ensemble import RandomForestRegressor

from keras.optimizers import SGD
from keras.layers import Dense, Normalization
from keras.models import Sequential
import numpy as np

if __name__ == "__main__":

    data = fetch_california_housing()
    X, y = data.data, data.target

    X_train, X_test, y_train, y_test = train_test_split(
        X, y, test_size=0.2, random_state=42)

    rf = RandomForestRegressor(n_estimators=200)
    rf.fit(X_train, y_train)

    yhat_rf = rf.predict(X_test)

    print(np.sqrt(mean_squared_error(y_test, yhat_rf)))

    X_train_np = np.array(X_train, dtype=np.float32)
    X_test_np = np.array(X_test, dtype=np.float32)

    y_train = np.array(y_train, dtype=np.float32)
    y_test = np.array(y_test, dtype=np.float32)

    normalizer = Normalization(axis=-1)
    normalizer.adapt(X_train_np)

    print(normalizer.mean.numpy())
    print(normalizer.variance.numpy())

    reg_model = Sequential([
        normalizer, 
        Dense(units=1)
    ])

    reg_model.compile(
        SGD(learning_rate=0.001), loss='mean_squared_error')

    _history = reg_model.fit(
        X_train_np, y_train,
        epochs=100, 
        verbose=1, 
        validation_data=(X_test_np, y_test)
    )








