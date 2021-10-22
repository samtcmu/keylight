#!/opt/local/bin/python3

import urllib.request
import json

KEYLIGHT_URL = "http://key-light.local:9123/elgato/lights"
KEYLIGHT_MIN_TEMPERATURE = 143
KEYLIGHT_MAX_TEMPERATURE = 344

def main():
    ToggleKeyLights()


def RotateTemperature():
    keylight = GetKeyLightStatus();

    for i in range(KEYLIGHT_MIN_TEMPERATURE, KEYLIGHT_MAX_TEMPERATURE, 1):
        for light in keylight["lights"]:
            light["temperature"] = i
        SetKeyLightStatus(keylight);
        print(f"{i}: {GetKeyLightStatus()}")
    


def ToggleKeyLights():
    # Get current status of keylight(s).
    keylight = GetKeyLightStatus();
    if ("numberOfLights" in keylight) and (keylight["numberOfLights"] <= 0):
        print("no keylight(s) found");
        return

    # Toggle keylight(s).
    for light in keylight["lights"]:
        light["on"] = (light["on"] + 1) % 2
    SetKeyLightStatus(keylight);


def GetKeyLightStatus():
    # Get current KeyLight status:
    #   curl -X GET key-light.local:9123/elgato/lights
    return json.load(urllib.request.urlopen(KEYLIGHT_URL))


def SetKeyLightStatus(keylight):
    # Set KeyLight status:
    #   curl -X PUT -H "Content-Type: application/json" \
    #        -d '{"Lights":[{"On":0,"Brightness": 20,"Temperature":300}]}'\
    #        key-light.local:9123/elgato/lights
    request = urllib.request.Request(url=KEYLIGHT_URL,
                                 data=bytes(json.dumps(keylight), encoding='utf8'),
                                 method='PUT')
    urllib.request.urlopen(request)
    


if __name__ == "__main__":
    main()
