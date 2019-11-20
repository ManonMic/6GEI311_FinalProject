import smtplib
from email.mime.text import MIMEText
from email.mime.image import MIMEImage
from email.mime.multipart import MIMEMultipart
import os

def EnvoyerMail(dest, subject, body, ImgFileName = None):
	#gmail_user = 'cameraexpress123@gmail.com'
	#gmail_password = 'LucasEnRetard123'
	
	mail = MIMEMultipart()
	mail['From'] = 'cameraexpress123@gmail.com'
	mail['Pass'] = 'LucasEnRetard123'
	mail['To'] = dest
	mail['Subject'] = subject
	text = MIMEText(body)
	mail.attach(text)
	
	if ImgFileName != None:		
		img_data = open(ImgFileName, 'rb').read()
		image = MIMEImage(img_data, _subtype="jpg", name=os.path.basename(ImgFileName))
		mail.attach(image)
	
	try:
		server = smtplib.SMTP_SSL('smtp.gmail.com', 465)
		server.ehlo()
		server.login(mail['From'], mail['Pass'])
	except:
		print('Erreur Login')
		return
	try:
		server.sendmail(mail['From'], mail['To'], mail.as_string())
		print('Mail Envoyer')
		return 
	except:
		print('Erreur envoie mail')
		return 
	server.quit()