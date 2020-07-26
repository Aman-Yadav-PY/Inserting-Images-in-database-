import os, time 
import pymysql.cursors
import pymysql
import binascii

t = time.localtime()
date_time = f"{t[0]}-{t[1]}-{t[2]} {t[3]}:{t[4]}:{t[5]}"

connector = pymysql.connect(
	host='ipaddress',
	user='username',
	password='password',
	db='customer',
	charset='utf8mb4',
	cursorclass=pymysql.cursors.SSDictCursor)

with connector.cursor() as cursor:
	cursor.execute("DROP TABLE safe")
	cursor.execute("""CREATE TABLE safe(
		date_time datetime,
		Name VARCHAR(30),
		Type VARCHAR(30),
		Data mediumblob
		)""")

	def insert(date, name, Type, data):
		cursor.execute("""INSERT INTO safe VALUES('%s', '%s', '%s', '%s')"""%(date, name, Type, data))

	for images in os.listdir():
		if images.endswith('.png') or images.endswith('.gif') or images.endswith('.jpg'):
			with open(images, 'rb') as img_file:
				data = binascii.b2a_hex(img_file.read()).decode('utf-8')

				n, t = images.split('.')

				insert(date_time, n, t, data)

			connector.commit()



connector.close()
