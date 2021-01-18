from flask import Flask, render_template, request, url_for, redirect, send_file
import sqlite3
import numpy as np

# libraries for making a report
from pandas import DataFrame
import matplotlib.pyplot as plt
from matplotlib.backends.backend_pdf import PdfPages

# Constant values
COLUMN_LIST = ["date", "time", "temperature", "noise", "light", "co2", "humidity"]
WEIGHTS = []
ROOM_NAMES = ['Room A', 'Room B', 'Room C']
Last_Date = ''
Last_Time = ''
Cozy_Status_Dict = {'A':"Really Cozy", 'B':"Really Cozy", 'C':"Really Cozy", 'A_degree':50, 'B_degree':50, 'C_degree':50}
COUNT_Report = 10

# Admin credentials
ADMIN_EMAIL = 'admin'
ADMIN_PASS = 'admin'
W_LIST =   ['tempoverhumidity', 'tempoverco2', 'tempovernoise', 'tempoverlight',
			'humidityoverco2', 'humidityovernoise', 'humidityoverlight',
			'co2overnoise', 'co2overlight', 'noiseoverlight']

roomA_dict = {}
roomB_dict = {}
roomC_dict = {}

app = Flask(__name__)

# connecting to the DataBase
db = sqlite3.connect("/home/pi/Desktop/IoT Project/SERVER_RaspberryPi/DataBase/mainDB", check_same_thread=False)


# Calculation of weights of parameters
def cal_weights(matrix):

	A = np.array(matrix)

	C1=A[0:5, 0:1]
	C2=A[0:5, 1:2]
	C3=A[0:5, 2:3]
	C4=A[0:5, 3:4]
	C5=A[0:5, 4:5]

	Norm_C1=C1/C1.sum()
	Norm_C2=C2/C2.sum()
	Norm_C3=C3/C3.sum()
	Norm_C4=C4/C4.sum()
	Norm_C5=C5/C5.sum()

	A[0:5, 0:1]=Norm_C1
	A[0:5, 1:2]=Norm_C2
	A[0:5, 2:3]=Norm_C3
	A[0:5, 3:4]=Norm_C4
	A[0:5, 4:5]=Norm_C5

	weights=[]
	for num in range(5):
	    weights.append(A[num].sum()/5)
	
	return weights


# Calculation of coziness level
def cal_cozy_room(room_values, name):
	total = 0
	coz_val = "Really Cozy"

	# Calculating room coziness level
	for w, r in zip(WEIGHTS, room_values):
		total += w*r

	# setting coziness values to rooms
	if total <= 69 and total >= 40:
	# noise
		coz_val = 'Somehow Cozy'
	elif total <= 39:
		coz_val = 'in Alarming State'

	Cozy_Status_Dict[name] = coz_val
	Cozy_Status_Dict[name+'_degree'] = round(total)

	return int(round(total))


# extraction of sensor values for coziness calculation
def coziness_values(cozy_val_room):
	room = []
	for item_from_cozy_val_room in cozy_val_room:
		room.append(round(float(item_from_cozy_val_room), 2))

	roomX_values = []
	# temperature
	value = room[0]
	if 16 <= value <= 22:
		roomX_values.append(100)
	elif (13 <= value <= 15) or (23 <= value <= 26):
		roomX_values.append(50)
	else:
		roomX_values.append(0)

	value = room[1]
	if 0 <= value <= 40:
		roomX_values.append(100)
	elif 41 <= value <= 70:
		roomX_values.append(50)
	else:
		roomX_values.append(0)

	# light
	value = room[2]
	if 200 <= value <= 500:
		roomX_values.append(100)
	elif (50 <= value <= 199) or (501 <= value <= 1000):
		roomX_values.append(50)
	else:
		roomX_values.append(0)

	# co2
	value = room[3]
	if 0 <= value <= 800:
		roomX_values.append(100)
	elif 801 <= value <= 2000:
		roomX_values.append(50)
	else:
		roomX_values.append(0)

	# humidity
	value = room[4]
	if 30 <= value <= 60:
		roomX_values.append(100)
	elif (25 <= value <= 29) or (61 <= value <= 70):
		roomX_values.append(50)
	else:
		roomX_values.append(0)

	return roomX_values


