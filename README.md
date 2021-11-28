# wifi_wrapper
A python wrapper over nmcli tool for linux devices.

## Install
```console
pip install wifi_wrapper
```

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

- After the installation has completed, start the Network Manager.
```console
sudo systemctl start NetworkManager.service
```
- Next, we will enable Network Manager to start on system boot. 

```console
sudo systemctl enable NetworkManager.service
```

- Disable hostapd and dnsmasq
```console
sudo systemctl disable dnsmasq.service
sudo systemctl disable hostapd.service
```

- Make sure your `/etc/NetworkManager/NetworkManager.conf` file looks exactly like this 
```bash
[main]
plugins=ifupdown,keyfile
dhcp=internal

[ifupdown]
managed=false
```
