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
        else:
            nmcli_result = nmcli_result.decode('utf-8')
        # nmcli_result = nmcli_result.split('\n')
        
        return nmcli_result

    @classmethod
    def connect(self, ssid, password):
        """
        Connect to a network.
        """
        cmd = ["sudo", "nmcli", "dev", "wifi", "connect", f"{ssid}", "password", f"{password}"]
        self.run_command(cmd)
        self.ssid = ssid
        return

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
        formatted_data = prepare_data(res)
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
        formatted_data = prepare_data(res)
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
        formatted_data = prepare_data(res)
        return formatted_data

    @classmethod
    def create_hotspot(self, ssid, password):
        """
        Creates a hotspot.
        """
        cmd = ["sudo", "nmcli", "dev", "wifi", "hotspot", "ifname", "wlan0", "ssid", f"{ssid}", "password", f"{password}"]
        self.run_command(cmd)
        return


def prepare_data(data):
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

    for j in range(1,length_final_data):
        temp= {}
        for i in range(0,length_final_data):
            # Preparing the data. Traverse the temp_data (2D array) and create a dict.
            # For eg: temp_data = [["DEVICE", "TYPE", "STATE", "CONNECTION"], ["wlan0", "wifi", "connected", "WillowCove"]]
            # index[0][n] contains the keys and index [1][n], [2][n], [3][n]... contains the values.
            temp[f"{temp_data[0][i]}"] = temp_data[j][i]
        
        final_data.append(temp)

    return final_data