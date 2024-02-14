# ---------------------------------------------------------------------------- #
#                        Stage 1: Build the final image                        #
# ---------------------------------------------------------------------------- #
FROM python:3.10.9-slim as build_final_image

ENV DEBIAN_FRONTEND=noninteractive \
   PIP_PREFER_BINARY=1 \
   LD_PRELOAD=libtcmalloc.so \
   ROOT=/ \
   PYTHONUNBUFFERED=1

SHELL ["/bin/bash", "-o", "pipefail", "-c"]



RUN apt-get update && \
   apt install -y \
   git && \
   apt-get autoremove -y && rm -rf /var/lib/apt/lists/* && apt-get clean -y

# Install Python dependencies (Worker Template)
COPY builder/requirements.txt /requirements.txt
RUN --mount=type=cache,target=/root/.cache/pip \
   pip install --upgrade pip && \
   pip install --upgrade -r /requirements.txt --no-cache-dir && \
   rm /requirements.txt

COPY builder/download_model.py /download_model.py

ADD src .

# Cleanup section (Worker Template)
# RUN apt-get autoremove -y && \
#     apt-get clean -y && \
#     rm -rf /var/lib/apt/lists/*

# Set permissions and specify the command to run
RUN chmod +x start.sh
CMD ls && ./start.sh
