from player import setup_options, run
from parser import parse, get_html

from flask import Flask, request
import asyncio
import json

app = Flask(__name__)
tasks = []

ALIVE_STATUS = 'y'

def clear_addr(addr):
    return addr.replace('/', '').replace(':', '').replace('?', '').replace('=', '').replace('&', '').replace(' ', '_').replace('.', '-')


def check_status(status):
    if status == ALIVE_STATUS:
        return False
    else:
        return True


@app.route('/show', methods=['POST'])
def show():
    print(request.json)
    for i in range(len(tasks)):
        tasks[i]['status'] = ''

    jdata = request.json
    html = get_html(parse(jdata['link']))
    fname = clear_addr(jdata['link'])

    with open(fname, 'w') as f:
        f.write(html)

    tasks.append({
        'name': fname,
        'status': ALIVE_STATUS
    })
    # await run_task()

    return json.dumps({'result': 'ok'}, indent=2)

async def run_task():
    task = tasks[0]
    driver = webdriver.Chrome('chromedriver', options=setup_options())
    await run(driver, task['name'], check_status, task['status'])

if __name__ == '__main__':
    app.run('0.0.0.0')
