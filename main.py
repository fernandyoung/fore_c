from flask import Flask, render_template, url_for, request, redirect, session, send_file, flash
import numpy as np
from sklearn.metrics import mean_absolute_error
from sklearn.metrics import mean_absolute_percentage_error
from datetime import datetime, timedelta
import yfinance as yf
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import pandas as pd
import json
import database as db
import svr
import dstat
import io
import pytz
import base64
from werkzeug.security import check_password_hash

app = Flask(__name__)

#connection
app.secret_key = 'sasukeuchiha'
mysql = db.connection()

current = datetime.now(pytz.utc)

timezone = pytz.timezone('Asia/Jakarta')
today=current.astimezone(timezone)

seminggu = today+timedelta(days=6)
today = today.strftime("%Y-%m-%d")

@app.route('/')
def index():
	return render_template('index.html', active_page='home')
	pass

@app.route('/chart', methods=('GET', 'POST'))
def chart():
	#load setting
	with open('config.json', 'r') as file:
		data = json.load(file)

	if request.form.get('hari') == None:
		hari=1
		config = data['setting'][0]
	else:
		hari = request.form.get('hari')
		config = data['setting'][int(hari)-1]
		pass

	tf=['','1d', '1wk']

	data = yf.download("BBCA.JK", start="2017-01-01", end=today, interval=tf[int(hari)]) #1wk #1d
	data = pd.DataFrame(data)
	df = data.reset_index()
	df['Date'] = df['Date'].dt.strftime('%Y-%m-%d')

	#training data
	forecast_model = svr.SVRForecast(kernel= config['kernel'], C=float(config['c']), epsilon=float(config['epsilon']))
	X_train, X_test, y_train, y_test, y_for, y = forecast_model.test_split(tf[int(hari)])
	forecast_model.train(X_train, y_train)
	
	#savedata ke csv
	datacsv = df.iloc[-30:]
	datacsv = datacsv.reset_index(drop=True)
	datacsv.to_csv('BBCA.JK(30).csv')
	
	#grafik
	df = df.dropna()
	df = df.iloc[-8:, [0,4]]
	his = np.asarray(df)
	his
	ramal = his.tolist()

	data = his
	fore = ramal

	labels = [row[0] for row in data]
	values = [row[1] for row in data]
	valfore = [row[1] for row in fore]
	labfore = [row[0] for row in fore]

	if request.method=="POST":
		test = df
		test = test['Close']
		test = test.dropna()
		#now = datetime.now().date()

		#y_test = test[-1:].values
		h_data = y[-5:]

		i = y_for.reshape(-1,1)
		h_data = h_data.reshape(-1,1)
		if int(hari) == 1:
			y_pred=forecast_model.predict(i)
			y_pred= forecast_model.inverse_y(y_pred.reshape(1,-1))
			#besok = now
			tanggal = today
			riwayat=forecast_model.predict(h_data)
			riwayat=forecast_model.inverse_y(riwayat.reshape(1,-1))
			pass
		else:
			y_pred=forecast_model.predict(i)
			y_pred= forecast_model.inverse_y(y_pred.reshape(1,-1))
			tanggal = seminggu.strftime("%Y-%m-%d")
			riwayat=forecast_model.predict(h_data)
			riwayat=forecast_model.inverse_y(riwayat.reshape(1,-1))

		y_pred = [format(x,".2f") for x in y_pred[0]]
		fore.append([tanggal, str(y_pred[0])])

		labels = [row[0] for row in data]
		values = [row[1] for row in data]
		valfore = [row[1] for row in fore]
		labfore = [row[0] for row in fore]

		riwayt = np.round(riwayat,2)

		return render_template('chart.html',post=True,riwayat=riwayt, tanggal=tanggal, harga=str(y_pred[0]), v=hari, active_page='chart', labels=labels, values=values, vfore = valfore, lfore=labfore)
		pass

	return render_template('chart.html',active_page='chart',post=False, labels=labels, values=values, vfore = valfore, lfore=labfore)
	pass

