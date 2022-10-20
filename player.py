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


def setup_options():
    options = webdriver.ChromeOptions()
    # options.add_argument('headless')
    options.add_argument('window-size=1920x900')
    # options.add_experimental_option("detach", True)
    options.add_argument("start-maximized")
    options.add_argument("disable-extensions")
    options.add_experimental_option("excludeSwitches", ["enable-automation"])
    options.add_experimental_option('useAutomationExtension', True)
    return options


async def run(driver, html_name: str, kill_predicate, kill_arg):
    try:
        # driver = webdriver.Firefox()
        async def __get(driver):
            # get current dir
            cwd = os.getcwd()
            driver.get(f'file://{cwd}/{html_name}')

        get_handle = __get(driver)
        print(driver)
        await get_handle
        # How to fix this?
        driver.find_element(By.ID, 'player').click()

        while not kill_predicate(kill_arg):
            await asyncio.sleep(5)

        print('Kill!')
        await asyncio.sleep(1)

    except Exception as exc:
        print('Something is wrong', exc)
        raise exc
    finally:
        driver.quit()


if __name__ == "__main__":
    driver = webdriver.Chrome('chromedriver', options=setup_options())
    try:
        asyncio.run(run(driver, 'parser_example.html', lambda _: False))
    except Exception as exc:
        print('Kill browser window, reason:', exc)
        driver.quit()
