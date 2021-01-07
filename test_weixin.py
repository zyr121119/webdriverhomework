import json
from time import sleep
import pytest
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions
from selenium.webdriver.support.wait import WebDriverWait


class TestChrome:
    def setup_class(self):
        chrome_args=webdriver.ChromeOptions()
        chrome_args.debugger_address = "127.0.0.1:9222"
        self.driver=webdriver.Chrome(options=chrome_args)
        self.driver.maximize_window()
        sleep(10)
    def teardown_class(self):
        self.driver.quit()

    @pytest.mark.run(order=1)
    def test_cookie(self):
        try:
            self.driver.get("https://work.weixin.qq.com/")
            with open("cookie.json","r")as f:
                cookies = json.load(f)
            for cookie in cookies:
                self.driver.add_cookie(cookie)
            self.driver.get("https://work.weixin.qq.com/wework_admin/frame#index")
            text=self.driver.find_element(By.XPATH,"//*[@id='menu_index']").text
            if text=="首页":
                print("cookie 正确")
            else:
                raise Exception
        except Exception as e:
            self.driver.get("https://work.weixin.qq.com/")
            self.driver.find_element_by_class_name("index_top_operation_loginBtn").click()
            sleep(10)
            print("cookie 不正确,请扫码登录")

            #WebDriverWait(self.driver,10).until(expected_conditions.visibility_of_element_located(By.XPATH,"//*[@id=menu_index]"))
            cookies=self.driver.get_cookies()
            with open("cookie.json","w") as f:
                json.dump(cookies,f)

    @pytest.mark.run(order=2)
    def test_chrome(self):
        self.driver.find_element(By.XPATH,"//*[@id='menu_customer']").click()
        sleep(15)
