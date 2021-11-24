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

## Dependency
- Your system should have nmcli installed and you should have sudo permissions
```console
sudo apt install network-manager
```

- After the installation has completed, we can start the Network Manager with this command.
```console
sudo systemctl start NetworkManager.service
```
- Next, we will enable Network Manager to start on system boot with using the systemctl command below. 

```console
sudo systemctl enable NetworkManager.service
```
