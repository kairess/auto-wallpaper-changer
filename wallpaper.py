import requests
import time, ctypes, os, random, platform

# https://www.pexels.com/api/new/
API_KEY = 'YOUR_API_KEY_HERE'
QUERY = 'cat'
INTERVAL = 60

os.makedirs('wallpapers', exist_ok=True)
system_name = platform.system().lower()

while True:
    # get random wallpaper
    page = random.randint(1, 100)
    url = f'https://api.pexels.com/v1/search?per_page=1&page={page}&query={QUERY}'
    res = requests.get(url, headers={'Authorization': API_KEY})

    if res.status_code != 200:
        print('[!] Error fetch image')
        time.sleep(INTERVAL)
        continue

    # download the wallpaper
    img_url = res.json().get('photos')[0]['src']['original']
    img = requests.get(img_url)

    img_path = os.path.join(os.getcwd(), 'wallpapers', f'{time.time()}.jpg')
    with open(img_path, 'wb') as f:
        f.write(img.content)

    # set the wallpaper
    if system_name == 'linux':
        os.system(f'gsettings set org.gnome.desktop.background picture-uri file:{img_path}')
    elif system_name == 'windows':
        ctypes.windll.user32.SystemParametersInfoW(20, 0, img_path, 0)
    elif system_name == 'darwin':
        import applescript
        applescript.tell.app('Finder', f'set desktop picture to POSIX file "{img_path}"')
    else:
        print('[!] Unknown system')

    time.sleep(INTERVAL)
