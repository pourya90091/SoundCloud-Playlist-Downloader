from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from webdriver_manager.chrome import ChromeDriverManager
from pathlib import Path
from os import mkdir
from os.path import isdir
import pickle


BASE_DIR = Path(__file__).parent.resolve()
BASE_URL = "https://soundcloudmp3.org"
PLAYLISTS_DIR = f"{BASE_DIR}/playlists" 
TIMEOUT = 0.5

try:
    if not Path(f"{BASE_DIR}/.remaining_tracks.data").is_file():
        with open(f"{BASE_DIR}/.remaining_tracks.data", "wb") as file:
            pickle.dump(None, file)

    with open(f"{BASE_DIR}/.remaining_tracks.data", "rb") as file:
        remaining_tracks = pickle.load(file)

    if remaining_tracks:
        verification = input("\nDo you wanna to continue downloading the last playlist? (Y/n): ")

        if verification == "":
            verification = "yes"

        verifications = ["y", "Y", "yes", "YES", "Yes", "yea", "yeah"]
        if not verification in verifications:
            with open(f"{BASE_DIR}/.remaining_tracks.data", "wb") as file:
                pickle.dump(None, file)

            with open(f"{BASE_DIR}/.remaining_tracks.data", "rb") as file:
                remaining_tracks = pickle.load(file)

            playlist_url = input("Set playlist url (https://soundcloud.com/<username>/sets/<playlist-name>): ")

            with open(f"{BASE_DIR}/.last_playlist_url.data", "wb") as file:
                pickle.dump(playlist_url, file)
        else:
            if not Path(f"{BASE_DIR}/.last_playlist_url.data").is_file():
                raise Exception("\".last_playlist_url.data\" is missing")

            with open(f"{BASE_DIR}/.last_playlist_url.data", "rb") as file:
                playlist_url = pickle.load(file)
    else:
        playlist_url = input("Set playlist url (https://soundcloud.com/<username>/sets/<playlist-name>): ")

        with open(f"{BASE_DIR}/.last_playlist_url.data", "wb") as file:
            pickle.dump(playlist_url, file)

    time_out = input("Set timeout (by default = 0.5): ")
    
    if not isdir(PLAYLISTS_DIR):
        mkdir(PLAYLISTS_DIR)

    if not playlist_url:
        raise Exception("\"playlist url\" is required")

    if not time_out:
        pass
    else:
        TIMEOUT = float(time_out) 
except (Exception, KeyboardInterrupt) as err:
    if type(err) is KeyboardInterrupt:
        err = "Interrupted"
    print("\nError:", err)
    exit()
else:
    print("\nPreparing the WebDriver")

    service = Service(executable_path=ChromeDriverManager().install())

    options = Options()
    options.add_argument("--headless")
    options.add_argument("--window-size=1920, 1080")
    options.add_argument('--no-sandbox')
    options.add_argument('--disable-dev-shm-usage')
    options.add_argument("--disable-gpu")
    options.add_argument("--disable-extensions")
    options.add_argument("--dns-prefetch-disable")
    options.add_argument("--disk-cache-size=1")
    options.add_argument("--media-cache-size=1")
    options.add_experimental_option("excludeSwitches", ["enable-logging"])
    options.page_load_strategy = "normal"

    driver = webdriver.Chrome(service=service, options=options)
    driver.implicitly_wait(TIMEOUT)
