import requests
import smtplib
import time
import logging
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from datetime import datetime
import ssl
import os
from colorama import Fore, Style, init

init(autoreset=True)

# 配置日志
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

# logo
llooggoo = r'''
  _   _                        ___ ____    ____            _     
 | | | | ___  _ __ ___   ___  |_ _|  _ \  |  _ \ _   _ ___| |__  
 | |_| |/ _ \| '_ ` _ \ / _ \  | || |_) | | |_) | | | / __| '_ \ 
 |  _  | (_) | | | | | |  __/  | ||  __/  |  __/| |_| \__ \ | | |
 |_| |_|\___/|_| |_| |_|\___| |___|_|     |_|    \__,_|___/_| |_|                                                           
  By KiLoyal | Version 1.4  |                                                       
'''

# 根据系统识别清空终端
if os.name == 'nt':
    os.system('cls')
else:
    os.system('clear')



# 打印logo

print(Fore.GREEN + llooggoo)
# 配置
config = {
    "smtp": {
        "server": "",
        "port": ,
        "username": "",
        "password": "",
        "use_ssl": True
    },
    "email": {
        "to_address": "",
        "from_address": "",
        "subject": "家的公网IP地址已经修改为{now_ip}"
    },
    "api_server": {
        "name": "pconline", # 默认API 感谢太平洋电脑网提供的API
        "url": "https://whois.pconline.com.cn/ipJson.jsp?ip=&json=true"
    },
    "check_interval_seconds": 10  # 单位为秒
}

# 获取公网IP地址
def get_public_ip(api_server):
    try:
        response = requests.get(api_server["url"], timeout=5)
        response.raise_for_status()
        
        # 尝试解析响应数据
        data = response.json()
        ip = data.get("ip")
        
        if ip:
            logger.info(Fore.GREEN + f"获取到了现在的IP地址 (=^-ω-^=): {ip}")
            return ip
        else:
            logger.warning(Fore.YELLOW + "无法从API获取IP地址(′゜ω。‵) 试试其他API吧")
            return None
    except requests.RequestException as e:
        logger.error(Fore.RED + f"哇啊啊 API调用失败啦(╥_╥): {api_server['name']}: {e}")
        logger.info(Fore.YELLOW + "等我有钱了，一定上线一个API服务器(￣▽￣)")
        return None

# 发送警告通知
# def sendWarring(previous_ip, current_ip):
#     smtp_config = config["smtp"]
#     email_config = config["email"]
#     interval_seconds = config["check_interval_seconds"]
    
#     # 设置邮件内容
#     message = MIMEMultipart()
#     message["From"] = email_config["from_address"]
#     message["To"] = email_config["to_address"]
#     message["Subject"] = email_config["subject"].format(now_ip=current_ip)

#     # HTML内容
#     body = f"""
#     <html>
#         <head>
#             <style>
#                 body {{
#                     display: flex;
#                     justify-content: center;
#                     align-items: center;
#                     height: 100vh;
#                     background-color: #f7f7f7;
#                 }}
#                 .container {{
#                     text-align: center;
#                     padding: 20px;
#                    border-radius: 10px;
#                 }}
#                 h1 {{
#                     font-size: 24px;
#                     color: #333333;
#                 }}
#                 p {{
#                     font-size: 16px;
#                     color: #666666;
#                 }}
#             </style>
#         </head>
#         <body>
#             <div class="container">
#                 <img src="https://s21.ax1x.com/2024/11/04/pArzONq.jpg" alt="表情包" width="120" height="120">
#                 <h1>家里出现网络连接问题！</h1>
#                 <p>出现时间</p>
#                 <{datetime.now().strftime('%Y-%m-%d %H:%M:%S')}>
#                 <p>原因日志</p>
#                 <pre>{logger.warring}</pre>
#                 <p>原IP地址: {previous_ip}</p>
#                 <p>现在的IP地址: {current_ip}</p>
#                 <p>请及时处理，以免影响使用。</p>
#             </div> 

#         </body>
#     </html>
#         """
#     message.attach(MIMEText(body, "html"))
    # 发送邮件
    # try:
    #     with smtplib.SMTP(smtp_config["server"], smtp_config["port"]) as server:
    #         server.starttls()
    #         server.login(smtp_config["username"], smtp_config["password"])
    #         server.sendmail(message["From"], message["To"], message.as_string())
    #     logger.info(Fore.GREEN + f"邮件已发送: {message['To']}")
    # except Exception as e:
    #     logger.error(Fore.RED + f"邮件发送失败: {e}")
    #     return None
