import json
import requests
import smtplib
import time
import logging
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from datetime import datetime
import ssl
import os
import subprocess
from colorama import Fore, Style, init
from typing import Optional, Dict, Any

# 你正在使用的版本为 : Open 1.5
# 开源地址 : https://github.com/Mapleawaa/Check-IP-And-Push-Notifications
# 如果个人使用 请勿删除本段注释
# 如遇到问题 请创建issue

# 配置日志记录
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler('ip_monitor.log', encoding='utf-8'),
        logging.StreamHandler()
    ]
)
logger = logging.getLogger(__name__)

# logo
LOGO = """
HOME-IP-CHECKER
"""

class ConfigManager:
    def __init__(self, config_file: str = "config.json"):
        self.config_file = config_file
        self.config = self._load_config()
        self.api_servers = self._load_api_servers()

    def _load_config(self) -> Dict[str, Any]:
        try:
            with open(self.config_file, 'r', encoding='utf-8') as f:
                return json.load(f)
        except FileNotFoundError:
            logger.error(Fore.RED + f"配置文件 {self.config_file} 未找到 (｡•́︿•̀｡)")
            return self._get_default_config()

    def _load_api_servers(self) -> Dict[str, Any]:
        try:
            with open('request_server.json', 'r', encoding='utf-8') as f:
                return json.load(f)
        except FileNotFoundError:
            logger.error(Fore.RED + "API服务器配置文件未找到 (｡•́︿•̀｡)")
            return {}

    def _get_default_config(self) -> Dict[str, Any]:
        return {
            "smtp": {
                "server": "smtp.163.com",
                "port": 465,
                "username": "",
                "password": "",
                "use_ssl": True
            },
            "email": {
                "to_address": "",
                "from_address": "",
                "subject": "公司的公网IP地址已经修改为{now_ip}"
            },
            "check_interval_seconds": 300
        }

class NetworkMonitor:
    def __init__(self, config_manager: ConfigManager):
        self.config_manager = config_manager
        self.last_ip = self._load_last_ip()
        self.current_api_index = 0

    def _load_last_ip(self) -> Optional[str]:
        try:
            with open("last_ip.txt", "r") as f:
                return f.read().strip()
        except FileNotFoundError:
            return None

    def _save_last_ip(self, ip: str) -> None:
        with open("last_ip.txt", "w") as f:
            f.write(ip)
        logger.info(Fore.CYAN + f"历史IP信息保存成功 ((꜆꜄꜆ ˙꒳˙)꜆꜄꜆: {ip}")

    def get_public_ip(self) -> Optional[str]:
        api_servers = list(self.config_manager.api_servers.values())
        attempts = len(api_servers)

        for _ in range(attempts):
            api_server = api_servers[self.current_api_index]
            try:
                response = requests.get(
                    api_server["url"], 
                    headers=api_server["header"][0],
                    timeout=5
                )
                response.raise_for_status()
                data = response.json()
                ip = data.get("ip")
                
                if ip:
                    logger.info(Fore.GREEN + f"获取到了现在的IP地址 (=^-ω-^=): {ip}")
                    return ip
                
            except Exception as e:
                logger.warning(Fore.YELLOW + f"API {self.current_api_index + 1} 调用失败: {str(e)}")
            
            self.current_api_index = (self.current_api_index + 1) % len(api_servers)

        logger.error(Fore.RED + "所有API服务器均无法访问 (╥_╥)")
        return None

    def check_network_status(self) -> Dict[str, bool]:
        return {
            "internet": self._check_internet_connection(),
            "intranet": self._check_intranet_connection()
        }

    def _check_internet_connection(self) -> bool:
        try:
            response = subprocess.check_output(["ping", "114.114.114.114"], timeout=5)
            return "TTL" in response.decode()
        except Exception as e:
            logger.error(Fore.RED + f"外网连接失败 (｡•́︿•̀｡): {e}")
            return False

    def _check_intranet_connection(self) -> bool:
        try:
            response = subprocess.check_output(["ping", "172.16.1.1"], timeout=5)
            return "TTL" in response.decode()
        except Exception as e:
            logger.error(Fore.RED + f"内网连接失败 (｡•́︿•̀｡): {e}")
            return False

