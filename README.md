# wifi_wrapper
A python wrapper over nmcli tool for linux devices.

## Quick Usage
```python
from wifi_wrapper import WiFi
from pprint import pprint


wifi = WiFi()

enabled = wifi.wifi_enabled()

if enabled:
  connections = wifi.scan()
  print("Available wifi nearby :")
  pprint(connections) 
"""
Output ->

Available wifi nearby:
        [
            {
                "IN-USE": "*",
                "BSSID": "8C:A3:99:16:4C:63",
                "SSID": "WillowCove",
                "MODE": "Infra",
                "CHAN": "1",
                "RATE": "130 Mbit/s",
                "SIGNAL": "74",
                "BARS": "▂▄▆_",
                "SECURITY": "WPA2",
                "CLIENT": "yes",    
            },
            { ... },
            { ... },
        ]
"""
```
