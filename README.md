# 6GEI311_FinalProject

By Lucas Azurduy, Marc-Olivier Guadreault-Villeneuve, Manon Michelet and Jean-Michel Plourde.

Conception of a software used to detect in images from an IP camera.

## Getting Started
These instructions will get you a copy of the project up and running on your local machine for development and testing purposes.

### Prerequisites
* Python36 installed
* Path to pip.exe and to python.exe in your environnement path
* A computer in the P2-1060 lab at UQAC or any computer plugged into the labeled *NET* ports

### Installing
- Open a command, navigate to the desired directory and clone the project from this repository
```
git clone https://github.com/ManonMic/6GEI311_FinalProject.git
```
- Install the project dependencies
```
pip install -r requirements.txt
```

## Using the software
- Open a command prompt
- Move to the installatioin directory at *installation_directory\6GEI311_FinalProject\Projet*
- Run the python script
```
python interface.py
```
- Use the software

## Features
- Email notification on/off : Disable or enable email notifications.
- Send test email: Send a test email that bypass any cool down timer or disabler.
- Every half second, each processed images appear appear on screen. If there is movement, a red rectangle will identify it and notifications will be sent according to the parameters.

## Parameters
- There is a cool down timer for sending email notifications.
- Email notifications can be toggled on or off.
- The test email functionnality is not subjected to the cool down timer nor deactivation of the email sending feature. Users should be cautious with it as to not get the sending email server to be flagged as spam.
- Acquired and treated images are loaded into memory. If memory is scarce, consider reducing the acquisition rate.
- Images are only written to the disk, once at a time, for attachment to notification emails and are promptly deleted afterward. The notification cool down timer should prevent memory cell fatigue from frequent read/write.
