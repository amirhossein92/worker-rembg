# -*- coding: utf-8 -*-

from pathlib import Path
from urllib import request


# Define the URL of the file to download
model_url = 'https://github.com/Alyetama/Rembg-Online/releases/download/v0.0.0/u2net.onnx'

# Define the directory where you want to save the file
save_dir = Path.home() / '.u2net'

# Make sure the directory exists, if not, create it
save_dir.mkdir(parents=True, exist_ok=True)

# Define the path where you want to save the file
save_path = save_dir / 'u2net.onnx'

# Download the file and save it
request.urlretrieve(model_url, save_path)