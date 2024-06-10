# 用python原生库监听本机ipv6地址变化，使用stmp邮箱服务发送

import datetime
import smtplib
import socket
from email.header import Header
from email.mime.text import MIMEText
from email.utils import formataddr, parseaddr

from_addr = "srcxx@com" # smtp邮箱
password = "xxxxxxx"  # smtp服务的授权码
to_addr = "tarxxxx@com"
smtp_server = "smtp.com"


def getipv6():
    host_ipv6 = []
    ips = socket.getaddrinfo(socket.gethostname(), 80)
    for ip in ips:
        if ip[4][0].startswith("24"):
            # 2408 中国联通
            # 2409 中国移动
            # 240e 中国电信
            #        print(ip[4][0])
            host_ipv6.append(ip[4][0])
    return host_ipv6


def _format_addr(s):
    name, addr = parseaddr(s)
    return formataddr((Header(name, "utf-8").encode(), addr))


if __name__ == "__main__":
    ipv6_temp = getipv6()[0]  # 读取目前第一个ipv6地址
    with open("./ipv6_no.txt") as f:
        ipv6_no = f.readline()

    if ipv6_temp != ipv6_no:
        timestmp_str = datetime.datetime.now().strftime(format="%Y-%m-%d %H:%M:%S")

        with open("./ipv6_changes.log", mode="a") as log:
            log.write(
                f"{timestmp_str} chances from \n    {ipv6_no} \n to \n    {ipv6_temp}\n"
            )

        with open("./ipv6_no.txt", "w") as nf:
            nf.write(ipv6_temp)

        msg = MIMEText(
            f"{timestmp_str} chances from \n    {ipv6_no} \n to \n    {ipv6_temp}\n",
            "plain",
            "utf-8",
        )
        msg["From"] = _format_addr(
            "Python爱好者win10 <%s>" % from_addr
        )  # 发件人自定义头
        msg["To"] = _format_addr("管理员 <%s>" % to_addr)
        msg["Subject"] = Header("来自SMTP的问候……ipv6", "utf-8").encode()

        server = smtplib.SMTP(smtp_server, 25)
        server.set_debuglevel(1)
        server.login(from_addr, password)
        server.sendmail(from_addr, [to_addr], msg.as_string())
        server.quit()

        with open("./ipv6_changes.log", mode="a") as log:
            log.write(f"    sended already {to_addr}")
