# ---------------------------------------------------------------------------- #
#                        Stage 1: Build the final image                        #
# ---------------------------------------------------------------------------- #
FROM python:3.10.9-slim as build_final_image

ARG SHA=0dcdb080ae083de57084c38e93fb210534c5c693

ENV DEBIAN_FRONTEND=noninteractive \
   PIP_PREFER_BINARY=1 \
   LD_PRELOAD=libtcmalloc.so \
   ROOT=/rembg \
   PYTHONUNBUFFERED=1

SHELL ["/bin/bash", "-o", "pipefail", "-c"]

RUN apt-get update && \
   apt install -y \
   fonts-dejavu-core rsync git jq moreutils aria2 wget libgoogle-perftools-dev procps libgl1 libglib2.0-0 && \
   apt-get autoremove -y && rm -rf /var/lib/apt/lists/* && apt-get clean -y

RUN --mount=type=cache,target=/root/.cache/pip \
   git clone https://github.com/danielgatis/rembg.git && \
   cd rembg && \
   git reset --hard ${SHA}

WORKDIR /rembg

RUN pip install --upgrade pip

COPY . .

RUN python -m pip install ".[cli]"

ADD src .

# Set permissions and specify the command to run
RUN chmod +x start.sh
CMD ls && ./start.sh