@app.route('/test', methods=('GET', 'POST'))
def test():
	if request.method=="POST":
		#plt.clf()
		hari = request.form['range']
		if hari == "0":
			data = '1d'
		else:
			data = '1wk'
		pass
		#training data
		c = request.form['c']
		epsilon = request.form['epsilon']
		kernel = request.form['kernel']
		forecast_model = svr.SVRForecast(kernel=kernel, C=float(c), epsilon=float(epsilon))
		X_train, X_test, y_train, y_test, y_for, y = forecast_model.test_split(data)
		forecast_model.train(X_train, y_train)

		y_pred = forecast_model.predict(X_test)

		yp_n = y_pred

		ypred = forecast_model.inverse_y(y_pred)
		ytrain = forecast_model.inverse_y(y_train)
		ytest = forecast_model.inverse_y(y_test)
		Xtest = forecast_model.inverse_x(X_test)
		Xtrain = forecast_model.inverse_x(X_train)

		mae = mean_absolute_error(ytest, ypred)
		mape = mean_absolute_percentage_error(ytest, ypred)
		#dstat
		ds = dstat.dstatn(ytest.reshape(-1),ypred.reshape(-1))
		hasil = ds.dstathasil()

		x = range(len(ypred.reshape(-1)))

		plt.plot(x, ypred.reshape(-1), label='prediksi', marker='o')
		plt.plot(x, ytest.reshape(-1), label='asli')

		proses=1

		plt.xlabel('Data Point')
		plt.ylabel('Value')

		plt.legend()
		#plt.show()
		# ========
		buffer = io.BytesIO()
		plt.savefig(buffer, format='png')
		buffer.seek(0)
		plt.close()
		plot_data = base64.b64encode(buffer.getvalue()).decode('utf-8')

		# buffer.close()

	return render_template('admin.html', dstat=hasil, proses=proses, plot_data=plot_data,
		y_test=ytest,
		y_pred = ypred,
		y_train=ytrain[0][:10],
		X_train=Xtrain[:10],
		X_test=X_test[:10],
		XtrainN=X_train[:10],
		ytrainN=y_train[:10],
		hari=hari, mae=mae, mape=mape,kernel=kernel, c=c, epsilon=epsilon, active_page='admin')#
	pass

@app.route('/download')
def download():
	filename = 'BBCA.JK(30).csv'
	return send_file(filename,as_attachment=True)
	pass

@app.route('/admin', methods=('GET', 'POST'))
def admin():
	if session.get('tipe') == 7 :
		with open('config.json', 'r') as file: #baca json
			data = json.load(file)
		if request.method == 'POST':
			ranges = request.form['range']
			if ranges == "0":
				data['setting'][0] = {
					'range' : ranges,
					'c' : request.form['c'],
					'epsilon' : request.form['epsilon'],
					'kernel' : request.form['kernel']
				}
			else:
				data['setting'][1] = {
					'range' : ranges,
					'c' : request.form['c'],
					'epsilon' : request.form['epsilon'],
					'kernel' : request.form['kernel']
				}
			with open('config.json', 'w') as file:
				json.dump(data, file)
			flash('Data berhasil disimpan!', 'Success')
			pass
		pass	
		return render_template('admin.html', active_page='admin')
		pass
	else:
		return render_template('404.html')
	pass

@app.route('/signin', methods=('GET', 'POST'))
def signin():
	if request.method == 'POST':
		username = request.form['username']
		password = request.form['password']

		akun = mysql.check_username(username)
		if akun is None:
			flash('Waduh! password atau username salah!', 'danger')
			pass
		elif not check_password_hash(akun[2], password):
			flash('Waduh! password atau username salah!', 'danger')
		else:
			session['loggedin'] = True
			session['username'] = akun[1]
			session['tipe'] = akun[3]
			if akun[3] == 7:
				return redirect(url_for('admin'))
			else:
				return redirect(url_for('chart'))
		pass
	return render_template('signin.html')
	pass

@app.route('/signup', methods=('GET','POST'))
def signup():
	test=None
	if request.method == 'POST':
		username = request.form['username']
		password = request.form['password']
		akun = mysql.check_username(username)
		if akun is None:
			flash('Daftar berhasil! silahkan masuk!', 'Success')
			mysql.insert(username,password)
			test = 1
			pass
		else: 
			flash('Waduh! username sudah terpakai!', 'danger')
			test = 0
	return render_template('signup.html', test=test)
	pass

@app.route('/info')
def info():
	return render_template('info.html')

@app.route('/logout')
def logout():
	session.pop('loggedin', None)
	session.pop('username', None)
	session.pop('tipe', None)
	return redirect(url_for('chart'))

@app.errorhandler(404)
def page_not_found(e):
	return render_template('404.html')
	pass

if __name__ == '__main__':
	#app.run(host="0.0.0.0", port=5000, debug=True)
	app.run(debug=True)
