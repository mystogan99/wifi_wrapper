from wifi import Wifi
from pprint import pprint


wifi = Wifi()

# enabled = wifi.wifi_enabled("n")

connection = wifi.get_connection_status()

print("Your connection status :")
pprint(connection) 

