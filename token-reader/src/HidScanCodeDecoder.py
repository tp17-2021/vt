class HidScanCodeDecoder:
    def __init__(self):
        """
        Decode URB_INTERRUPT_IN bytes

        Keyboard report format (docs from https://stackoverflow.com/a/27085911)
        Byte 0: Keyboard modifier bits (SHIFT, ALT, CTRL etc)
        Byte 1: reserved
        Byte 2-7: Up to six keyboard usage indexes representing the keys that are
                currently "pressed".
                Order is not important, a key is either pressed (present in the
                buffer) or not pressed.
        """

        # associate USB HID scan codes with ascii characters
        self.scan_code_map = {
            4: "a",
            5: "b",
            6: "c",
            7: "d",
            8: "e",
            9: "f",
            30: "1",
            31: "2",
            32: "3",
            33: "4",
            34: "5",
            35: "6",
            36: "7",
            37: "8",
            38: "9",
            39: "0",
            40: "\n",
        }

    def decode(self, bytesArray) -> str:
        if len(bytesArray) < 3:
            return ""

        keycode = int(bytesArray[2])
        if not keycode in self.scan_code_map:  # if we have a valid key code in scan_code_map
            if keycode != 0:
                print("Unknown keycode: " + str(keycode))

            return ""

        return self.scan_code_map[keycode]
            
