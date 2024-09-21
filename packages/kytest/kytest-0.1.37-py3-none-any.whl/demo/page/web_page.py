"""
@Author: kang.yang
@Date: 2024/9/14 09:48
"""
from kytest import Page, WebElem
from data.user_data import USERNAME, PASSWORD


class IndexPage(Page):
    """首页"""
    url = "https://www-test.qizhidao.com/"
    loginBtn = WebElem(xpath='(//div[text()="登录/注册"])[1]')
    patentText = WebElem(xpath='//*[text()="查专利"]')


class LoginPage(Page):
    """登录页"""
    pwdTab = WebElem(xpath='//*[text()="密码登录"]')
    userInput = WebElem(xpath='//input[@placeholder="请输入手机号码"]')
    pwdInput = WebElem(xpath='//input[@placeholder="请输入密码"]')
    accept = WebElem(css=".agreeCheckbox .el-checkbox__inner")
    loginBtn = WebElem(xpath='//*[text()="立即登录"]')
    firstItem = WebElem(xpath="(//img[@class='right-icon'])[1]")


# 公共方法放在这个公共方法中
class CommonPage:
    """登录模块公共方法"""

    def __init__(self, driver):
        self.ip = IndexPage(driver)
        self.lp = LoginPage(driver)

    def login(self, username=USERNAME, password=PASSWORD):
        """从首页进行登录"""
        self.ip.open()
        self.ip.sleep(5)
        self.ip.loginBtn.click()
        self.ip.sleep(5)
        self.lp.pwdTab.click()
        self.lp.userInput.input(username)
        self.lp.pwdInput.input(password)
        self.lp.accept.click()
        self.lp.loginBtn.click()
        self.lp.firstItem.click()

