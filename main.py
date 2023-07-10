from initialize import driver, remaining_tracks
from core import fetch_track_urls, download_tracks


def main():
    if remaining_tracks:
        print("\nGoing to download remaining tracks")
        track_urls = remaining_tracks
    else:
        print("\nGoing to fetch and download tracks")
        track_urls = fetch_track_urls()

    download_tracks(track_urls)


if __name__ == "__main__":
    try:
        main()
    except (Exception, KeyboardInterrupt) as err:
        if type(err) is KeyboardInterrupt:
            err = "Interrupted"
        print("\nError:", err)
        exit()
    finally:
        print("\nWait for the WebDriver to quit")
        driver.quit()
