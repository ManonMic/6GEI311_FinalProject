import requests
import shutil

url = 'http://172.16.12.131/Streaming/channels/1/picture'
reponse = requests.get(url, auth=('admin','linux111'))
if reponse.status_code == 200:
    with open(r"C:\Users\labop2\Desktop\hrllo.jpg", 'wb') as f:
        f.write(reponse.content)
