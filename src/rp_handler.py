import runpod
import base64
from rembg import remove
from PIL import Image
from io import BytesIO
import re

# ---------------------------------------------------------------------------- #
#                              Utility Functions                               #
# ---------------------------------------------------------------------------- #

def image_to_base64(image_path):
    with open(image_path, "rb") as img_file:
        image_bytes = img_file.read()
        base64_encoded = base64.b64encode(image_bytes)
        base64_string = base64_encoded.decode('utf-8')
        return base64_string
    
def open_image_from_data_uri(data_uri):
    # Extract the image data from the data URI
    image_data = re.sub('^data:image/.+;base64,', '', data_uri)
    
    # Decode the base64 encoded image data
    image_bytes = BytesIO(base64.b64decode(image_data))
    
    # Open the image using Pillow
    image = Image.open(image_bytes)
    
    return image

# ---------------------------------------------------------------------------- #
#                                RunPod Handler                                #
# ---------------------------------------------------------------------------- #
def handler(event):
    '''
    This is the handler function that will be called by the serverless.
    '''

    data_uri_inputs = event['input']['data_uris']

    results = []
    index = 0
    for data_uri_input in data_uri_inputs:
        input = open_image_from_data_uri(data_uri_input)

        output_path = f"output_{index}.png"
        output = remove(input)
        output.save(output_path)

        result = image_to_base64(output_path)
        results.append(result)
        index = index+1

    return results


if __name__ == "__main__":
    print("rembg API Service is ready. Starting RunPod...")

    runpod.serverless.start({"handler": handler})
