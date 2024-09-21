"""
@Author: kang.yang
@Date: 2023/11/16 17:50
"""
import kytest

from page.web_page import CommonPage


@kytest.story('登录模块')
class TestWebDemo(kytest.WebTC):
    def start(self):
        self.cp = CommonPage(self.dr)

    @kytest.title("登录")
    def test_login(self):
        self.cp.login()
        self.assert_url()
        self.shot('首页', delay=3)




