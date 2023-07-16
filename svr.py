from sklearn.svm import SVR
from sklearn.model_selection import train_test_split
import numpy as np
import pandas as pd
from sklearn.preprocessing import StandardScaler
from datetime import datetime, timedelta
import yfinance as yf

today = datetime.today().date()
yesterday = today+timedelta(days=1)
yesterday = yesterday.strftime("%Y-%m-%d")

class SVRForecast(object):
	"""docstring for SVRForecast"""
	def __init__(self, C=1.0, epsilon=0.1, kernel='rbf'):
		self.C = C
		self.epsilon = epsilon
		self.kernel = kernel
		self.regressor = SVR(kernel=self.kernel, C=self.C, epsilon=self.epsilon)
		self.scaler = StandardScaler()

	def train(self, X_train, y_train):
		self.regressor.fit(X_train, y_train)
		pass

	def predict(self, X_test):
		y_pred = self.regressor.predict(X_test)
		return y_pred

	def inverse_y(self, y):
		asli = self.scaler.inverse_transform(y.reshape(1,-1))
		return asli

	def inverse_x(self, x):
		asli = self.scaler.inverse_transform(x)
		return asli

	def test_split(self, time):
		data = yf.download("BBCA.JK", start="2022-01-01", end=yesterday, interval=time) #1wk #1d
		data = pd.DataFrame(data)
		df = data.reset_index()
		df['X'] = df['Close'].shift(1)
		df = df.iloc[:, [7,4]]
		df = df.dropna()

		x = df.iloc[:, :-1].values.astype(float)
		y = df.iloc[:, -1].values.astype(float)

		x = self.scaler.fit_transform(x)
		y = self.scaler.fit_transform(y.reshape(-1,1))

		y_for = y[-1]

		y = y[:-1]
		x = x[:-1]

		X_train, X_test, y_train, y_test = train_test_split(x, y, test_size=0.2, random_state=0)
		return X_train, X_test, y_train, y_test, y_for, y