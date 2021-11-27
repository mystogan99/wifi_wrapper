import wifi_wrapper.subprocess_wrapper as wrap

class WiFi:
    """
    Presents a Python interface to the output of nmcli.
    """

    def __init__(self):
        self.ssid = None
        self.wifi_details = []

    
    @classmethod
    def run_command(cls, cmd):
        """
        Run any command accepted by nmcli.
        cmd should be a array of strings.
        for eg: ["sudo", "nmcli", "dev", "wifi"]
        """
        nmcli_result = None
        try:
            nmcli_result = wrap.check_output(cmd,stderr=wrap.STDOUT)
        except wrap.CalledProcessError as e:
            print(f"There was some error -> {e.output.strip()}")
            return e.output.strip()
        else:
            nmcli_result = nmcli_result.decode('utf-8')
        # nmcli_result = nmcli_result.split('\n')
        
        return nmcli_result

    @classmethod
    def general_status(self):
        """
        Returns the general status of the wifi.
        """
        res = self.run_command(["sudo", "nmcli", "general", "status"])
        formatted_data = self.prepare_data(res)
        return formatted_data

    @classmethod
    def is_hotspot_enabled(self):
        """
        Returns True if wifi hotspot is enabled
        """
        res = self.run_command(["sudo", "nmcli", "general", "status"])
        return True if (res.find("local only") != -1) else False


    @classmethod
    def connected(self):
        """
        Returns True if the device is connected to a network.
        """
        cmd = ["sudo" , "nmcli", "con", "show" , "--active"]
        res = self.run_command(cmd)
        formatted_data = self.prepare_data(res)
        return formatted_data

    @classmethod
    def connect(self, ssid, password):
        """
        Connect to a network.
        """
        cmd = ["sudo", "nmcli", "dev", "wifi", "connect", f"{ssid}", "password", f"{password}"]
        res = self.run_command(cmd)
        return res

    @classmethod
    def get_connection_status(self):
        """
        Returns the connection status of the device.
        [
            {
                "CONNECTION": "WillowCove",
                "DEVICE": "wlan0",
                "STATE": "connected",
                "TYPE": "wifi",
            }
        ]
        """
        cmd = ["sudo", "nmcli", "dev"]
        res = self.run_command(cmd)
        formatted_data = self.prepare_data(res)
        return formatted_data
    
    @classmethod
    def wifi_enabled(self):
        """
        Returns True if the wifi is enabled.
        """
        cmd = ["sudo", "nmcli", "n"]
        res =  self.run_command(cmd)
        return True if res.find("enabled") != -1 else False

    @classmethod
    def start_wifi(self):
        """
        Starts the wifi.
        """
        cmd = ["sudo", "nmcli", "radio", "wifi", "on"]
        self.run_command(cmd)
        return True if self.wifi_enabled() else False

    @classmethod
    def scan(self):
        """
        Scans for available networks.
        Result:
        [
            {
                "IN-USE": "*",
                "BSSID": "8C:A3:99:36:4B:65",
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
        cmd = ["sudo", "nmcli", "dev", "wifi"]
        res = self.run_command(cmd)
        formatted_data = self.prepare_data(res)
        return formatted_data

    @classmethod
    def get_ssid(self):
        """
        Returns the SSID of the current network.
        """
        return self.ssid

    @classmethod
    def get_saved_connections(self):
        """
        Returns a list of all saved connections.

        [
            {
            'DEVICE': 'wlan0',
            'NAME': 'WillowCove',
            'TYPE': 'wifi',
            'UUID': 'fa06ef2a-d174-4f37-8f95-d12b2117a288'
            }
        ]

        """
        cmd = ["sudo", "nmcli", "c"]
        res = self.run_command(cmd)
        formatted_data = self.prepare_data(res)
        return formatted_data
    
    @classmethod
    def disable_hotspot(self, scheme_name):
        """
        Stop hotspot with given scheme name.
        """
        cmd = ["sudo", "nmcli", "con", "down", scheme_name]
        res = self.run_command(cmd)
        return res

    @classmethod
    def create_hotspot(self, name):
        """
        Creates a hotspot.
        from : https://unix.stackexchange.com/a/384513
        """
        cached_scan_result = self.scan()
        cmd = ["sudo", "nmcli", "connection", "up", f"{name}"]
        self.run_command(cmd)
        return cached_scan_result
    
    @classmethod
    def create_hotspot_scheme(self, name, ssid, password):
        """
        Creates a scheme for connecting to hotspot.
        """
        # nmcli c add type wifi ifname wifi-device con-name connection-name autoconnect no ssid hotspot-ssid
        # nmcli connection modify connection-name 802-11-wireless.mode ap 802-11-wireless.band bg ipv4.method shared
        # nmcli connection modify connection-name wifi-sec.key-mgmt wpa-psk
        # nmcli connection modify connection-name wifi-sec.psk "le password"
        # nmcli connection up connection-name

        cmd1 = ['sudo', 'nmcli', 'c', 'add', 'type', 'wifi', 'ifname', 'wlan0', 'con-name', f'{name}', 'autoconnect', 'no', 'ssid', f'{ssid}']
        cmd2 = ['sudo', 'nmcli', 'connection', 'modify', f'{name}', '802-11-wireless.mode', 'ap', '802-11-wireless.band', 'bg', 'ipv4.method', 'shared']
        cmd3 = ['sudo', 'nmcli', 'connection', 'modify', f'{name}', 'wifi-sec.key-mgmt', 'wpa-psk']
        cmd4 = ['sudo', 'nmcli', 'connection', 'modify', f'{name}', 'wifi-sec.psk', f'{password}']
        self.run_command(cmd1)
        self.run_command(cmd2)
        self.run_command(cmd3)
        self.run_command(cmd4)
        return

    @classmethod    
    def prepare_data(self, data):
        """
        Returns a dict from string formatted table For eg:

        DEVICE         TYPE      STATE         CONNECTION
        wlan0          wifi      connected     WillowCove
        p2p-dev-wlan0  wifi-p2p  disconnected  --
        lo             loopback  unmanaged     --

        >> 
            [
                {
                    "CONNECTION": "WillowCove",
                    "DEVICE": "wlan0",
                    "STATE": "connected",
                    "TYPE": "wifi",
                },
                { ... },
                { ... },
            ]

        """
        final_data = []
        if data is not None:
            rows = data.split("\n")
            # after splitting the data, we have a empty array in the end.
            del rows[-1]
            temp_data = []
            for row in rows:
                    single_row = row.split(" ")
                    formatted_data = []
                    memo = None
                    for ele in range(0,len(single_row)):
                            if (single_row[ele] != "" or ele == 0):
                                    # If we have combined two elemets we need to skip this element
                                    if memo == single_row[ele]:
                                        continue
                                    val = single_row[ele]
                                    last_index = len(single_row) - 1
                                    # If we have reached the last element, no need to check
                                    if (ele != last_index):
                                        if (single_row[ele+1] != ""):
                                                # if 2 consecutive elements in the row are not empty,
                                                # then we have to combine them.
                                                # For eg: "120","MBits/s"
                                                val = val  + " " + single_row[ele+1]
                                                # save this for use in next iteration
                                                memo = single_row[ele+1]

                                    formatted_data.append(val)
                    # Remove the last element which is always empty.
                    if len(formatted_data) > 0:
                        temp_data.append(formatted_data)

            length_final_data = len(temp_data)

            try:

                for down in range(1,length_final_data):
                    temp= {}
                    for side in range(0,len(temp_data[0])):
                        # Preparing the data. Traverse the temp_data (2D array) and create a dict.
                        # For eg: temp_data = [["DEVICE", "TYPE", "STATE", "CONNECTION"], ["wlan0", "wifi", "connected", "WillowCove"]]
                        # index[0][n] contains the keys and index [1][n], [2][n], [3][n]... contains the values.
                        temp[f"{temp_data[0][side]}"] = temp_data[down][side]
                    
                    final_data.append(temp)
            except IndexError as error:
                print("There was some error : ", error)
                print(temp_data)
                return []

            return final_data
        else:
            return []