# Automatic Check Public IP address And Push Notifications
## Automatically detect public IP and send notifications
This program is a Python script for dynamic public address detection. It obtains the current public IP address through the public API and compares it with the last detected IP address. If the IP address changes, the program will send an email notification containing the new IP address. The email is sent using the SMTP protocol, and the email template uses HTML syntax, including the current IP address, the previous IP address, the email sending time, and the current time.
| [English](./README_EN.md) | [Simplified Chinese](./README.md) |
![](https://img.shields.io/badge/Python-3.10-blue) ![](https://img.shields.io/badge/SMTP-465-green) ![](https://img.shields.io/badge/HTML-5.0-yellow)![](https://img.shields.io/github/license/Mapleawaa/Check-IP-And-Push-Notifications) ![](https://img.shields.io/github/issues/Mapleawaa/Check-IP-And-Push-Notifications)
![](https://img.shields.io/github/stars/Mapleawaa/Check-IP-And-Push-Notifications) ![](https://img.shields.io/github/forks/Mapleawaa/Check-IP-And-Push-Notifications)
![logo](./icon.jpg)
## Description

1. Check if the current public IP address is the same as the last detected IP address. If the same, no action is taken.
2. If different, write the variable with the new IP address and send an email to the specified email address through a fixed email template. The email uses the SMTP protocol.

## Function
1. Get the current public IPv4 address through the public API (api.ip.sb).
You can also get the public API list through the pre-configured json file, the format is: {"requsetServer_meitu": {"url": "https://webapi-pc.meitu.com/common/ip_location","requsetServer_ipcn": {"url": "https://www.ip.cn/api/index?ip=&type=0"}
2. Check every 5 minutes whether the IP address has changed 0.
3. Send the changed IP address email via SMTP protocol.
4. The email template uses HTML syntax, including the current IP address, the previous IP address, the email sending time and the current time.

## Implement functions
- [x] Get the current public IP address
- [x] Check if the IP address has changed
- [x] Send email notifications
- [x] The email template uses HTML syntax
- [x] The email template contains the current IP address, the previous IP address, the email sending time and the current time
- [x] The IP usage time record is being fixed and will now be displayed as 10 minutes
- [ ] Access different notification methods
- [ ] The email template supports different formats, such as plain text, Markdown, etc.
- [ ] Add log records
- [ ] Record offline logs

## Pre-configuration information
!!! note Note
    The pre-configuration information is in the config variable in the program, please make sure to modify it.

    The configuration format is as follows
```json
config = {
"smtp": {
"server": "smtp.163.com", # Mail server address
"port": 465, # Mail server port
"username": "maverick@163.com", # Mail email account
"password": "ZDkg8yLUDTr4nV8j", # Mail email password, usually the generated authorization code
"use_ssl": True # Enable SSL encryption
},
"email": {
"to_address": "testemailaddr@gmail.com", # Receiving email account
"from_address": "sendmailaddr@163.com", # Sending email account
"subject": "The public IP address of the home has been changed to {now_ip}" # Email subject
},
"api_server": {
"name": "pconline", # Default API Thanks to PConline for providing the API
"url": "https://whois.pconline.com.cn/ipJson.jsp?ip=&json=true"
},
"check_interval_seconds": 600 # Unit is seconds, detection interval
}
```

## Email content
The email content includes the current IP address, previous IP address, email sending time and current time.
You can modify it yourself, modify it in the `send_email` function in the program
Default email content preview

![Preview](./web-preview.png)

## Program environment
Python 3.10

## Special thanks
* [pconline](https://whois.pconline.com.cn/ipJson.jsp?ip=&json=true) Thanks to PConline for providing the API
* [api.ip.sb](https://api.ip.sb/geoip) Thanks to api.ip.sb for providing the API
* [jetBrains PyCharm](https://www.jetbrains.com/pycharm/) Thanks to jetBrains for providing the IDE

![pycharmlogo](./Pycharm.png)