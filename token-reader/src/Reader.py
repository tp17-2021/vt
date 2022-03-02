from time import sleep
from HidScanCodeDecoder import HidScanCodeDecoder
import hid

VERBOSE = False


class Reader:
    def __init__(self, vendor_id: int = 0x04d9, product_id: int = 0x1503):
        self.decoder = HidScanCodeDecoder()
        self.vendor_id = vendor_id
        self.product_id = product_id

        self.connect_to_reader()


    def connect_to_reader(self):
        print("Waiting for the reader to be connected")
        while True:
            try:
                h = hid.device()
                h.open(self.vendor_id, self.product_id)  # reader
                self.h = h
                print("Connected to the reader")
                break
            except OSError as e:
                if VERBOSE:
                    print("Printed not yet connected")
                sleep(.1)


    def debug_print_reader_info(self):
        print("Manufacturer:", self.h.get_manufacturer_string())
        print("Product:", self.h.get_product_string())
        print("Serial No:", self.h.get_serial_number_string())


    def disconnect_from_reader(self) -> None:
        print("Disconnecting from the reader")
        self.h.close()


    def read(self) -> str:
        print("Reading from the reader")

        out = ""
        while True:
            d = self.h.read(4)  # d format: [0, 0, 0, 0]

            if not d:
                continue

            d = bytearray(d)
            ascii_char = self.decoder.decode(d)
            if ascii_char != "":
                if ascii_char == "\n":
                    self.h.read(4)
                    return out

                out += ascii_char
