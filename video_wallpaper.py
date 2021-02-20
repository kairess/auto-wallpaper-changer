import cv2
import applescript
import requests
import time, ctypes, os, platform
from glob import glob

INTERVAL = 0.001

video_filename = 'The City Under The Cherry Tree.mp4'
video_path = os.path.join('videos', video_filename)
video_frames_path = os.path.join('videos', os.path.splitext(video_filename)[0])

if not os.path.exists(video_frames_path):
    print('Split video into frames...')

    os.makedirs(video_frames_path, exist_ok=True)

    cap = cv2.VideoCapture(video_path)

    i = 0
    while cap.isOpened():
        ret, img = cap.read()
        if not ret:
            break

        cv2.imwrite(os.path.join(video_frames_path, f'{str(i).zfill(5)}.jpg'), img)
        i += 1

print('Start!')

system_name = platform.system().lower()

img_list = sorted(glob(os.path.join(video_frames_path, '*.jpg')))

i = 0
while True:
    img_path = os.path.join(os.getcwd(), video_frames_path, f'{str(i % len(img_list)).zfill(5)}.jpg')

    if system_name == 'linux':
        os.system(f'gsettings set org.gnome.desktop.background picture-uri file:{img_path}')
    elif system_name == 'windows':
        ctypes.windll.user32.SystemParametersInfoW(20, 0, img_path, 0)
    elif system_name == 'darwin':
        applescript.tell.app('Finder', f'''ignoring application responses
        set desktop picture to POSIX file "{img_path}"
        end ignoring''')
        # applescript.tell.app('System Events', f'''ignoring application responses
        # tell current desktop to set picture to "{img_path}"
        # end ignoring''')
        # applescript.run('do shell script "killall System\\ Events"')
    else:
        print('[!] Unknown system')

    time.sleep(INTERVAL)
    i += 1
