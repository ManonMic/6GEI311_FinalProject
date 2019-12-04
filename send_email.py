import smtplib
from email.mime.text import MIMEText
from email.mime.image import MIMEImage
from email.mime.multipart import MIMEMultipart
import os


def send_email(dest, subject, body, body_img_file_name = None):
	mail = MIMEMultipart()
	mail['From'] = 'cameraexpress123@gmail.com'
	mail['Pass'] = 'LucasEnRetard123'
	mail['To'] = dest
	mail['Subject'] = subject
	text = MIMEText(body)
	mail.attach(text)
	
	if body_img_file_name:
		img_data = open(body_img_file_name, 'rb').read()
		image = MIMEImage(img_data, _subtype="jpg", name=os.path.basename(body_img_file_name))
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
