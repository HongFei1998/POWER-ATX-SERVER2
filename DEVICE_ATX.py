import os
import time
import subprocess
import requests
import json

MXBC_ATX_DIR = os.path.dirname(os.path.realpath(__file__))
atx_log = open(f'{MXBC_ATX_DIR}/atx.log', 'a')


def start_rethinkdb():
    os.chdir(f'{MXBC_ATX_DIR}/rethinkdb/rethinkdb-v2.4.0-srh-win-1-Release_x64')
    cmd = f'rethinkdb.exe -d /data/ --http-port 8088'
    this_P = subprocess.Popen(cmd, shell=True, stdout=atx_log, stderr=atx_log)
    time.sleep(5)
    # print(this_P.pid)
    pass


def start_atx_server2(port):
    os.chdir(f'{MXBC_ATX_DIR}/atxserver2-master')
    cmd = f'python main.py --port {port} -d'
    this_P = subprocess.Popen(cmd, shell=True, stdout=atx_log, stderr=atx_log)
    time.sleep(5)
    # print(this_P.pid)
    pass


def start_atx_server2_android_provider(port):
    os.chdir(f'{MXBC_ATX_DIR}/atxserver2-android-provider-master')
    cmd = f'python main.py --server localhost:{port} --allow-remote'
    this_P = subprocess.Popen(cmd, shell=True, stdout=atx_log, stderr=atx_log)
    time.sleep(5)
    # print(this_P.pid)
    pass


def start_atx_server2_ios_provider(port):
    os.chdir(f'{MXBC_ATX_DIR}/atxserver2-ios-provider-master')

    # 手动启用wda
    cmd = f'python main.py -s "http://localhost:{port}" --manually-start-wda'

    # 自动启用wda
    # cmd = f'python main.py -s "http://localhost:{port}" --use-tidevice --wda-bundle-pattern "*WebDriverAgent*"'

    this_P = subprocess.Popen(cmd, shell=True, stdout=atx_log, stderr=atx_log)
    time.sleep(5)
    # print(this_P.pid)
    pass


def start_device_atx_server(port=4001):
    start_rethinkdb()
    start_atx_server2(port)
    start_atx_server2_android_provider(port)
    start_atx_server2_ios_provider(port)
    print(f'ATX服务启动完成，地址：http://127.0.0.1:{port}')


if __name__ == '__main__':
    start_device_atx_server(4001)
    while True:
        pass