class EmailNotifier:
    def __init__(self, config_manager: ConfigManager):
        self.config = config_manager.config

    def send_ip_change_notification(self, previous_ip: str, current_ip: str) -> bool:
        return self._send_email(
            "IP地址变更通知",
            self._get_ip_change_template(previous_ip, current_ip)
        )

    def send_warning_notification(self, error_message: str, network_status: Dict[str, bool]) -> bool:
        return self._send_email(
            "网络连接警告",
            self._get_warning_template(error_message, network_status)
        )

    def _send_email(self, subject: str, body: str) -> bool:
        smtp_config = self.config["smtp"]
        email_config = self.config["email"]

        message = MIMEMultipart()
        message["From"] = email_config["from_address"]
        message["To"] = email_config["to_address"]
        message["Subject"] = subject
        message.attach(MIMEText(body, "html"))

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
            return True
        except Exception as e:
            logger.error(Fore.RED + f"邮件发送失败 (′゜ω。‵): {e}")
            return False

    def _get_ip_change_template(self, previous_ip: str, current_ip: str) -> str:
        # 这里放入之前的IP变更邮件模板
        return f"""
        <html>
            <!-- 原有的IP变更邮件模板 -->
        </html>
        """

    def _get_warning_template(self, error_message: str, network_status: Dict[str, bool]) -> str:
        # 这里放入之前的警告邮件模板
        return f"""
        <html>
            <!-- 原有的警告邮件模板 -->
        </html>
        """

class IPMonitorService:
    def __init__(self):
        self.config_manager = ConfigManager()
        self.network_monitor = NetworkMonitor(self.config_manager)
        self.email_notifier = EmailNotifier(self.config_manager)

    def run(self):
        try:
            while True:
                self._check_and_update()
                interval = self.config_manager.config["check_interval_seconds"]
                logger.info(Fore.BLUE + f"等待 {interval} 秒后再次检查... ( ˊ̱˂˃ˋ̱ )")
                time.sleep(interval)
        except KeyboardInterrupt:
            logger.info(Fore.YELLOW + "程序已手动停止 /ᐠ .ᆺ. ᐟ\ﾉ")

    def _check_and_update(self):
        network_status = self.network_monitor.check_network_status()
        
        if not any(network_status.values()):
            self.email_notifier.send_warning_notification(
                "网络连接完全中断",
                network_status
            )
            return

        current_ip = self.network_monitor.get_public_ip()
        if current_ip is None:
            return

        if current_ip != self.network_monitor.last_ip:
            if self.email_notifier.send_ip_change_notification(
                self.network_monitor.last_ip,
                current_ip
            ):
                self.network_monitor._save_last_ip(current_ip)
                self.network_monitor.last_ip = current_ip

def main():
    HOMELOGO = f"""
                                                                                                        
    _|_|_|  _|_|_|                  _|_|_|  _|    _|  _|_|_|_|    _|_|_|  _|    _|  _|_|_|_|  _|_|_|    
    _|    _|    _|              _|        _|    _|  _|        _|        _|  _|    _|        _|    _|  
    _|    _|_|_|    _|_|_|_|_|  _|        _|_|_|_|  _|_|_|    _|        _|_|      _|_|_|    _|_|_|    
    _|    _|                    _|        _|    _|  _|        _|        _|  _|    _|        _|    _|  
    _|_|_|  _|                      _|_|_|  _|    _|  _|_|_|_|    _|_|_|  _|    _|  _|_|_|_|  _|    _|  
                                                                                                        
    """
    init(autoreset=True)
    print(Fore.GREEN + HOMELOGO )  # LOGO常量需要定义
    
    service = IPMonitorService()
    service.run()

if __name__ == "__main__":
    main()
