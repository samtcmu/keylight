#!/opt/local/bin/python3

import urllib.request
import json

KEYLIGHT_LEFT_URL = "http://key-light-left.local:9123/elgato/lights"
KEYLIGHT_RIGHT_URL = "http://key-light-right.local:9123/elgato/lights"
KEYLIGHT_MIN_TEMPERATURE = 143
KEYLIGHT_MAX_TEMPERATURE = 344

def main():
    ToggleKeyLights(KEYLIGHT_LEFT_URL)
    ToggleKeyLights(KEYLIGHT_RIGHT_URL)


def AdjustBrightness(increment, keylight_url=KEYLIGHT_LEFT_URL):
    keylight = GetKeyLightStatus();
    for light in keylight["lights"]:
        light["brightness"] = max(min(light["brightness"] + increment, 100), 0)
    SetKeyLightStatus(keylight);


def RotateTemperature(keylight_url=KEYLIGHT_LEFT_URL):
    keylight = GetKeyLightStatus();

    for i in range(KEYLIGHT_MIN_TEMPERATURE, KEYLIGHT_MAX_TEMPERATURE, 1):
        for light in keylight["lights"]:
            light["temperature"] = i
        SetKeyLightStatus(keylight);
        print(f"{i}: {GetKeyLightStatus()}")


def ToggleKeyLights(keylight_url=KEYLIGHT_LEFT_URL):
    # Get current status of keylight(s).
    keylight_status = GetKeyLightStatus(keylight_url);
    if ("numberOfLights" in keylight_status) and (keylight_status["numberOfLights"] <= 0):
        print("no keylight(s) found");
        return

    # Toggle keylight(s).
    for light in keylight_status["lights"]:
        light["on"] = (light["on"] + 1) % 2
    SetKeyLightStatus(keylight_status, keylight_url);


def GetKeyLightStatus(keylight_url=KEYLIGHT_LEFT_URL):
    # Get current KeyLight status:
    #   curl -X GET key-light.local:9123/elgato/lights
    return json.load(urllib.request.urlopen(keylight_url))


def SetKeyLightStatus(keylight_status, keylight_url=KEYLIGHT_LEFT_URL):
    # Set KeyLight status:
    #   curl -X PUT -H "Content-Type: application/json" \
    #        -d '{"Lights":[{"On":0,"Brightness": 20,"Temperature":300}]}'\
    #        key-light.local:9123/elgato/lights
    request = urllib.request.Request(url=keylight_url,
                                 data=bytes(json.dumps(keylight_status), encoding='utf8'),
                                 method='PUT')
    urllib.request.urlopen(request)
    


if __name__ == "__main__":
    main()
