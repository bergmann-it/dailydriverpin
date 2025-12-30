from selenium import webdriver
from selenium.webdriver.firefox.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.common.action_chains import ActionChains
import pyotp
import time

def update_amazon_pin(mail,pwd,totp_secret,pin):
    amazon_totp = pyotp.TOTP(totp_secret)

    options = Options()
    options.add_argument('-headless')
    service = webdriver.FirefoxService(executable_path='/usr/local/bin/geckodriver')
    driver = webdriver.Firefox(options=options,service=service)

#call page
    driver.get("https://www.amazon.de/a/addresses?ref_=ya_d_c_addr")

#first enter mail Adress
    mailadress_input = driver.find_element(By.CSS_SELECTOR, "input[autocomplete=\"username\"]")
    mailadress_input.send_keys(mail)
    submit = driver.find_element(By.CSS_SELECTOR, "input[type=\"submit\"]")
    submit.click()

#then enter password
    pwd_input = driver.find_element(By.CSS_SELECTOR, "input[autocomplete=\"current-password\"]")
    pwd_input.send_keys(pwd)
    submit = driver.find_element(By.CSS_SELECTOR, "input[type=\"submit\"]")
    submit.click()

#then enter OTP
    otp_input = driver.find_element(By.NAME, "otpCode")
    otp_input.send_keys(amazon_totp.now())
    submit = driver.find_element(By.CSS_SELECTOR, "input[type=\"submit\"]")
    submit.click()

#open the modal
    time.sleep(1)
    modal_link = driver.find_element(By.LINK_TEXT, "Lieferanweisungen hinzufügen")
    modal_link.click()
    time.sleep(1)

#then enter new code
    doorotp_input = driver.find_element(By.NAME, "securityCode")
    doorotp_input.clear()
    doorotp_input.send_keys(pin)
    submit = driver.find_element(By.CSS_SELECTOR, "#cdp-save-button input")
    submit.click()

    driver.quit()


