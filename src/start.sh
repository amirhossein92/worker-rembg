#!/bin/bash

echo "Worker Initiated"

# echo "Starting rembg server"
# rembg s --port 7000 --log_level info &

echo "Download Models"
python -u ./download_model.py

echo "Starting RunPod Handler"
python -u ./rp_handler.py
