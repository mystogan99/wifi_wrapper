from wifi_wrapper import Wifi
from pprint import pprint


wifi = Wifi()

# enabled = wifi.wifi_enabled("n")

# res = wifi.run_command("dev wifi")

connection = wifi.scan()

print("Your connection status :")
pprint(connection) 

