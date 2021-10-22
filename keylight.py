#!/opt/local/bin/python3

import urllib.request
import json

def main():
    KEYLIGHT_URL = "http://key-light.local:9123/elgato/lights"

    # Get current status of keylight(s).
    keylight = json.load(urllib.request.urlopen(KEYLIGHT_URL))
    if ("numberOfLights" in keylight) and (keylight["numberOfLights"] <= 0):
        print("no keylight(s) found");
        return

    # Toggle keylight(s).
    for light in keylight["lights"]:
        light["on"] = (light["on"] + 1) % 2
    request = urllib.request.Request(url=KEYLIGHT_URL,
                                 data=bytes(json.dumps(keylight), encoding='utf8'),
                                 method='PUT')
    urllib.request.urlopen(request)


if __name__ == "__main__":
    main()
