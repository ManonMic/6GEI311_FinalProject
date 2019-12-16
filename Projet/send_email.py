import smtplib
import numpy as np
from email.mime.text import MIMEText
from email.mime.image import MIMEImage
from email.mime.multipart import MIMEMultipart
import os
from datetime import datetime

from PIL import Image


def send_email(dest, subject, body, image_bytestring=None):
	mail = MIMEMultipart()
	mail['From'] = 'cameraexpress123@gmail.com'
	mail['Pass'] = 'LucasEnRetard123'
	mail['To'] = dest
	mail['Subject'] = subject
	text = MIMEText(body)
	mail.attach(text)
	
	if image_bytestring is not None:
		path = "images/" + str(datetime.now()) + ".png"
		rescaled = (255.0 / image_bytestring.max() * (image_bytestring - image_bytestring.min())).astype(np.uint8)
		image = Image.fromarray(rescaled)
		image.save(path)
		img_data = open(path, 'rb').read()
		image = MIMEImage(img_data, _subtype="jpg", name=os.path.basename(path))
		mail.attach(image)
		os.remove(path=path)
	
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
