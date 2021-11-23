from __future__ import division
import subprocess_wrapper as wrap

class Wifi:
    """
    Presents a Python interface to the output of nmcli.
    """

    def __init__(self):
        self.ssid = None

    
    @classmethod
    def run_command(cls, cmd):
        """
        Returns a list of all cells extracted from the output of iwlist.
        """
        nmcli_result = None
        try:
            nmcli_result = wrap.check_output(['sudo','nmcli', cmd],stderr=wrap.STDOUT)
        except wrap.CalledProcessError as e:
            print(f"There was some error -> {e.output.strip()}")
        else:
            nmcli_result = nmcli_result.decode('utf-8')
        # nmcli_result = nmcli_result.split('\n')
        
        return nmcli_result

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
            },
            {
                "CONNECTION": "--",
                "DEVICE": "p2p-dev-wlan0",
                "STATE": "disconnected",
                "TYPE": "wifi-p2p",
            },
        ]
        """
        res = self.run_command("d")
        formatted_data = prepare_data(res)
        return formatted_data
    
    @classmethod
    def wifi_enabled(self):
        """
        Returns True if the wifi is enabled.
        """
        res =  self.run_command("n")
        print(dir(res))
        return True if res.find("enabled") != -1 else False

    @classmethod
    def get_ssid(self):
        """
        Returns the SSID of the current network.
        """

        return self.ssid



def prepare_data(data):
    """
    Returns a dict from string formatted table For eg:

    DEVICE         TYPE      STATE         CONNECTION
    wlan0          wifi      connected     WillowCove
    p2p-dev-wlan0  wifi-p2p  disconnected  --
    lo             loopback  unmanaged     --

    """
    final_data = []

    rows = data.split("\n")
    temp_data = []
    for row in rows:
            single_row = row.split(" ")
            formatted_data = []
            for ele in single_row:
                    if (ele != ""):
                            formatted_data.append(ele)
            if len(formatted_data) > 0:
                temp_data.append(formatted_data)

    length_final_data = len(temp_data)

    for j in range(1,length_final_data):
        temp= {}
        for i in range(0,length_final_data):
            temp[f"{temp_data[0][i]}"] = temp_data[j][i]
        
        final_data.append(temp)

    return final_data