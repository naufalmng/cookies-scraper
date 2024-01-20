import json
from pprint import pprint

from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from decouple import config

'''
USAGE:
1. active project by 
'''


URL='https://booking.com/'
chrome_options = webdriver.ChromeOptions()  # Add options to chrome
chrome_options.add_experimental_option('detach', True)
chrome_options.add_argument('--disable-extensions')  # Disable extensions
chrome_options.add_argument('--no-sandbox')  # Bypass OS security model
chrome_options.add_argument('--disk-cache-size=0')  # Disable cache
chrome_options.add_argument('--blink-settings=imagesEnabled=false')  # Disable images
chrome_options.add_argument('user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36')
chrome_options.add_argument('--headless')

if __name__ == '__main__':
    driver = webdriver.Chrome(options=chrome_options)
    driver.get('https://account.booking.com/sign-in')
    WebDriverWait(driver,15).until(EC.element_to_be_clickable((By.XPATH,'//*[@id="username"]'))) # wait for email field to be clickable

    driver.find_element(By.XPATH, '//*[@id="username"]').send_keys(config('EMAIL')) # type email

    driver.find_element(
        By.XPATH,
        '//*[@id="root"]/div/div/div/div[2]/div[1]/div/div/div/div/div/div/form/div[3]/button'
    ).click() # click on next button

    WebDriverWait(driver,15).until(EC.element_to_be_clickable((By.XPATH,'//*[@id="password"]'))) # wait for password field to be clickable
    driver.find_element(By.XPATH, '//*[@id="password"]').send_keys(config('PASSWORD')) # type password

    try:
        driver.find_element(
            By.XPATH,
            '//*[@id="root"]/div/div/div/div[2]/div[1]/div/div/div/div/div/div/form/div[2]/button'
        ).click()  # click on login button
        WebDriverWait(driver, 15).until(
            EC.visibility_of_element_located((By.XPATH, '//*[@id="b2indexPage"]')))  # wait for home page to be loaded

        cookies = driver.get_cookies()
        with open('cookies.json', 'w') as file:
            json.dump(cookies, file)
            # print dumped cookies
            for cookie in cookies:
                pprint(cookie)
            print('Cookies have been saved..')
    except Exception as e:
        print('Failed to save cookies..')
        print(e)
        exit()