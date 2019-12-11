import smtplib
from email.mime.text import MIMEText
from email.mime.image import MIMEImage
from email.mime.multipart import MIMEMultipart
import os
import time


def send_email(dest, subject, body, image_bytestring=None):
	mail = MIMEMultipart()
	mail['From'] = 'cameraexpress123@gmail.com'
	mail['Pass'] = 'LucasEnRetard123'
	mail['To'] = dest
	mail['Subject'] = subject
	text = MIMEText(body)
	mail.attach(text)
	
	if image_bytestring:
		path = "images/" + str(time.time()) + ".jpg"
		image_bytestring.save(path)
		img_data = open(path, 'rb').read()
		image = MIMEImage(img_data, _subtype="jpg", name=os.path.basename(path))
		mail.attach(image)
	
	try:
		server = smtplib.SMTP_SSL('smtp.gmail.com', 465)
		server.ehlo()
		server.login(mail['From'], mail['Pass'])
	except ConnectionError:
		print('Login error')
		return

	try:
		server.sendmail(mail['From'], mail['To'], mail.as_string())
		print('Email sent')
	except:
		print('Error sending email')
		return

	server.quit()
