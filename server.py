from player import setup_driver, run_player
from parser import parse, get_html

from selenium.webdriver.common.by import By
from multiprocessing import Process, Pool
from flask import Flask, request
from time import sleep
import asyncio
import json
import os

app = Flask(__name__)
task = None
task_handler = None
# makes mutable
driver = [0]
ALIVE_STATUS = 'y'

def clear_addr(addr):
    return addr.replace('/', '').replace(':', '').replace('?', '').replace('=', '').replace('&', '').replace(' ', '_').replace('.', '-')


def check_status(status):
    if status == ALIVE_STATUS:
        return False
    else:
        return True


@app.route('/show', methods=['POST'])
async def show():
    global task_handler
    global task
    global driver
    if isinstance(task_handler, Process) and isinstance(task, dict):
        driver[0].quit()
        task_handler.terminate()
        os.remove(task['name'])

    jdata = request.json
    html = get_html(parse(jdata['link']))
    fname = clear_addr(jdata['link']) + '.html'

    with open(fname, 'w') as f:
        f.write(html)

    driver[0] = setup_driver()
    task = {
        'name': fname,
        # 'status': ALIVE_STATUS,
    }
    task_handler = Process(target=task_handle)
    task_handler.start()

    return json.dumps({'result': 'ok'}, indent=2)


@app.route('/pause', methods=['GET', 'POST'])
async def pause():
    global driver
    global task_handler
    if isinstance(task_handler, Process):
        driver[0].find_element(By.ID, 'player').click()


def run():
    app.run('0.0.0.0')


def task_handle():
    global task
    try:
        asyncio.run(run_player(driver[0], task['name']))
    except Exception as exc:
        driver[0].quit()


def daemon():
    # while True:
    #     sleep(10)
    return 0


if __name__ == '__main__':
    p1 = Process(target=run)
    p2 = Process(target=daemon)

    p1.start()
    p2.start()
    p1.join()


    
