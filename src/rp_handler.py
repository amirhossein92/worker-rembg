import time

import runpod
import requests
from requests.adapters import HTTPAdapter, Retry
import requests
import urllib.parse
import base64

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


def run_inference(inference_request, endpoint_query):
    '''
    Run inference on a request.
    '''

    # Convert the inference_request to form data
    form_data = urllib.parse.urlencode(inference_request)

    # Convert the form data to a dictionary
    form_data_dict = dict(urllib.parse.parse_qsl(form_data))

    # Create a dictionary of files to be sent as multipart/form-data
    files = {}
    for key, value in form_data_dict.items():
        if key == 'file':
            # Convert base64 encoded image to file stream
            file_stream = base64.b64decode(value)
            files[key] = ('image.png', file_stream)
        else:
            files[key] = (None, value)

    # Send the request as multipart/form-data
    response = automatic_session.post(url=f'{LOCAL_URL}/remove?{endpoint_query}', files=files, timeout=600)

    # Convert byte array to base64
    base64_image = base64.b64encode(response.content).decode('utf-8')
    return base64_image


# ---------------------------------------------------------------------------- #
#                                RunPod Handler                                #
# ---------------------------------------------------------------------------- #
def handler(event):
    '''
    This is the handler function that will be called by the serverless.
    '''

    json = run_inference(event["input"]["form"], event["input"]["query"])

    # return the output that you want to be returned like pre-signed URLs to output artifacts
    return json


if __name__ == "__main__":
    wait_for_service(url=f'{LOCAL_URL}')

    print("rembg API Service is ready. Starting RunPod...")

    runpod.serverless.start({"handler": handler})
