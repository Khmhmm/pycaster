from selenium import webdriver
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.expected_conditions import (presence_of_element_located)
from selenium.webdriver.support.wait import WebDriverWait
import os
import signal
import time
import asyncio

options = webdriver.ChromeOptions()
# options.add_argument('headless')
options.add_argument('window-size=1920x900')
# options.add_experimental_option("detach", True)
options.add_argument("start-maximized")
options.add_argument("disable-extensions")
options.add_experimental_option("excludeSwitches", ["enable-automation"])
options.add_experimental_option('useAutomationExtension', True)

async def run(options):
    try:
        global driver
        driver = webdriver.Chrome('chromedriver', options=options)
        # driver = webdriver.Firefox()
        async def __get(driver):
            driver.get("file:///media/matvey/6bf4fb31-7931-4e05-80ce-fca506bac845/git/Projects/caster/example.html")

        get_handle = __get(driver)
        print(driver)
        await get_handle
        # How to fix this?
        driver.find_element(By.ID, 'ytplayer').click()

        await asyncio.sleep(5)
        print('Kill!')
        await asyncio.sleep(1)
        driver.quit()

    except Exception as exc:
        print('Something is wrong', exc)

asyncio.run(run(options))

#print(driver.service.process.pid)
#print("Woops I'm going to make something harmful")
#time.sleep(2)
#print('Now!')
#os.killpg(driver.service.process.pid, signal.SIGKILL)
