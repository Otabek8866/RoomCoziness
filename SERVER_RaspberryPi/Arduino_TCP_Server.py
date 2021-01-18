import socket
from time import localtime, strftime, sleep
import sqlite3
import random

MEASURE_TIMES = 10
WAITING_TIME_FOR_BUFFER = 1
WAITING_TIME = 10

# Difference Ranges for Random Number Generator 
# 1-teperature, 2-noise, 3- light, 4-co2, 5-humidity
Ran_Gen_Vals = [9, 50, 100, 100, 9]

# Server IP address and Port number
DEST_IP = '192.168.10.1'
DEST_PORT = 80

BUFFER_SIZE = 1024

# Creating a message to send the Server
string = '\n'
MESSAGE = string.encode("utf-8")

# connecting to the mainDB database
db = sqlite3.connect("/home/pi/Desktop/IoT Project/SERVER_RaspberryPi/DataBase/mainDB")
cr = db.cursor()

# Starting SQL statement for each room
roomA = 'INSERT INTO roomA(date, time, temperature, noise, light, co2, humidity) '
roomB = 'INSERT INTO roomB(date, time, temperature, noise, light, co2, humidity) '
roomC = 'INSERT INTO roomC(date, time, temperature, noise, light, co2, humidity) '

try:
	# every 2 minutes, the data is inserted into the database
	print("<<<<<----- Database is connected, Server started ----->>>>>")
	while True:
		while int(strftime("%H:%M", localtime())[4])%2 == 0:

			x = int(strftime("%H:%M", localtime())[4])
			# getting the timestamp values
			time_stamp_values = 'VALUES("' + strftime("%Y-%m-%d", localtime()) + '", "' + strftime("%H:%M", localtime())[0:4] + str(x) +'", "'
		    
		    # creating lists of values for each senor
			temperature_values = []
			noise_values = []
			light_values = []
			co2_values = []
			humidity_values = []

			for _ in range(MEASURE_TIMES):
				# Creating a new socket
				s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

				# Connect to the Arduino Server
				s.connect((DEST_IP, DEST_PORT))
				print("Client is connected")

				# Send a message to the Server
				s.send(MESSAGE)
				print("Cient is sending a message")
				sleep(WAITING_TIME_FOR_BUFFER)

				# Receiving data from the Server
				data = s.recv(BUFFER_SIZE)
				print("Client received data:", data)

				# closing the connection with user
				s.close()
				print("Client is disconnected")

				# Appending values to the lists
				val1, val2, val3 ,val4, val5 = data.decode("utf-8").split(':')
				temperature_values.append(float(val1))
				noise_values.append(float(val2))
				light_values.append(float(val3))
				co2_values.append(float(val4))
				humidity_values.append(float(val5))

				print('='*64)
				sleep(WAITING_TIME)

			print("Calculating average values and creating SQL statements")
			
			# Calculating avarage vlaues for Room A
			temperature_average = sum(temperature_values)/len(temperature_values)
			noise_average = sum(noise_values)/len(noise_values)
			light_average = sum(light_values)/len(light_values)
			co2_average = sum(co2_values)/len(co2_values)
			humidity_average = sum(humidity_values)/len(humidity_values)

			# Calculating avarage vlaues for Room B
			temperature_average2 = random.uniform(-1, 1)*Ran_Gen_Vals[0]+ temperature_average
			noise_average2 = random.uniform(-1, 1)*Ran_Gen_Vals[1] + noise_average
			light_average2 = random.uniform(-1, 1)*Ran_Gen_Vals[2] + light_average
			co2_average2 = random.uniform(-1, 1)*Ran_Gen_Vals[3] + co2_average
			humidity_average2 = random.uniform(-1, 1)*Ran_Gen_Vals[4] + humidity_average

			# Calculating avarage vlaues for Room C
			temperature_average3 = random.uniform(-1, 1)*Ran_Gen_Vals[0]+ temperature_average
			noise_average3 = random.uniform(-1, 1)*Ran_Gen_Vals[1] + noise_average
			light_average3 = random.uniform(-1, 1)*Ran_Gen_Vals[2] + light_average
			co2_average3 = random.uniform(-1, 1)*Ran_Gen_Vals[3] + co2_average
			humidity_average3 = random.uniform(-1, 1)*Ran_Gen_Vals[4] + humidity_average
			
			roomA_sensor_values = str(round(temperature_average, 2))+'", "'+str(round(noise_average, 2))+'", "'+str(round(light_average, 2))+'", "'+str(round(co2_average, 2))+'", "'+str(round(humidity_average, 2))+'");'
			roomB_sensor_values = str(round(temperature_average2, 2))+'", "'+str(round(noise_average2, 2))+'", "'+str(round(light_average2, 2))+'", "'+str(round(co2_average2, 2))+'", "'+str(round(humidity_average2, 2))+'");'
			roomC_sensor_values = str(round(temperature_average3, 2))+'", "'+str(round(noise_average3, 2))+'", "'+str(round(light_average3, 2))+'", "'+str(round(co2_average3, 2))+'", "'+str(round(humidity_average3, 2))+'");'

			# creating final SQL statements
			roomA_sql_statement = roomA + time_stamp_values + roomA_sensor_values
			roomB_sql_statement = roomB + time_stamp_values + roomB_sensor_values
			roomC_sql_statement = roomC + time_stamp_values + roomC_sensor_values

			try:
				# inserting values into the DB
				cr.execute(roomA_sql_statement)
				cr.execute(roomB_sql_statement)
				cr.execute(roomC_sql_statement)
				cr.connection.commit()
				print('+++++++++ SQL statements status ==> SUCCESS ++++++++++++')
				print("Inserted in", time_stamp_values[7:])
				print('='*64)

			except Exception as e:
				print(e)

except Exception as e:
	print("Error occured:", e)

	# closing connections with the database
	db.close()
	cr.close()
	print("Database connection is closed")