# 发送邮件通知
def send_email(previous_ip, current_ip):
    smtp_config = config["smtp"]
    email_config = config["email"]
    interval_seconds = config["check_interval_seconds"]
    
    # 设置邮件内容
    message = MIMEMultipart()
    message["From"] = email_config["from_address"]
    message["To"] = email_config["to_address"]
    message["Subject"] = email_config["subject"].format(now_ip=current_ip)

    # HTML内容
    body = f"""
    <html>
        <head>
            <style>
                body {{
                    display: flex;
                    justify-content: center;
                    align-items: center;
                    height: 100vh;
                    background-color: #f7f7f7;
                }}
                .container {{
                    text-align: center;
                    padding: 20px;
                    border-radius: 10px;
                    box-shadow: 0 4px 8px rgba(0, 0, 0, 0.1);
                    background-color: #ffffff;
                    max-width: 400px;
                    margin: auto;
                }}
                h1 {{
                    font-size: 24px;
                    color: #333333;
                }}
                p {{
                    font-size: 16px;
                    color: #666666;
                }}
                .btn {{
                    display: inline-block;
                    padding: 10px 20px;
                    margin-top: 20px;
                    font-size: 16px;
                    color: #ffffff;
                    background-color: #007bff;
                    border-radius: 5px;
                    text-decoration: none;
                }}
            </style>
        </head>
        <body>
            <div class="container">
                <img src="https://s21.ax1x.com/2024/11/04/pArzONq.jpg" alt="表情包" width="120" height="120">
                <h1>家 的 IP地址已经改变</h1>
                <p>原IP地址: {previous_ip}</p>
                <p>现在的IP地址: {current_ip}</p>
                <p>上一次IP更新时间: {interval_seconds / 60}分钟</p>
                <p>本次IP更新时间: {datetime.now()}</p>
            </div>
        </body>
    </html>
    """
    message.attach(MIMEText(body, "html"))

    # 发送邮件
    context = ssl.create_default_context()
    try:
        with smtplib.SMTP_SSL(smtp_config["server"], smtp_config["port"], context=context) as server:
            server.login(smtp_config["username"], smtp_config["password"])
            server.sendmail(
                email_config["from_address"],
                email_config["to_address"],
                message.as_string()
            )
        logger.info(Fore.GREEN + "邮件发送成功! ฅ^•ﻌ•^ฅ")
    except Exception as e:
        logger.error(Fore.RED + f"邮件发送失败了 (′゜ω。‵) : {e}")


def checkInternatConnection(): 
    # 根据ping网关记录网络信息 外网链接判断请求返回值
    try:
        responseInternet = subprocess.check_output(["ping", "114.114.114.114"], timeout=5)
        if responseInternet.decode().find("TTL") != -1:
            return True
        else:
            return False
    except Exception as e:
        logger.error(Fore.RED + f"网络连接失败了 (｡•́︿•̀｡) : {e}")
    return False

def checkIntranetConnection():
    # 根据ping网关记录网络信息 内网链接判断请求返回值
    try:
        responseIntranet = subprocess.check_output(["ping", '172.16.1.1'], timeout=5)
        if responseIntranet.decode().find("TTL") != -1:
            return True
        else:
            return False
    except Exception as e:
        logger.error(Fore.RED + f"网关连接失败了 (｡•́︿•̀｡) : {e}")


# 保留离线警告日志 发送到邮箱
def offlineWarring ():
    # 记录离线日志和出现时间戳
    with open("offline.log", "a") as file:
        file.write(f"{datetime.now()} 连接失败了\n")


# 主程序逻辑
def main():
    api_server = config["api_server"]
    check_interval = config["check_interval_seconds"]
    last_ip = None
    ip_file = "last_ip.txt"

    # 检查之前保存的IP地址
    if os.path.exists(ip_file):
        with open(ip_file, "r") as file:
            last_ip = file.read().strip()
        logger.info(Fore.CYAN + f"喔！加载了上一次的IP地址 ᕕ ( ᐛ ) ᕗ，地址为: {last_ip}")
    try:
        while True:
            current_ip = get_public_ip(api_server)
            if current_ip is None:
                logger.warning(Fore.YELLOW + "_(┐ ◟;ﾟдﾟ)ノ 无法获取IP地址，请检查API服务器是否正常工作或是否有网络连接。")
            elif current_ip != last_ip:
                logger.info(Fore.GREEN + f"IP已经从 {last_ip} 变为 {current_ip} 啦！⁽⁽٩(๑˃̶͈̀ ᗨ ˂̶͈́)۶⁾⁾")
                send_email(last_ip, current_ip)
                last_ip = current_ip
                # 保存最新IP
                with open(ip_file, "w") as file:
                    file.write(current_ip)
                logger.info(Fore.CYAN + f"历史IP信息保存成功了喔！((꜆꜄꜆ ˙꒳˙)꜆꜄꜆: {current_ip}")
            else:
                logger.warning(Fore.RED + "啊，找不到到新的IP地址，那就不更新了吧. (′゜ω。‵) ")
            
            # 等待下一次检测
            logger.info(Fore.BLUE + f"等待 {check_interval} 秒后再次检查... ( ˊ̱˂˃ˋ̱ ) ")
            time.sleep(check_interval)

    except KeyboardInterrupt:
        logger.error(Fore.RED + "手动退出了.../ᐠ .ᆺ. ᐟ\ﾉ")

# 截获KeyboardInterrupt异常，并退出程序

if __name__ == "__main__":
    main()