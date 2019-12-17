import requests


def get_photo():
    """Get a photo from the IP camera"""       
    url = 'http://172.16.12.131/Streaming/channels/1/picture'
    reponse = requests.get(url, auth=('admin', 'linux111'))
    if reponse.status_code == 200:
        return reponse.content
    else:
        print("Can't get any reponse")
