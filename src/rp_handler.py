import time

import runpod
import requests
from requests.adapters import HTTPAdapter, Retry
import requests
import urllib.parse
import base64
from rembg import remove
from PIL import Image
from io import BytesIO

LOCAL_URL = "http://127.0.0.1:7000/api"

automatic_session = requests.Session()
retries = Retry(total=10, backoff_factor=0.1, status_forcelist=[502, 503, 504])
automatic_session.mount('http://', HTTPAdapter(max_retries=retries))


# ---------------------------------------------------------------------------- #
#                              Automatic Functions                             #
# ---------------------------------------------------------------------------- #
def wait_for_service(url):
    '''
    Check if the service is ready to receive requests.
    '''
    while True:
        try:
            requests.get(url, timeout=120)
            return
        except requests.exceptions.RequestException:
            print("Service not ready yet. Retrying...")
        except Exception as err:
            print("Error: ", err)

        time.sleep(0.2)


# ---------------------------------------------------------------------------- #
#                                RunPod Handler                                #
# ---------------------------------------------------------------------------- #
def handler(event):
    '''
    This is the handler function that will be called by the serverless.
    '''

    base64Input = event['input']['src']

    output_path = 'output.png'
    base64Input = base64Input.replace('data:image/png;base64,', '').replace('data:image/jpeg;base64,', '')

    input= Image.open(BytesIO(base64.b64decode(base64Input)))

    output = remove(input)
    output.save(output_path)

    outputImage= Image.open(output_path)

    base64_output = base64.b64encode(outputImage.tobytes()).decode('utf-8')

    return base64_output


if __name__ == "__main__":
    # wait_for_service(url=f'{LOCAL_URL}')

    print("rembg API Service is ready. Starting RunPod...")

    runpod.serverless.start({"handler": handler})
