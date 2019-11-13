import requests
import shutil
import time
import ffmpeg

url = 'http://172.16.12.131/Streaming/channels/1/picture'
# i = 0



# while i < 10:
    # reponse = requests.get(url, auth=('admin','linux111'))
    # if reponse.status_code == 200:
        # with open(location, 'wb') as f:
            # f.write(reponse.content)
    # i++
    # location.replace('0',i)

for i in range(10):
	reponse = requests.get(url, auth=('admin', 'linux111'))
	if reponse.status_code == 200:
		location = r"C:\Users\labop2\Desktop\images\img" + str(i) + ".jpg"
		print (location)
		with open(location, 'wb') as f:
			f.write(reponse.content)


