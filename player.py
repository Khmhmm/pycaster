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


def setup_chromedriver():
    options = webdriver.ChromeOptions()
    # options.add_argument('headless')
    options.add_argument('window-size=1920x900')
    # options.add_experimental_option("detach", True)
    options.add_argument("start-maximized")
    options.add_argument("disable-extensions")
    options.add_experimental_option("excludeSwitches", ["enable-automation"])
    options.add_experimental_option('useAutomationExtension', True)
    driver = webdriver.Chrome('chromedriver', options=options)
    return driver


def setup_geckodriver():
    options = webdriver.FirefoxOptions()
    options.set_preference('network.http.tls-handshake-timeout', 1)
    driver = webdriver.Firefox(options=options)
    driver.fullscreen_window()
    return driver


def setup_driver():
    # driver = setup_chromedriver()    
    driver = setup_geckodriver()
    return driver


async def run_player(driver, html_name: str):
    try:
        # driver = webdriver.Firefox()
        async def __get(driver):
            # get current dir
            cwd = os.getcwd()
            driver.get(f'file://{cwd}/{html_name}')

        get_handle = __get(driver)
        await get_handle
        await asyncio.sleep(1)
        # How to fix this?
        driver.find_element(By.ID, 'player').click()
        
        while True:
            await asyncio.sleep(1)

        # print('Kill!')
        # await asyncio.sleep(1)

    except Exception as exc:
        print('Something is wrong', exc)
        raise exc
    finally:
        driver.quit()


if __name__ == "__main__":
    driver = setup_driver()
    try:
        asyncio.run(run_player(driver, 'example.html'))
    except Exception as exc:
        print('Kill browser window, reason:', exc)
        driver.quit()
