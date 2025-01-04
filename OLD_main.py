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

# 你正在使用的版本为 : Beta 1.4
# 开源地址 : https://github.com/Mapleawaa/Check-IP-And-Push-Notifications
# 如果个人使用 请勿删除本段注释
# 如遇到问题 请创建issue

# 配置日志
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

# logo
llooggoo = r'''
                                                                                                    
_|_|_|  _|_|_|                  _|_|_|  _|    _|  _|_|_|_|    _|_|_|  _|    _|  _|_|_|_|  _|_|_|    
  _|    _|    _|              _|        _|    _|  _|        _|        _|  _|    _|        _|    _|  
  _|    _|_|_|    _|_|_|_|_|  _|        _|_|_|_|  _|_|_|    _|        _|_|      _|_|_|    _|_|_|    
  _|    _|                    _|        _|    _|  _|        _|        _|  _|    _|        _|    _|  
_|_|_|  _|                      _|_|_|  _|    _|  _|_|_|_|    _|_|_|  _|    _|  _|_|_|_|  _|    _|  
                                                                                                    
                                                                                                                                                            
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
        "server": "smtp.163.com",
        "port": 465,
        "username": "maverickawa@163.com",
        "password": "ZDkg8yLUDTrBnV8j",
        "use_ssl": True
    },
    "email": {
        "to_address": "apple.yan@me.com",
        "from_address": "maverickawa@163.com",
        "subject": "公司的公网IP地址已经修改为{now_ip}"
    },
    "api_server": {
        "name": "pconline", # 默认API 感谢太平洋电脑网提供的API
        "url": "https://whois.pconline.com.cn/ipJson.jsp?ip=&json=true"
    },
    "check_interval_seconds": 600  # 单位为秒
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
                <p>当前时间: {datetime.now()}</p>
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