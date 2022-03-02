import requests
from Reader import Reader
import os

def main():
    reader = Reader()

    while True:
        try:
            token = reader.read()
            print("Token:", token)
            requests.post(
                f'http://{os.environ["TOKEN_URL"]}',
                json=token
            )

        except OSError as e:
            print("Reader disconnected")
            reader.connect_to_reader()


if __name__ == "__main__":
    main()
