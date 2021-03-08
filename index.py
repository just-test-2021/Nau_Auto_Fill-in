from Tools.scripts.serve import app
from selenium import webdriver
from selenium.webdriver import ActionChains
from selenium.webdriver.support.select import Select
from selenium.webdriver.common.keys import Keys
import time
import smtplib
from email.mime.text import MIMEText
from email.header import Header
import time
from selenium import webdriver
from PIL import Image
import pytesseract
import datetime


if __name__ == '__main__':
    # 这里改成你的统一认证用户名和密码
    user_name = '你的账号'
    pwd = '你的密码'

    # 加上这两句话不打开浏览器
    option = webdriver.ChromeOptions()
    # option.add_argument('headless') # 设置option
    # 用浏览器打开打卡的网址
    browser = webdriver.Chrome(options=option)
    # browser.get("http://yq.nauvpn.cn/student/perday")
    browser.get("http://yq.nauvpn.cn")
    # 第一次打开

    no_xia = browser.find_element_by_css_selector("label.yd-checkbox")
    ActionChains(browser).move_to_element(no_xia).click(no_xia).perform()

    ty = browser.find_element_by_css_selector('label.yd-checkbox.check-text')
    ActionChains(browser).move_to_element(ty).click(ty).perform()

    time.sleep(10)

    kstb = browser.find_element_by_css_selector('button.yd-btn-block.yd-btn-primary')
    ActionChains(browser).move_to_element(kstb).click(kstb).perform()
    time.sleep(3)
    # 输用户名和密码
    user_name_input = browser.find_element_by_css_selector("[type=text][placeholder=请输入学号]").click()
    user_name_input = browser.find_element_by_css_selector("[type=text][placeholder=请输入学号]").send_keys(user_name)
    user_pwd_input = browser.find_element_by_css_selector("[type=password][placeholder=请输入密码]").click()
    user_pwd_input = browser.find_element_by_css_selector("[type=password][placeholder=请输入密码]").send_keys(pwd)

    # 点击记住密码
    jzmm = browser.find_element_by_css_selector('label.yd-checkbox')
    ActionChains(browser).move_to_element(jzmm).click(jzmm).perform()

    # 识别验证码
    browser.save_screenshot("")
    imgeLement = browser.find_element_by_xpath('//*[@id="app"]/div/div[1]/div[2]/div/div[3]/div[2]/div/svg')  # 定位验证码
    location = imgeLement.location  # 获取验证码x,y轴坐标
    size = imgeLement.size  # 获取验证码的长宽
    rangle = (int(location["x"] * 2), int(location["y"] * 2), int(location["x"] * 2 + size["width"] * 2),
              int(location["y"] * 2 + size["height"] * 2))  # 写成需要截取的位置坐标

    i = Image.open("imgeLement")  # 打开截图
    frame4 = i.crop(rangle)  # 使用Image的crop函数，从截图中再次截取需要的区域
    frame4.save("C:\Users\Jonah\Desktop\yanzhengma")  # 图片保存路径
    qq = Image.open("C:\Users\Jonah\Desktop\yanzhengma")  # 图片的保存路径

    text = pytesseract.image_to_string(qq).strip()  # 使用image_to_string识别验证码
    print(text)  # 打印出验证码

    # login_button = browser.find_element_by_xpatch('//span[text()="登录"]')
    login_button = browser.find_element_by_css_selector('button.btn-login.mgt.yd-btn-block.yd-btn-primary')
    ActionChains(browser).move_to_element(login_button).click(login_button).perform()
    print('登录')

    # browser.get("http://yq.nauvpn.cn/student/perday")

# 个人健康状况 正常
# zc = browser.find_element_by_id("sui-multiselect-jkzk32")
# ActionChains(browser).move_to_element(zc).click(zc).perform()

# 现人员位置 在其他地区
# wz = //*[@id="app"]/div/div[1]/div[14]/div/div[2]/div/input("sui-select-xrywz9")
# ActionChains(browser).move_to_element(wz).click(wz).perform()

# 具体位置 102
# jtwz = browser.find_element_by_css_selector("[type=text][name=jtdz]")
# jtwz.send_keys("102")

# 医学隔离中 否
# gl = browser.find_element_by_xpath("//*[@id='sui-select-sfyxglz11']")
# ActionChains(browser).move_to_element(gl).click(gl).perform()

# 体温
tw = browser.find_element_by_css_selector("[type=text][placeholder=请输入今日体温]")
tw.send_keys("36.5")
# 提交
tpost = browser.find_element_by_xpatch('//span[text()="提交"]')
ActionChains(browser).move_to_element(tpost).click(tpost).perform()

time.sleep(10)
# 关闭浏览器
browser.quit()

# 发送给个人邮箱
# 用于构建邮件头
# 发信方的信息：发信邮箱，QQ 邮箱授权码
from_addr = '1847541219@qq.com'
# 进入qq邮箱->设置->账户->找到stmp服务，点击开启。验证后会给你一个授权码，直接复制，填入下方即可
password = 'tdjuhndujfhocehc'

# 收信方邮箱
to_addr = '3205038881@qq.com'

# 发信服务器
smtp_server = 'smtp.qq.com'

# 邮箱正文内容，第一个参数为内容（正文部分），第二个参数为格式(plain 为纯文本)，第三个参数为编码
msg = MIMEText('今日已经填报好健康信息', 'plain', 'utf-8')

# 邮件头信息
msg['From'] = Header(from_addr)
msg['To'] = Header(to_addr)
msg['Subject'] = Header('每日疫情填报情况')

# 开启发信服务，这里使用的是加密传输
server = smtplib.SMTP_SSL(smtp_server)
server.connect(smtp_server, 465)
# 登录发信邮箱
server.login(from_addr, password)
# 发送邮件
server.sendmail(from_addr, to_addr, msg.as_string())
# 关闭服务器
server.quit()