def prepare_report(df_temperature, df_noise, df_light, df_co2, df_humidity):

	with PdfPages('Report.pdf', 'w+') as export_pdf:
                
		plt.plot(df_temperature['time'], df_temperature['temperature'], color='red', marker='o')
		plt.title('Temperature', fontsize=14)
		plt.xlabel('Time in minutes', fontsize=8)
		plt.ylabel('Temperature in Celcius', fontsize=8)
		plt.grid(True)
		export_pdf.savefig()
		plt.close()

		plt.plot(df_noise['time'], df_noise['noise'], color='red', marker='o')
		plt.title('Noise', fontsize=14)
		plt.xlabel('Time in minutes', fontsize=8)
		plt.ylabel('Noise in dB', fontsize=8)
		plt.grid(True)
		export_pdf.savefig()
		plt.close()

		plt.plot(df_light['time'], df_light['light'], color='red', marker='o')
		plt.title('Light', fontsize=14)
		plt.xlabel('Time in minutes', fontsize=8)
		plt.ylabel('Light in Celcius', fontsize=8)
		plt.grid(True)
		export_pdf.savefig()
		plt.close()

		plt.plot(df_co2['time'], df_co2['co2'], color='red', marker='o')
		plt.title('Carbon Dioxide', fontsize=14)
		plt.xlabel('Time in minutes', fontsize=8)
		plt.ylabel('CO2 in ppm', fontsize=8)
		plt.grid(True)
		export_pdf.savefig()
		plt.close()

		plt.plot(df_humidity['time'], df_humidity['humidity'], color='red', marker='o')
		plt.title('Humidity', fontsize=14)
		plt.xlabel('Time in minutes', fontsize=8)
		plt.ylabel('Humidity in %', fontsize=8)
		plt.grid(True)
		export_pdf.savefig()
		plt.close()
		print("PDF report is ready")


# Main page
@app.route('/')
def index():
	cr = db.cursor()

	# Fetching the last inserted rows from DataBase
	roomA_cursor = tuple(cr.execute("SELECT * FROM (SELECT * FROM roomA ORDER BY Id DESC LIMIT 1);").fetchone())	
	roomB_cursor = tuple(cr.execute("SELECT * FROM (SELECT * FROM roomB ORDER BY Id DESC LIMIT 1);").fetchone())
	roomC_cursor = tuple(cr.execute("SELECT * FROM (SELECT * FROM roomC ORDER BY Id DESC LIMIT 1);").fetchone())

	cr.close()
	
	roomA_cursor_copy = list(roomA_cursor)[3:]
	roomB_cursor_copy = list(roomB_cursor)[3:]
	roomC_cursor_copy = list(roomC_cursor)[3:]

	# setting last date and time value
	Last_Date = roomA_cursor[0] 
	Last_Time = roomA_cursor[1]

	# getting values for Room A and B
	for i, j in zip(COLUMN_LIST[2:], roomA_cursor[3:]):
		roomA_dict[i] = j

	for x, y in zip(COLUMN_LIST[2:], roomB_cursor[3:]):
		roomB_dict[x] = y

	for a, b in zip(COLUMN_LIST[2:], roomC_cursor[3:]):
		roomC_dict[a] = b


	rooms = {}
	keys_list = []
	keys_list.append(cal_cozy_room(coziness_values(roomA_cursor_copy), "A"))
	keys_list.append(cal_cozy_room(coziness_values(roomB_cursor_copy), "B"))
	keys_list.append(cal_cozy_room(coziness_values(roomC_cursor_copy), "C"))
	
	rooms = sorted([(keys_list[0], 'Room A'), (keys_list[1], 'Room B'), (keys_list[2], 'Room C')], key=lambda x: x[0], reverse=True)

	result = {}
	# Room names
	result['number_1_room'] = rooms[0][1]
	result['number_2_room'] = rooms[1][1]
	result['number_3_room'] = rooms[2][1]
	# Room coziness values
	result['room_1_degree'] = rooms[0][0]
	result['room_2_degree'] = rooms[1][0]
	result['room_3_degree'] = rooms[2][0]
	
	return render_template('Main-Page.html', **result)


