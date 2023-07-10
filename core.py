from initialize import driver, playlist_url, TIMEOUT, BASE_DIR, BASE_URL, PLAYLISTS_DIR
import requests as req
import time
import re
from os import mkdir
from os.path import isdir
import pickle


track_list = "//ul[contains(@class, 'trackList__list')]"
playlist_name = re.findall(r"^https://soundcloud.com/.+/sets/(.+)$", playlist_url)[0]


def get_tracks() -> list:
    tracks = driver.find_elements("xpath", f"{track_list}/li")
    return tracks


def scroll_down() -> None:
    try:
        driver.execute_script(f"document.evaluate(\"{track_list}\", document, null, XPathResult.FIRST_ORDERED_NODE_TYPE, null).singleNodeValue.scrollIntoView(false);")
    except:
        raise Exception("The track list is not loaded")


def download_tracks(track_urls) -> None:
    def download_file(url, track_url):
        local_filename = track_url.split('/')[-1]
        with req.get(url, stream=True) as r:
            r.raise_for_status()

            if not isdir(f"{PLAYLISTS_DIR}/{playlist_name}"):
                mkdir(f"{PLAYLISTS_DIR}/{playlist_name}")

            with open(f"{PLAYLISTS_DIR}/{playlist_name}/{local_filename}.mp3", "wb") as f:
                for chunk in r.iter_content(chunk_size=8192): 
                    f.write(chunk)


    for track_url in track_urls:
        driver.get(BASE_URL)

        input = driver.find_element("xpath", "//input[@name='url']")
        input.send_keys(track_url)

        submit_button = driver.find_element("xpath", "//button[@name='submit']")
        submit_button.click()

        while True:
            try: 
                driver.find_element("xpath", "//div[not(@class='hidden')]/h4[text()='Finished, click here to download your MP3!']")
                btn_success = driver.find_element("xpath", "//a[contains(@class, 'btn-success')]")
            except:
               time.sleep(TIMEOUT)
               continue
            else:
                url = btn_success.get_attribute("href")
                download_file(url, track_url)

                downloaded_track = track_urls.pop(track_urls.index(track_url))
                print(f"Downloaded {downloaded_track}")

                with open(f"{BASE_DIR}/.remaining_tracks.data", "wb") as file:
                    pickle.dump(track_urls, file)

                break


def fetch_track_urls() -> list[str]:
    driver.get(playlist_url)

    while True:
        tracks = get_tracks()

        scroll_down()

        time.sleep(TIMEOUT)

        new_tracks = get_tracks()

        if len(tracks) == len(new_tracks):
            track_urls = []
            for track in tracks:
                try:
                    track_url = track.find_element("xpath", "./div/div[contains(@class, 'trackItem__content')]/a[contains(@class, 'sc-link-primary')]").get_attribute("href")
                    track_url = track_url.split('?')[0]
                    track_urls.append(track_url)
                except:
                    continue
            else:
                with open(f"{BASE_DIR}/.remaining_tracks.data", "wb") as file:
                    pickle.dump(track_urls, file)
                return track_urls