# Individual room page
@app.route("/rooms/<room_name>", methods=["GET", "POST"])
def individual_room(room_name):

	if room_name == 'Room A':
		selected_room = roomA_dict
	elif room_name == 'Room B':
		selected_room = roomB_dict
	elif room_name == 'Room C':
		selected_room = roomC_dict
	else:
		return "<h7>You selected a wrong room, Please go back and select again<h7>"

	for i in COLUMN_LIST[2:]:
		selected_room[i] = round(float(selected_room[i]))

	selected_room['room_name'] = room_name
	selected_room['cozy_status'] = Cozy_Status_Dict[room_name[-1]]
	selected_room['cozy_degree'] = Cozy_Status_Dict[room_name[-1]+'_degree']
	
	return render_template('Individual-Room.html', **selected_room)


# Admin's username and password checking
@app.route("/admin/", methods=["POST"])
def admin_login():
	login = request.form.get('username')
	password = request.form.get('pass')
	print(login, password)

	if login == ADMIN_EMAIL and password == ADMIN_PASS:
		return render_template('admin.html')
	else:
		return "<h11>Password or username is not correct</h11>"


# (Admin API page) Calculating new weight values for AHP 
@app.route("/weight/", methods=["GET", "POST"])
def admin_api():
	w_dict = {}
	if request.method != 'POST':
		return "Bad Gateway, Try it later :("

	for item in W_LIST:
		w_dict[item] = float(request.form.get(item))

	new_array = [[1, w_dict['tempovernoise'], w_dict['tempoverlight'], w_dict['tempoverco2'], w_dict['tempoverhumidity']],
				[round(1/w_dict['tempovernoise'], 2), 1, w_dict['noiseoverlight'], round(1/w_dict['co2overnoise'], 2), round(1/w_dict['humidityovernoise'], 2)],
				[round(1/w_dict['tempoverlight'], 2), round(1/w_dict['noiseoverlight'], 2), 1, round(1/w_dict['co2overlight'], 2), round(1/w_dict['humidityoverlight'], 2)],
				[round(1/w_dict['tempoverco2'], 2), w_dict['co2overnoise'], w_dict['co2overlight'], 1, round(1/w_dict['humidityoverco2'], 2)],
				[round(1/w_dict['tempoverhumidity'], 2), w_dict['humidityovernoise'], w_dict['humidityoverlight'], w_dict['humidityoverco2'], 1]]
			
	WEIGHTS = cal_weights(new_array)

	return redirect(url_for('index'))


# Report download page(function) for selected room
@app.route("/report/<room_id>", methods=["GET"])
def download_report(room_id):

	room_id = room_id[-1]
	
	if room_id not in ['A', 'B', 'C']:
	    return "Wrong selection"
	room_id = "room" + room_id

	# creating a new cursor for data retrival
	cr2 = db.cursor()

	time_data = []
	temperature_data = []
	noise_data = []
	light_data = []
	co2_data = []
	humidity_data = []

	raw_data = list(cr2.execute("SELECT * FROM (SELECT * FROM {0} ORDER BY Id DESC LIMIT {1}) ORDER BY Id;".format(room_id, COUNT_Report)).fetchall())

	cr2.close()

	for row in raw_data:
	    time_data.append(row[2])
	    temperature_data.append(row[3])
	    noise_data.append(row[4])
	    light_data.append(row[5])
	    co2_data.append(row[6])
	    humidity_data.append(row[7])    

	df_temperature = DataFrame({'temperature':temperature_data, "time":time_data},columns=['temperature','time'])
	df_noise = DataFrame({'noise':noise_data, "time":time_data},columns=['noise','time'])
	df_light = DataFrame({'light':light_data, "time":time_data},columns=['light','time'])
	df_co2 = DataFrame({'co2':co2_data, "time":time_data},columns=['co2','time'])
	df_humidity = DataFrame({'humidity':humidity_data, "time":time_data},columns=['humidity','time'])

	prepare_report(df_temperature, df_noise, df_light, df_co2, df_humidity)

	return send_file('Report.pdf', attachment_filename='Report.pdf')


@app.route("/login-page/", methods=["GET"])
def login_page_forwarding():
	return render_template('login-page.html')

if __name__ == "__main__":
	
	initial_matrix=[[1, 5, 5, 1, 3],
			[0.2, 1, 1, 0.2, 0.2],
			[0.2, 1, 1, 0.2, 0.143],
			[1, 5, 5, 1, 0.33],
			[0.33, 5, 7, 3, 1]]
	
	WEIGHTS = cal_weights(initial_matrix)

	app.run(debug=True, host='192.168.10.10', port=80)
